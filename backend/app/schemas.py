from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(UserBase):
    id: int
    is_admin: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class SweetBase(BaseModel):
    name: str
    category: str
    price: float
    quantity: int


class SweetCreate(SweetBase):
    pass


class SweetUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None


class SweetResponse(SweetBase):
    id: int

    class Config:
        from_attributes = True


class PurchaseRequest(BaseModel):
    quantity: int = 1


class RestockRequest(BaseModel):
    quantity: int


class SearchParams(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None

