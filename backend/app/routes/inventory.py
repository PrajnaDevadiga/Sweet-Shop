from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Sweet
from ..schemas import PurchaseRequest, RestockRequest, SweetResponse
from ..auth import get_current_user, get_current_admin_user

router = APIRouter(prefix="/api/sweets", tags=["inventory"])


@router.post("/{sweet_id}/purchase", response_model=SweetResponse)
async def purchase_sweet(
    sweet_id: int,
    purchase: PurchaseRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Purchase a sweet, decreasing its quantity"""
    if purchase.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Purchase quantity must be greater than 0"
        )
    
    db_sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()
    if not db_sweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sweet not found"
        )
    
    if db_sweet.quantity < purchase.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient quantity available"
        )
    
    db_sweet.quantity -= purchase.quantity
    db.commit()
    db.refresh(db_sweet)
    return db_sweet


@router.post("/{sweet_id}/restock", response_model=SweetResponse)
async def restock_sweet(
    sweet_id: int,
    restock: RestockRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """Restock a sweet, increasing its quantity (Admin only)"""
    if restock.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Restock quantity must be greater than 0"
        )
    
    db_sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()
    if not db_sweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sweet not found"
        )
    
    db_sweet.quantity += restock.quantity
    db.commit()
    db.refresh(db_sweet)
    return db_sweet

