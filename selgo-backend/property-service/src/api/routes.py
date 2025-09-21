from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from ..database.database import get_database
from ..services.property_services import PropertyCategoryService, PropertyService
from ..models.property_schemas import (
    PropertyCategoryResponse, PropertyResponse,
    PropertyCreate, PropertyUpdate, PropertyFilterParams, PaginatedResponse
)
from ..utils.auth import get_current_user_id
from .holiday_rental_routes import router as holiday_rental_router

router = APIRouter(prefix="/api/v1/properties", tags=["Properties"])

# Include holiday rental routes
router.include_router(holiday_rental_router, prefix="", tags=["Holiday Rentals"])

@router.get("/categories", response_model=List[PropertyCategoryResponse])
async def get_property_categories(
    db: Session = Depends(get_database)
):
    return PropertyCategoryService.get_all_categories(db)

@router.post("/filter", response_model=PaginatedResponse)
async def filter_properties(
    filters: PropertyFilterParams,
    db: Session = Depends(get_database)
):
    properties, total = PropertyService.filter_properties(db, filters)
    return PaginatedResponse(
        items=properties,
        total=total,
        limit=filters.limit,
        offset=filters.offset
    )

@router.get("/{property_id}", response_model=PropertyResponse)
async def get_property_detail(
    property_id: UUID,
    db: Session = Depends(get_database)
):
    property_obj = PropertyService.get_property_by_id(db, str(property_id), increment_view=True)
    
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    return property_obj

@router.post("", response_model=PropertyResponse)
async def create_property(
    property_data: PropertyCreate,
    db: Session = Depends(get_database),
    current_user_id: str = Depends(get_current_user_id)
):
    try:
        property_obj = PropertyService.create_property(db, property_data, current_user_id)
        return property_obj
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating property: {str(e)}"
        )

@router.put("/{property_id}", response_model=PropertyResponse)
async def update_property(
    property_id: UUID,
    property_data: PropertyUpdate,
    db: Session = Depends(get_database),
    current_user_id: str = Depends(get_current_user_id)
):
    property_obj = PropertyService.update_property(db, str(property_id), property_data, current_user_id)
    
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found or permission denied"
        )
    
    return property_obj

@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_property(
    property_id: UUID,
    db: Session = Depends(get_database),
    current_user_id: str = Depends(get_current_user_id)
):
    success = PropertyService.delete_property(db, str(property_id), current_user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found or permission denied"
        )
    return {"detail": "Property deleted successfully"}

# Finn.no-like enhanced features

@router.get("/{property_id}/similar", response_model=List[PropertyResponse])
async def get_similar_properties(
    property_id: UUID,
    limit: int = Query(6, ge=1, le=20),
    db: Session = Depends(get_database)
):
    """Get similar properties based on location, price, and type."""
    similar_properties = PropertyService.get_similar_properties(db, str(property_id), limit)
    return similar_properties

@router.post("/{property_id}/favorite")
async def toggle_property_favorite(
    property_id: UUID,
    db: Session = Depends(get_database),
    current_user_id: str = Depends(get_current_user_id)
):
    """Add or remove property from user's favorites."""
    is_favorited = PropertyService.toggle_favorite(db, str(property_id), current_user_id)
    return {"is_favorited": is_favorited, "message": "Favorite status updated"}

@router.get("/{property_id}/price-history")
async def get_property_price_history(
    property_id: UUID,
    db: Session = Depends(get_database)
):
    """Get price history for a property."""
    price_history = PropertyService.get_price_history(db, str(property_id))
    return {"price_history": price_history}

