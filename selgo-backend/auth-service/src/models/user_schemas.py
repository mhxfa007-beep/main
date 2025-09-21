from pydantic import BaseModel, EmailStr, Field, ConfigDict  # Updated import
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from .user_models import UserRole, AuthProvider

# User schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    role: UserRole = UserRole.BUYER
    location: Optional[str] = None
    postal_code: Optional[str] = None

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    location: Optional[str] = None
    postal_code: Optional[str] = None
    bio: Optional[str] = None
    date_of_birth: Optional[date] = None
    company_name: Optional[str] = None
    company_org_number: Optional[str] = None
    company_address: Optional[str] = None

class NotificationPreferences(BaseModel):
    email_notifications: bool = True
    sms_notifications: bool = False
    push_notifications: bool = True
    marketing_emails: bool = False

class PrivacySettings(BaseModel):
    show_phone: bool = True
    show_email: bool = False
    show_location: bool = True

class UserResponse(UserBase):
    id: int
    role: UserRole
    auth_provider: AuthProvider
    avatar_url: Optional[str] = None
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    location: Optional[str] = None
    postal_code: Optional[str] = None
    bio: Optional[str] = None
    rating: float = 0.0
    rating_count: int = 0
    profile_completion: int = 0
    company_name: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)  # Updated for Pydantic v2

class UserProfileResponse(UserResponse):
    email_notifications: bool
    sms_notifications: bool
    push_notifications: bool
    marketing_emails: bool
    show_phone: bool
    show_email: bool
    show_location: bool
    date_of_birth: Optional[date] = None
    company_org_number: Optional[str] = None
    company_address: Optional[str] = None

# Auth schemas
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=6)

# OAuth schemas
class OAuthCallback(BaseModel):
    code: str
    state: Optional[str] = None

# Token validation response (for other services)
class TokenValidationResponse(BaseModel):
    user_id: int
    username: str
    email: str
    role: UserRole
    is_active: bool

# Rating schemas
class UserRatingCreate(BaseModel):
    rated_user_id: int
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None
    transaction_id: Optional[str] = None

class UserRatingResponse(BaseModel):
    id: int
    rater_id: int
    rated_user_id: int
    rating: int
    comment: Optional[str] = None
    transaction_id: Optional[str] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Favorite schemas
class UserFavoriteCreate(BaseModel):
    item_type: str
    item_id: str
    service_name: str

class UserFavoriteResponse(BaseModel):
    id: int
    user_id: int
    item_type: str
    item_id: str
    service_name: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Notification schemas
class UserNotificationCreate(BaseModel):
    user_id: int
    title: str
    message: str
    notification_type: str
    related_item_type: Optional[str] = None
    related_item_id: Optional[str] = None

class UserNotificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    notification_type: str
    is_read: bool
    related_item_type: Optional[str] = None
    related_item_id: Optional[str] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Saved search schemas
class SavedSearchCreate(BaseModel):
    search_name: str
    service_name: str
    search_criteria: Dict[str, Any]
    email_alerts: bool = True

class SavedSearchResponse(BaseModel):
    id: int
    user_id: int
    search_name: str
    service_name: str
    search_criteria: Dict[str, Any]
    email_alerts: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)