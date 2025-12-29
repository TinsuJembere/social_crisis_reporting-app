"""
Pydantic schemas for request/response validation
Will be used in authentication and CRUD endpoints
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models import UserRole, IssueCategory, IssueStatus

# User Schemas
class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    role: UserRole
    created_at: datetime
    
    class Config:
        from_attributes = True

# Authentication Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRegister(UserCreate):
    pass

# Issue Schemas
class IssueBase(BaseModel):
    title: str
    description: str
    category: IssueCategory
    latitude: float
    longitude: float

class IssueCreate(IssueBase):
    pass

class IssueUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[IssueCategory] = None
    status: Optional[IssueStatus] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class IssueResponse(IssueBase):
    id: int
    status: IssueStatus
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    reporter_id: int
    
    class Config:
        from_attributes = True

# Notification Schemas
class NotificationBase(BaseModel):
    title: str
    message: str

class NotificationCreate(NotificationBase):
    user_id: int
    issue_id: Optional[int] = None

class NotificationResponse(NotificationBase):
    id: int
    user_id: int
    issue_id: Optional[int] = None
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