@router.get("/search/advanced", response_model=PaginatedResponse)
async def advanced_property_search(
    # Location filters
    city: Optional[str] = Query(None),
    postal_code: Optional[str] = Query(None),
    radius_km: Optional[float] = Query(None, ge=0.1, le=50),
    
    # Property type filters
    property_type: Optional[str] = Query(None),
    property_category: Optional[str] = Query(None),
    housing_type: Optional[str] = Query(None),
    
    # Size filters
    min_bedrooms: Optional[int] = Query(None, ge=0),
    max_bedrooms: Optional[int] = Query(None, ge=0),
    min_bathrooms: Optional[int] = Query(None, ge=0),
    max_bathrooms: Optional[int] = Query(None, ge=0),
    min_area: Optional[float] = Query(None, ge=0),
    max_area: Optional[float] = Query(None, ge=0),
    
    # Price filters
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    
    # Features
    has_balcony: Optional[bool] = Query(None),
    has_terrace: Optional[bool] = Query(None),
    has_parking: Optional[bool] = Query(None),
    has_garden: Optional[bool] = Query(None),
    is_furnished: Optional[bool] = Query(None),
    
    # Other filters
    year_built_from: Optional[int] = Query(None, ge=1800),
    year_built_to: Optional[int] = Query(None, le=2030),
    energy_rating: Optional[str] = Query(None),
    
    # Pagination and sorting
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    sort_by: Optional[str] = Query("created_at", regex="^(price|created_at|updated_at|area|bedrooms)$"),
    sort_order: Optional[str] = Query("desc", regex="^(asc|desc)$"),
    
    db: Session = Depends(get_database)
):
    """Advanced property search with multiple filters."""
    search_params = {
        "city": city,
        "postal_code": postal_code,
        "radius_km": radius_km,
        "property_type": property_type,
        "property_category": property_category,
        "housing_type": housing_type,
        "min_bedrooms": min_bedrooms,
        "max_bedrooms": max_bedrooms,
        "min_bathrooms": min_bathrooms,
        "max_bathrooms": max_bathrooms,
        "min_area": min_area,
        "max_area": max_area,
        "min_price": min_price,
        "max_price": max_price,
        "has_balcony": has_balcony,
        "has_terrace": has_terrace,
        "has_parking": has_parking,
        "has_garden": has_garden,
        "is_furnished": is_furnished,
        "year_built_from": year_built_from,
        "year_built_to": year_built_to,
        "energy_rating": energy_rating,
        "page": page,
        "limit": limit,
        "sort_by": sort_by,
        "sort_order": sort_order
    }
    
    properties, total = PropertyService.advanced_search(db, search_params)
    return PaginatedResponse(
        items=properties,
        total=total,
        limit=limit,
        offset=(page - 1) * limit
    )

@router.get("/statistics/market")
async def get_market_statistics(
    city: Optional[str] = Query(None),
    property_type: Optional[str] = Query(None),
    db: Session = Depends(get_database)
):
    """Get market statistics for properties."""
    stats = PropertyService.get_market_statistics(db, city, property_type)
    return stats

@router.get("/statistics/price-trends")
async def get_price_trends(
    city: Optional[str] = Query(None),
    months: int = Query(12, ge=1, le=60),
    db: Session = Depends(get_database)
):
    """Get price trends over time."""
    trends = PropertyService.get_price_trends(db, city, months)
    return {"trends": trends}

@router.post("/{property_id}/contact")
async def contact_property_owner(
    property_id: UUID,
    contact_data: dict,
    db: Session = Depends(get_database)
):
    """Send message to property owner."""
    success = PropertyService.send_contact_message(db, str(property_id), contact_data)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    return {"message": "Message sent successfully"}

@router.get("/featured", response_model=List[PropertyResponse])
async def get_featured_properties(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_database)
):
    """Get featured properties."""
    properties = PropertyService.get_featured_properties(db, limit)
    return properties

@router.get("/recent", response_model=List[PropertyResponse])
async def get_recent_properties(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_database)
):
    """Get recently added properties."""
    properties = PropertyService.get_recent_properties(db, limit)
    return properties

@router.get("/popular", response_model=List[PropertyResponse])
async def get_popular_properties(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_database)
):
    """Get most viewed properties."""
    properties = PropertyService.get_popular_properties(db, limit)
    return properties

@router.get("/map/bounds")
async def get_properties_in_bounds(
    north: float = Query(..., ge=-90, le=90),
    south: float = Query(..., ge=-90, le=90),
    east: float = Query(..., ge=-180, le=180),
    west: float = Query(..., ge=-180, le=180),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_database)
):
    """Get properties within map bounds for map view."""
    properties = PropertyService.get_properties_in_bounds(db, north, south, east, west, limit)
    return {"properties": properties}

@router.post("/{property_id}/report")
async def report_property(
    property_id: UUID,
    report_data: dict,
    db: Session = Depends(get_database),
    current_user_id: Optional[str] = Depends(get_current_user_id)
):
    """Report a property for inappropriate content."""
    success = PropertyService.report_property(db, str(property_id), report_data, current_user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    return {"message": "Property reported successfully"}

@router.get("/user/{user_id}", response_model=List[PropertyResponse])
async def get_user_properties(
    user_id: UUID,
    status: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_database)
):
    """Get properties by user ID."""
    properties = PropertyService.get_properties_by_user(db, str(user_id), status, limit, offset)
    return properties