from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from ..database.database import get_db
from ..services.auth_service import AuthService
from ..models.user_schemas import (
    UserCreate, UserResponse, UserProfileResponse, UserUpdate, LoginRequest, LoginResponse, 
    RefreshTokenRequest, TokenResponse, ChangePasswordRequest, TokenValidationResponse,
    NotificationPreferences, PrivacySettings, UserRatingCreate, UserRatingResponse,
    UserFavoriteCreate, UserFavoriteResponse, UserNotificationResponse, SavedSearchCreate, SavedSearchResponse
)
from ..utils.auth_utils import get_user_from_token
from ..config.config import settings
from ..models.user_models import User, UserRating, UserFavorite, UserNotification, SavedSearch

# Main auth router (existing)
router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])

# NEW: Separate router for user endpoints (no auth prefix)
user_router = APIRouter(prefix="/api/v1", tags=["users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/auth/token")

auth_service = AuthService()

# Existing auth routes
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    return auth_service.register_user(db, user_data)

@router.post("/login", response_model=LoginResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Login with username/email and password."""
    access_token, refresh_token, user = auth_service.authenticate_user(db, login_data)
    
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse.model_validate(user)  # Updated for Pydantic v2
    )

@router.post("/token", response_model=LoginResponse)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """OAuth2 compatible token endpoint."""
    login_data = LoginRequest(username=form_data.username, password=form_data.password)
    access_token, refresh_token, user = auth_service.authenticate_user(db, login_data)
    
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse.model_validate(user)  # Updated for Pydantic v2
    )

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(token_data: RefreshTokenRequest, db: Session = Depends(get_db)):
    """Refresh access token."""
    access_token = auth_service.refresh_access_token(db, token_data.refresh_token)
    return TokenResponse(
        access_token=access_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

@router.post("/logout")
def logout(token_data: RefreshTokenRequest, db: Session = Depends(get_db)):
    """Logout (revoke refresh token)."""
    success = auth_service.revoke_refresh_token(db, token_data.refresh_token)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid refresh token"
        )
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserResponse)
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Get current user information."""
    user_data = get_user_from_token(token)
    user = auth_service.user_repo.get_by_id(db, user_data["user_id"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserResponse.model_validate(user)  # Updated for Pydantic v2

@router.post("/change-password")
def change_password(
    password_data: ChangePasswordRequest,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Change user password."""
    user_data = get_user_from_token(token)
    success = auth_service.change_password(
        db, user_data["user_id"], 
        password_data.current_password, 
        password_data.new_password
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to change password"
        )
    return {"message": "Password changed successfully"}

# Token validation endpoint for other services
@router.post("/validate", response_model=TokenValidationResponse)
def validate_token(token: str = Depends(oauth2_scheme)):
    """Validate token and return user information. Used by other microservices."""
    user_data = get_user_from_token(token)
    return TokenValidationResponse(**user_data)

# MOVED: User endpoint to separate router with correct prefix
@user_router.get("/users/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID - for other microservices"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "phone": user.phone,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "role": user.role.value if hasattr(user, 'role') else "buyer"
        }
    except Exception as e:
        print(f"Error fetching user {user_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

# Enhanced User Profile Management
@router.get("/profile", response_model=UserProfileResponse)
def get_user_profile(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Get detailed user profile with all information."""
    user_data = get_user_from_token(token)
    user = auth_service.user_repo.get_by_id(db, user_data["user_id"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserProfileResponse.model_validate(user)

@router.put("/profile", response_model=UserResponse)
def update_user_profile(
    profile_data: UserUpdate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Update user profile information."""
    user_data = get_user_from_token(token)
    user = auth_service.user_repo.get_by_id(db, user_data["user_id"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update user fields
    for field, value in profile_data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    
    # Calculate profile completion
    completion = auth_service.calculate_profile_completion(user)
    user.profile_completion = completion
    
    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)

@router.put("/notifications", response_model=dict)
def update_notification_preferences(
    preferences: NotificationPreferences,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Update user notification preferences."""
    user_data = get_user_from_token(token)
    user = auth_service.user_repo.get_by_id(db, user_data["user_id"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.email_notifications = preferences.email_notifications
    user.sms_notifications = preferences.sms_notifications
    user.push_notifications = preferences.push_notifications
    user.marketing_emails = preferences.marketing_emails
    
    db.commit()
    return {"message": "Notification preferences updated successfully"}

@router.put("/privacy", response_model=dict)
def update_privacy_settings(
    privacy: PrivacySettings,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Update user privacy settings."""
    user_data = get_user_from_token(token)
    user = auth_service.user_repo.get_by_id(db, user_data["user_id"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.show_phone = privacy.show_phone
    user.show_email = privacy.show_email
    user.show_location = privacy.show_location
    
    db.commit()
    return {"message": "Privacy settings updated successfully"}

# User Rating System
@router.post("/ratings", response_model=UserRatingResponse, status_code=201)
def create_user_rating(
    rating_data: UserRatingCreate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Rate another user."""
    user_data = get_user_from_token(token)
    
    # Check if user is trying to rate themselves
    if user_data["user_id"] == rating_data.rated_user_id:
        raise HTTPException(status_code=400, detail="Cannot rate yourself")
    
    # Check if rated user exists
    rated_user = auth_service.user_repo.get_by_id(db, rating_data.rated_user_id)
    if not rated_user:
        raise HTTPException(status_code=404, detail="User to rate not found")
    
    # Create rating
    rating = UserRating(
        rater_id=user_data["user_id"],
        rated_user_id=rating_data.rated_user_id,
        rating=rating_data.rating,
        comment=rating_data.comment,
        transaction_id=rating_data.transaction_id
    )
    
    db.add(rating)
    db.commit()
    db.refresh(rating)
    
    # Update user's average rating
    auth_service.update_user_rating(db, rating_data.rated_user_id)
    
    return UserRatingResponse.model_validate(rating)

@router.get("/ratings/{user_id}", response_model=List[UserRatingResponse])
def get_user_ratings(user_id: int, db: Session = Depends(get_db)):
    """Get ratings for a specific user."""
    ratings = db.query(UserRating).filter(UserRating.rated_user_id == user_id).all()
    return [UserRatingResponse.model_validate(rating) for rating in ratings]

# Favorites System
@router.post("/favorites", response_model=UserFavoriteResponse, status_code=201)
def add_favorite(
    favorite_data: UserFavoriteCreate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Add item to user's favorites."""
    user_data = get_user_from_token(token)
    
    # Check if already favorited
    existing = db.query(UserFavorite).filter(
        UserFavorite.user_id == user_data["user_id"],
        UserFavorite.item_type == favorite_data.item_type,
        UserFavorite.item_id == favorite_data.item_id,
        UserFavorite.service_name == favorite_data.service_name
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Item already in favorites")
    
    favorite = UserFavorite(
        user_id=user_data["user_id"],
        item_type=favorite_data.item_type,
        item_id=favorite_data.item_id,
        service_name=favorite_data.service_name
    )
    
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    
    return UserFavoriteResponse.model_validate(favorite)

@router.get("/favorites", response_model=List[UserFavoriteResponse])
def get_user_favorites(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Get user's favorite items."""
    user_data = get_user_from_token(token)
    favorites = db.query(UserFavorite).filter(UserFavorite.user_id == user_data["user_id"]).all()
    return [UserFavoriteResponse.model_validate(fav) for fav in favorites]

@router.delete("/favorites/{favorite_id}")
def remove_favorite(
    favorite_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Remove item from favorites."""
    user_data = get_user_from_token(token)
    favorite = db.query(UserFavorite).filter(
        UserFavorite.id == favorite_id,
        UserFavorite.user_id == user_data["user_id"]
    ).first()
    
    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")
    
    db.delete(favorite)
    db.commit()
    return {"message": "Favorite removed successfully"}

# Notifications System
@router.get("/notifications", response_model=List[UserNotificationResponse])
def get_user_notifications(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
    unread_only: bool = False
):
    """Get user notifications."""
    user_data = get_user_from_token(token)
    query = db.query(UserNotification).filter(UserNotification.user_id == user_data["user_id"])
    
    if unread_only:
        query = query.filter(UserNotification.is_read == False)
    
    notifications = query.order_by(UserNotification.created_at.desc()).all()
    return [UserNotificationResponse.model_validate(notif) for notif in notifications]

@router.put("/notifications/{notification_id}/read")
def mark_notification_read(
    notification_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Mark notification as read."""
    user_data = get_user_from_token(token)
    notification = db.query(UserNotification).filter(
        UserNotification.id == notification_id,
        UserNotification.user_id == user_data["user_id"]
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.is_read = True
    db.commit()
    return {"message": "Notification marked as read"}

# Saved Searches
@router.post("/saved-searches", response_model=SavedSearchResponse, status_code=201)
def create_saved_search(
    search_data: SavedSearchCreate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Save a search for future use."""
    user_data = get_user_from_token(token)
    
    saved_search = SavedSearch(
        user_id=user_data["user_id"],
        search_name=search_data.search_name,
        service_name=search_data.service_name,
        search_criteria=search_data.search_criteria,
        email_alerts=search_data.email_alerts
    )
    
    db.add(saved_search)
    db.commit()
    db.refresh(saved_search)
    
    return SavedSearchResponse.model_validate(saved_search)

@router.get("/saved-searches", response_model=List[SavedSearchResponse])
def get_saved_searches(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Get user's saved searches."""
    user_data = get_user_from_token(token)
    searches = db.query(SavedSearch).filter(SavedSearch.user_id == user_data["user_id"]).all()
    return [SavedSearchResponse.model_validate(search) for search in searches]

@router.delete("/saved-searches/{search_id}")
def delete_saved_search(
    search_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Delete a saved search."""
    user_data = get_user_from_token(token)
    search = db.query(SavedSearch).filter(
        SavedSearch.id == search_id,
        SavedSearch.user_id == user_data["user_id"]
    ).first()
    
    if not search:
        raise HTTPException(status_code=404, detail="Saved search not found")
    
    db.delete(search)
    db.commit()
    return {"message": "Saved search deleted successfully"}