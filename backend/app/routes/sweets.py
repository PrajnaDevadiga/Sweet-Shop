from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..database import get_db
from ..models import User, Sweet
from ..schemas import SweetCreate, SweetUpdate, SweetResponse, SearchParams
from ..auth import get_current_user, get_current_admin_user

router = APIRouter(prefix="/api/sweets", tags=["sweets"])


@router.post("", response_model=SweetResponse, status_code=status.HTTP_201_CREATED)
async def create_sweet(
    sweet: SweetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """Create a new sweet (Admin only)"""
    # Check if sweet with same name already exists
    db_sweet = db.query(Sweet).filter(Sweet.name == sweet.name).first()
    if db_sweet:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sweet with this name already exists"
        )
    
    db_sweet = Sweet(**sweet.model_dump())
    db.add(db_sweet)
    db.commit()
    db.refresh(db_sweet)
    return db_sweet


@router.get("", response_model=List[SweetResponse])
async def list_sweets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all available sweets"""
    sweets = db.query(Sweet).all()
    return sweets


@router.get("/search", response_model=List[SweetResponse])
async def search_sweets(
    name: str = Query(None),
    category: str = Query(None),
    min_price: float = Query(None),
    max_price: float = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Search sweets by name, category, or price range"""
    query = db.query(Sweet)
    
    if name:
        query = query.filter(Sweet.name.ilike(f"%{name}%"))
    if category:
        query = query.filter(Sweet.category.ilike(f"%{category}%"))
    if min_price is not None:
        query = query.filter(Sweet.price >= min_price)
    if max_price is not None:
        query = query.filter(Sweet.price <= max_price)
    
    sweets = query.all()
    return sweets


@router.get("/{sweet_id}", response_model=SweetResponse)
async def get_sweet(
    sweet_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific sweet by ID"""
    sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()
    if not sweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sweet not found"
        )
    return sweet


@router.put("/{sweet_id}", response_model=SweetResponse)
async def update_sweet(
    sweet_id: int,
    sweet_update: SweetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """Update a sweet (Admin only)"""
    db_sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()
    if not db_sweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sweet not found"
        )
    
    update_data = sweet_update.model_dump(exclude_unset=True)
    
    # Check if updating name would create duplicate
    if "name" in update_data and update_data["name"] != db_sweet.name:
        existing = db.query(Sweet).filter(Sweet.name == update_data["name"]).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Sweet with this name already exists"
            )
    
    for field, value in update_data.items():
        setattr(db_sweet, field, value)
    
    db.commit()
    db.refresh(db_sweet)
    return db_sweet


@router.delete("/{sweet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sweet(
    sweet_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """Delete a sweet (Admin only)"""
    db_sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()
    if not db_sweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sweet not found"
        )
    db.delete(db_sweet)
    db.commit()
    return None

