from sqlalchemy.orm import Session
from typing import Optional, Tuple
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from ..models.user_models import User, RefreshToken, UserRole, AuthProvider, UserRating
from ..models.user_schemas import UserCreate, LoginRequest, UserResponse
from ..repositories.user_repository import UserRepository
from ..utils.auth_utils import hash_password, verify_password, create_access_token, create_refresh_token
from ..config.config import settings
import logging

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()
    
    def register_user(self, db: Session, user_data: UserCreate) -> User:
        """Register a new user."""
        # Check if user already exists
        existing_user = self.user_repo.get_by_email(db, user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        existing_username = self.user_repo.get_by_username(db, user_data.username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        # Create user
        hashed_password = hash_password(user_data.password)
        user_dict = user_data.dict(exclude={'password'})
        user_dict['hashed_password'] = hashed_password
        user_dict['auth_provider'] = AuthProvider.EMAIL
        
        return self.user_repo.create(db, user_dict)
    
    def authenticate_user(self, db: Session, login_data: LoginRequest) -> Tuple[str, str, User]:
        """Authenticate user and return tokens."""
        # Try to find user by username or email
        user = self.user_repo.get_by_username(db, login_data.username)
        if not user:
            user = self.user_repo.get_by_email(db, login_data.username)
        
        if not user or not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username/email or password"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is deactivated"
            )
        
        # Create tokens
        access_token = self._create_user_access_token(user)
        refresh_token = self._create_user_refresh_token(db, user)
        
        # Update last login
        self.user_repo.update_last_login(db, user.id)
        
        return access_token, refresh_token, user
    
    def refresh_access_token(self, db: Session, refresh_token: str) -> str:
        """Create new access token from refresh token."""
        token_record = self.user_repo.get_refresh_token(db, refresh_token)
        
        if not token_record or token_record.is_revoked:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        if token_record.expires_at < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token expired"
            )
        
        user = self.user_repo.get_by_id(db, token_record.user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        return self._create_user_access_token(user)
    
    def revoke_refresh_token(self, db: Session, refresh_token: str) -> bool:
        """Revoke a refresh token (logout)."""
        return self.user_repo.revoke_refresh_token(db, refresh_token)
    
    def change_password(self, db: Session, user_id: int, current_password: str, new_password: str) -> bool:
        """Change user password."""
        user = self.user_repo.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if not verify_password(current_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect current password"
            )
        
        new_hashed_password = hash_password(new_password)
        return self.user_repo.update_password(db, user_id, new_hashed_password)
    
    def _create_user_access_token(self, user: User) -> str:
        """Create access token for user."""
        token_data = {
            "sub": str(user.id),
            "username": user.username,
            "email": user.email,
            "role": user.role.value,
            "is_active": user.is_active
        }
        return create_access_token(token_data)
    
    def _create_user_refresh_token(self, db: Session, user: User) -> str:
        """Create and store refresh token for user."""
        refresh_token = create_refresh_token()
        expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        
        self.user_repo.create_refresh_token(db, user.id, refresh_token, expires_at)
        return refresh_token
    
    def calculate_profile_completion(self, user: User) -> int:
        """Calculate profile completion percentage."""
        fields_to_check = [
            'full_name', 'phone', 'location', 'bio', 'avatar_url'
        ]
        
        completed_fields = 0
        total_fields = len(fields_to_check)
        
        for field in fields_to_check:
            if getattr(user, field, None):
                completed_fields += 1
        
        # Add bonus for business users with company info
        if user.role == UserRole.BUSINESS:
            business_fields = ['company_name', 'company_org_number', 'company_address']
            for field in business_fields:
                if getattr(user, field, None):
                    completed_fields += 0.5
            total_fields += 1.5
        
        return int((completed_fields / total_fields) * 100)
    
    def update_user_rating(self, db: Session, user_id: int):
        """Update user's average rating and rating count."""
        from sqlalchemy import func
        
        # Calculate average rating and count
        result = db.query(
            func.avg(UserRating.rating).label('avg_rating'),
            func.count(UserRating.id).label('rating_count')
        ).filter(UserRating.rated_user_id == user_id).first()
        
        user = self.user_repo.get_by_id(db, user_id)
        if user:
            user.rating = float(result.avg_rating) if result.avg_rating else 0.0
            user.rating_count = result.rating_count if result.rating_count else 0
            db.commit()