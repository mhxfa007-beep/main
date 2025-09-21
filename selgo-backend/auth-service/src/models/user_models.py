from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Text, Float, JSON
from sqlalchemy.sql import func
from ..database.database import Base
import enum

class UserRole(enum.Enum):
    ADMIN = "admin"
    BUYER = "buyer"
    SELLER = "seller"
    BUSINESS = "business"

class AuthProvider(enum.Enum):
    EMAIL = "email"
    GOOGLE = "google"
    TWITTER = "twitter"
    FACEBOOK = "facebook"

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=True)  # Nullable for OAuth users
    full_name = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    role = Column(Enum(UserRole), default=UserRole.BUYER)
    auth_provider = Column(Enum(AuthProvider), default=AuthProvider.EMAIL)
    provider_id = Column(String(255), nullable=True)  # OAuth provider user ID
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    last_login = Column(DateTime, nullable=True)
    
    # Finn.no-like features
    location = Column(String(255), nullable=True)  # User's location
    postal_code = Column(String(10), nullable=True)
    bio = Column(Text, nullable=True)  # User description
    rating = Column(Float, default=0.0)  # Average rating from other users
    rating_count = Column(Integer, default=0)  # Number of ratings received
    
    # Notification preferences
    email_notifications = Column(Boolean, default=True)
    sms_notifications = Column(Boolean, default=False)
    push_notifications = Column(Boolean, default=True)
    marketing_emails = Column(Boolean, default=False)
    
    # Business information (for business users)
    company_name = Column(String(255), nullable=True)
    company_org_number = Column(String(50), nullable=True)
    company_address = Column(Text, nullable=True)
    
    # Additional profile data
    date_of_birth = Column(DateTime, nullable=True)
    profile_completion = Column(Integer, default=0)  # Percentage of profile completion
    
    # Privacy settings
    show_phone = Column(Boolean, default=True)
    show_email = Column(Boolean, default=False)
    show_location = Column(Boolean, default=True)

class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    token = Column(Text, nullable=False, unique=True)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now())
    is_revoked = Column(Boolean, default=False)

class UserRating(Base):
    __tablename__ = 'user_ratings'
    
    id = Column(Integer, primary_key=True, index=True)
    rater_id = Column(Integer, nullable=False, index=True)  # User who gives the rating
    rated_user_id = Column(Integer, nullable=False, index=True)  # User being rated
    rating = Column(Integer, nullable=False)  # 1-5 stars
    comment = Column(Text, nullable=True)
    transaction_id = Column(String(255), nullable=True)  # Related transaction/listing
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class UserFavorite(Base):
    __tablename__ = 'user_favorites'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    item_type = Column(String(50), nullable=False)  # 'car', 'property', 'job', etc.
    item_id = Column(String(255), nullable=False)  # ID of the favorited item
    service_name = Column(String(50), nullable=False)  # Which microservice
    created_at = Column(DateTime, default=func.now())

class UserNotification(Base):
    __tablename__ = 'user_notifications'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), nullable=False)  # 'message', 'favorite', 'price_drop', etc.
    is_read = Column(Boolean, default=False)
    related_item_type = Column(String(50), nullable=True)
    related_item_id = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now())

class SavedSearch(Base):
    __tablename__ = 'saved_searches'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    search_name = Column(String(255), nullable=False)
    service_name = Column(String(50), nullable=False)  # 'car', 'property', etc.
    search_criteria = Column(JSON, nullable=False)  # Search parameters as JSON
    email_alerts = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  
