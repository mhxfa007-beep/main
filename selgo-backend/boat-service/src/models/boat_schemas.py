from pydantic import BaseModel, Field, validator, root_validator
from typing import List, Dict, Any, Union
from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID
from .boat_models import (
    BoatType, BoatCondition, HullMaterial, HullType, EngineType, 
    FuelType, PropulsionType, SellerType, AdType, MooringType, FixRequestStatus
)

# Pydantic models (schemas) for request and response validation

# Category schemas
class BoatCategoryBase(BaseModel):
    label: str
    icon: Union[str, None] = Field(default=None)
    parent_id: Union[int, None] = Field(default=None)

class BoatCategoryCreate(BoatCategoryBase):
    pass

class BoatCategoryResponse(BoatCategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class BoatCategoryWithCountResponse(BoatCategoryResponse):
    count: int = 0

class BoatCategoryNestedResponse(BoatCategoryResponse):
    children: List['BoatCategoryNestedResponse'] = []
    
    class Config:
        orm_mode = True

# Feature schemas
class BoatFeatureBase(BaseModel):
    name: str

class BoatFeatureCreate(BoatFeatureBase):
    pass

class BoatFeatureResponse(BoatFeatureBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

# Image schemas
class BoatImageBase(BaseModel):
    image_url: str
    is_primary: bool = False

class BoatImageCreate(BoatImageBase):
    pass

class BoatImageResponse(BoatImageBase):
    id: int
    boat_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

# Rating schemas
class BoatRatingBase(BaseModel):
    stars: int = Field(..., ge=1, le=5)
    review: Union[str, None] = Field(default=None)
    
    @validator('stars')
    def validate_stars(cls, v):
        if v < 1 or v > 5:
            raise ValueError('Rating must be between 1 and 5 stars')
        return v

class BoatRatingCreate(BoatRatingBase):
    boat_id: int

class BoatRatingResponse(BoatRatingBase):
    id: int
    boat_id: int
    user_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

# Fix Done Request schemas
class BoatFixDoneRequestBase(BaseModel):
    price: float
    message: Union[str, None] = Field(default=None)

class BoatFixDoneRequestCreate(BoatFixDoneRequestBase):
    boat_id: int

class BoatFixDoneRequestResponse(BoatFixDoneRequestBase):
    id: int
    boat_id: int
    buyer_id: int
    seller_id: int
    status: FixRequestStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class BoatFixDoneRequestStatusUpdate(BaseModel):
    status: FixRequestStatus

# Boat schemas
class GeoPoint(BaseModel):
    latitude: float
    longitude: float

class BoatBase(BaseModel):
    title: str
    description: Union[str, None] = Field(default=None)
    price: float
    category_id: int
    boat_type: Union[str, None] = Field(default=None)
    condition: Union[BoatCondition, None] = Field(default=None)
    year: Union[int, None] = Field(default=None)
    make: Union[str, None] = Field(default=None)
    model: Union[str, None] = Field(default=None)
    length: Union[float, None] = Field(default=None)
    beam: Union[float, None] = Field(default=None)
    draft: Union[float, None] = Field(default=None)
    fuel_type: Union[str, None] = Field(default=None)
    hull_material: Union[str, None] = Field(default=None)
    engine_make: Union[str, None] = Field(default=None)
    engine_model: Union[str, None] = Field(default=None)
    engine_hours: Union[int, None] = Field(default=None)
    engine_power: Union[int, None] = Field(default=None)
    seller_type: Union[SellerType, None] = Field(default=None)
    ad_type: Union[AdType, None] = Field(default=None)
    is_featured: bool = False
    location_name: Union[str, None] = Field(default=None)

class BoatCreate(BoatBase):
    location: Union[GeoPoint, None] = Field(default=None)
    features: List[int] = []  # List of feature IDs
    images: List[BoatImageCreate] = []

class BoatUpdate(BaseModel):
    title: Union[str, None] = Field(default=None)
    description: Union[str, None] = Field(default=None)
    price: Union[float, None] = Field(default=None)
    category_id: Union[int, None] = Field(default=None)
    condition: Union[BoatCondition, None] = Field(default=None)
    year: Union[int, None] = Field(default=None)
    make: Union[str, None] = Field(default=None)
    model: Union[str, None] = Field(default=None)
    length: Union[float, None] = Field(default=None)
    beam: Union[float, None] = Field(default=None)
    draft: Union[float, None] = Field(default=None)
    fuel_type: Union[str, None] = Field(default=None)
    hull_material: Union[str, None] = Field(default=None)
    engine_make: Union[str, None] = Field(default=None)
    engine_model: Union[str, None] = Field(default=None)
    engine_hours: Union[int, None] = Field(default=None)
    engine_power: Union[int, None] = Field(default=None)
    seller_type: Union[SellerType, None] = Field(default=None)
    ad_type: Union[AdType, None] = Field(default=None)
    is_featured: Union[bool, None] = Field(default=None)
    location: Union[GeoPoint, None] = Field(default=None)
    location_name: Union[str, None] = Field(default=None)
    features: Union[List[int, None]] = None  # List of feature IDs

class BoatResponse(BoatBase):
    id: int
    status: str
    user_id: int
    view_count: int
    created_at: datetime
    updated_at: datetime
    location: Union[GeoPoint, None] = Field(default=None)
    category: BoatCategoryResponse
    images: List[BoatImageResponse] = []
    features: List[BoatFeatureResponse] = []
    
    class Config:
        orm_mode = True

class BoatListResponse(BaseModel):
    id: int
    title: str
    price: float
    location_name: Union[str, None] = Field(default=None)
    year: Union[int, None] = Field(default=None)
    make: Union[str, None] = Field(default=None)
    model: Union[str, None] = Field(default=None)
    length: Union[float, None] = Field(default=None)
    created_at: datetime
    primary_image: Union[str, None] = Field(default=None)
    
    class Config:
        orm_mode = True

class BoatDetailResponse(BoatResponse):
    fix_requests: List[BoatFixDoneRequestResponse] = []
    ratings: List[BoatRatingResponse] = []
    avg_rating: Union[float, None] = Field(default=None)
    
    class Config:
        orm_mode = True

# Loan Estimation schemas
class LoanEstimateRequest(BaseModel):
    price: float
    duration: int = Field(..., description="Loan term in months")
    interest_rate: Union[float, None] = Field(default=None)  # Annual interest rate, e.g., 5.5% = 5.5

class LoanEstimateResponse(BaseModel):
    monthly_payment: float
    total_interest: float
    total_payable: float
    breakdown: Dict[str, Any]  # Monthly breakdown

# Filter schemas
class BoatFilterParams(BaseModel):
    category_id: Union[int, None] = Field(default=None)
    boat_type: Union[str, None] = Field(default=None)  
    boat_types: Union[List[str, None]] = None  # ✅ ADDED: Support for multiple boat types
    condition: Union[BoatCondition, None] = Field(default=None)
    price_min: Union[float, None] = Field(default=None)
    price_max: Union[float, None] = Field(default=None)
    year_min: Union[int, None] = Field(default=None)
    year_max: Union[int, None] = Field(default=None)
    length_min: Union[float, None] = Field(default=None)
    length_max: Union[float, None] = Field(default=None)
    location: Union[GeoPoint, None] = Field(default=None)
    distance: Union[float, None] = Field(default=None)
    seller_type: Union[SellerType, None] = Field(default=None)
    ad_type: Union[AdType, None] = Field(default=None)
    features: Union[List[int, None]] = None
    search_term: Union[str, None] = Field(default=None)
    sort_by: Union[str, None] = "created_at"
    sort_order: Union[str, None] = "desc"
    limit: int = 10
    offset: int = 0

class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    limit: int
    offset: int

# Favorite schemas
class UserFavoriteCreate(BaseModel):
    boat_id: int
    
class FavoriteBoatInfo(BaseModel):
    id: int
    title: str
    price: float
    location_name: Union[str, None] = Field(default=None)
    year: Union[int, None] = Field(default=None)
    make: Union[str, None] = Field(default=None)
    model: Union[str, None] = Field(default=None)
    length: Union[float, None] = Field(default=None)
    created_at: str  # Use string instead of datetime for JSON compatibility
    primary_image: Union[str, None] = Field(default=None)
    
class UserFavoriteSimple(BaseModel):
    id: int
    user_id: int
    boat_id: int
    created_at: str  # Use string instead of datetime for JSON compatibility
    boat: FavoriteBoatInfo

class UserFavoriteResponse(BaseModel):
    id: int
    user_id: int
    boat_id: int
    created_at: datetime
    boat: BoatListResponse
    
    class Config:
        orm_mode = True

class FavoriteToggleResponse(BaseModel):
    is_favorite: bool
    message: str

# Enhanced Boat Schemas with Finn.no marine features

class BoatSpecificationBase(BaseModel):
    # Detailed Engine Specifications
    engine_configuration: Union[str, None] = Field(default=None, max_length=100)
    engine_displacement: Union[float, None] = Field(default=None, ge=0)
    engine_cooling: Union[str, None] = Field(default=None, max_length=50)
    transmission: Union[str, None] = Field(default=None, max_length=100)
    propeller_type: Union[str, None] = Field(default=None, max_length=100)
    propeller_material: Union[str, None] = Field(default=None, max_length=50)
    
    # Electrical System
    electrical_system: Union[str, None] = Field(default=None, max_length=50)
    battery_capacity: Union[str, None] = Field(default=None, max_length=50)
    shore_power: Union[str, None] = Field(default=None, max_length=50)
    generator: Union[str, None] = Field(default=None, max_length=100)
    inverter: Union[str, None] = Field(default=None, max_length=100)
    
    # Plumbing and Water Systems
    fresh_water_system: Union[str, None] = Field(default=None, max_length=200)
    hot_water_system: Union[str, None] = Field(default=None, max_length=200)
    waste_system: Union[str, None] = Field(default=None, max_length=200)
    bilge_pumps: Union[str, None] = Field(default=None, max_length=200)
    
    # Heating and Cooling
    heating_system: Union[str, None] = Field(default=None, max_length=200)
    air_conditioning: Union[str, None] = Field(default=None, max_length=200)
    
    # Construction Details
    construction_method: Union[str, None] = Field(default=None, max_length=200)
    deck_material: Union[str, None] = Field(default=None, max_length=100)
    interior_material: Union[str, None] = Field(default=None, max_length=100)
    
    # Performance Data
    max_speed: Union[float, None] = Field(default=None, ge=0)
    cruise_speed: Union[float, None] = Field(default=None, ge=0)
    fuel_consumption: Union[float, None] = Field(default=None, ge=0)
    range_nautical_miles: Union[int, None] = Field(default=None, ge=0)

class BoatSpecificationCreate(BoatSpecificationBase):
    boat_id: UUID

class BoatSpecification(BoatSpecificationBase):
    id: UUID
    boat_id: UUID
    created_at: datetime
    updated_at: Union[datetime, None] = Field(default=None)
    
    class Config:
        from_attributes = True

class BoatInspectionBase(BaseModel):
    inspection_date: datetime
    inspection_type: Union[str, None] = Field(default=None, max_length=50)
    surveyor_name: Union[str, None] = Field(default=None, max_length=100)
    surveyor_certification: Union[str, None] = Field(default=None, max_length=100)
    
    # Inspection Results
    overall_condition: Union[str, None] = Field(default=None, max_length=20)
    hull_condition: Union[str, None] = Field(default=None, max_length=20)
    engine_condition: Union[str, None] = Field(default=None, max_length=20)
    electrical_condition: Union[str, None] = Field(default=None, max_length=20)
    plumbing_condition: Union[str, None] = Field(default=None, max_length=20)
    safety_equipment_condition: Union[str, None] = Field(default=None, max_length=20)
    
    # Detailed Findings
    findings: Union[str, None] = Field(default=None)
    recommendations: Union[str, None] = Field(default=None)
    estimated_repair_cost: Union[Decimal, None] = Field(default=None, ge=0)
    estimated_value: Union[Decimal, None] = Field(default=None, ge=0)
    
    # Documentation
    report_url: Union[str, None] = Field(default=None, max_length=500)
    images: Union[List[str], None] = Field(default_factory=list)
    
    is_passed: Union[bool, None] = Field(default=None)
    valid_until: Union[datetime, None] = Field(default=None)

class BoatInspectionCreate(BoatInspectionBase):
    boat_id: UUID

class BoatInspection(BoatInspectionBase):
    id: UUID
    boat_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True

class BoatAlertCreate(BaseModel):
    alert_name: str = Field(max_length=200)
    boat_type: Union[str, None] = Field(default=None, max_length=100)
    make: Union[str, None] = Field(default=None, max_length=100)
    model: Union[str, None] = Field(default=None, max_length=100)
    price_min: Union[Decimal, None] = Field(default=None, ge=0)
    price_max: Union[Decimal, None] = Field(default=None, ge=0)
    year_min: Union[int, None] = Field(default=None, ge=1900, le=2030)
    year_max: Union[int, None] = Field(default=None, ge=1900, le=2030)
    length_min: Union[float, None] = Field(default=None, ge=0)
    length_max: Union[float, None] = Field(default=None, ge=0)
    engine_power_min: Union[int, None] = Field(default=None, ge=0)
    engine_power_max: Union[int, None] = Field(default=None, ge=0)
    city: Union[str, None] = Field(default=None, max_length=100)
    radius_km: int = Field(default=50, ge=1, le=500)
    
    # Alert settings
    email_notifications: bool = Field(default=True)
    push_notifications: bool = Field(default=True)
    frequency: str = Field(default='immediate', regex='^(immediate|daily|weekly)$')

class BoatAlert(BaseModel):
    id: UUID
    user_id: UUID
    alert_name: str
    boat_type: Union[str, None] = Field(default=None)
    make: Union[str, None] = Field(default=None)
    model: Union[str, None] = Field(default=None)
    price_min: Union[Decimal, None] = Field(default=None)
    price_max: Union[Decimal, None] = Field(default=None)
    year_min: Union[int, None] = Field(default=None)
    year_max: Union[int, None] = Field(default=None)
    length_min: Union[float, None] = Field(default=None)
    length_max: Union[float, None] = Field(default=None)
    engine_power_min: Union[int, None] = Field(default=None)
    engine_power_max: Union[int, None] = Field(default=None)
    city: Union[str, None] = Field(default=None)
    radius_km: int
    
    is_active: bool
    email_notifications: bool
    push_notifications: bool
    frequency: str
    
    matches_found: int
    last_match_date: Union[datetime, None] = Field(default=None)
    
    created_at: datetime
    updated_at: Union[datetime, None] = Field(default=None)
    
    class Config:
        from_attributes = True

class BoatComparisonCreate(BaseModel):
    boat_ids: List[str] = Field(min_items=2, max_items=5)
    comparison_name: Union[str, None] = Field(default=None, max_length=200)
    is_public: bool = Field(default=False)

class BoatComparison(BaseModel):
    id: UUID
    user_id: Union[UUID, None] = Field(default=None)
    session_id: Union[str, None] = Field(default=None)
    boat_ids: List[str]
    comparison_name: Union[str, None] = Field(default=None)
    is_public: bool
    created_at: datetime
    updated_at: Union[datetime, None] = Field(default=None)
    
    class Config:
        from_attributes = True

class BoatReportCreate(BaseModel):
    boat_id: UUID
    report_type: str = Field(regex='^(fraud|inappropriate|spam|sold)$')
    reason: Union[str, None] = Field(default=None, max_length=200)
    description: Union[str, None] = Field(default=None)
    evidence_urls: Union[List[str], None] = Field(default_factory=list)

class BoatReport(BaseModel):
    id: UUID
    boat_id: UUID
    reporter_id: Union[UUID, None] = Field(default=None)
    report_type: str
    reason: Union[str, None] = Field(default=None)
    description: Union[str, None] = Field(default=None)
    evidence_urls: Union[List[str], None] = Field(default=None)
    status: str
    admin_notes: Union[str, None] = Field(default=None)
    resolved_by: Union[UUID, None] = Field(default=None)
    resolved_at: Union[datetime, None] = Field(default=None)
    created_at: datetime
    
    class Config:
        from_attributes = True

class MarinaBase(BaseModel):
    name: str = Field(max_length=200)
    description: Union[str, None] = Field(default=None)
    website: Union[str, None] = Field(default=None, max_length=500)
    phone: Union[str, None] = Field(default=None, max_length=50)
    email: Union[str, None] = Field(default=None, max_length=200)
    
    # Location
    address: Union[str, None] = Field(default=None, max_length=500)
    city: Union[str, None] = Field(default=None, max_length=100)
    postal_code: Union[str, None] = Field(default=None, max_length=20)
    country: Union[str, None] = Field(default=None, max_length=100)
    
    # Marina Details
    total_berths: Union[int, None] = Field(default=None, ge=0)
    available_berths: Union[int, None] = Field(default=None, ge=0)
    max_boat_length: Union[float, None] = Field(default=None, ge=0)
    max_draft: Union[float, None] = Field(default=None, ge=0)
    
    # Facilities and Services
    facilities: Union[List[str], None] = Field(default_factory=list)
    services: Union[List[str], None] = Field(default_factory=list)
    
    # Pricing
    daily_rate: Union[Decimal, None] = Field(default=None, ge=0)
    weekly_rate: Union[Decimal, None] = Field(default=None, ge=0)
    monthly_rate: Union[Decimal, None] = Field(default=None, ge=0)
    annual_rate: Union[Decimal, None] = Field(default=None, ge=0)

class MarinaCreate(MarinaBase):
    pass

class Marina(MarinaBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: Union[datetime, None] = Field(default=None)
    
    class Config:
        from_attributes = True

class AdvancedBoatSearchFilters(BaseModel):
    # Basic filters
    category_id: Union[int, None] = Field(default=None)
    boat_type: Union[str, None] = Field(default=None)
    make: Union[str, None] = Field(default=None)
    model: Union[str, None] = Field(default=None)
    condition: Union[str, None] = Field(default=None)
    seller_type: Union[str, None] = Field(default=None)
    ad_type: Union[str, None] = Field(default=None)
    
    # Price and year
    price_min: Union[Decimal, None] = Field(default=None, ge=0)
    price_max: Union[Decimal, None] = Field(default=None, ge=0)
    year_min: Union[int, None] = Field(default=None, ge=1900, le=2030)
    year_max: Union[int, None] = Field(default=None, ge=1900, le=2030)
    
    # Physical specifications
    length_min: Union[float, None] = Field(default=None, ge=0)
    length_max: Union[float, None] = Field(default=None, ge=0)
    beam_min: Union[float, None] = Field(default=None, ge=0)
    beam_max: Union[float, None] = Field(default=None, ge=0)
    draft_min: Union[float, None] = Field(default=None, ge=0)
    draft_max: Union[float, None] = Field(default=None, ge=0)
    
    # Engine and performance
    engine_type: Union[str, None] = Field(default=None)
    fuel_type: Union[str, None] = Field(default=None)
    engine_power_min: Union[int, None] = Field(default=None, ge=0)
    engine_power_max: Union[int, None] = Field(default=None, ge=0)
    engine_hours_max: Union[int, None] = Field(default=None, ge=0)
    
    # Hull specifications
    hull_material: Union[str, None] = Field(default=None)
    hull_type: Union[str, None] = Field(default=None)
    
    # Accommodation
    berths_min: Union[int, None] = Field(default=None, ge=0)
    cabins_min: Union[int, None] = Field(default=None, ge=0)
    heads_min: Union[int, None] = Field(default=None, ge=0)
    
    # History and documentation
    max_owners: Union[int, None] = Field(default=None, ge=1)
    service_history_required: Union[bool, None] = Field(default=None)
    recent_survey_required: Union[bool, None] = Field(default=None)
    vat_paid_required: Union[bool, None] = Field(default=None)
    ce_certification_required: Union[bool, None] = Field(default=None)
    
    # Location
    city: Union[str, None] = Field(default=None)
    country: Union[str, None] = Field(default=None)
    radius_km: Union[int, None] = Field(default=50, ge=1, le=500)
    
    # Mooring
    mooring_included: Union[bool, None] = Field(default=None)
    mooring_type: Union[str, None] = Field(default=None)
    
    # Status
    include_sold: bool = Field(default=False)
    featured_only: bool = Field(default=False)
    
    # Search term
    search_term: Union[str, None] = Field(default=None, max_length=200)
    
    # Sorting
    sort_by: str = Field(default='created_at', regex='^(created_at|price|year|length_overall|views_count)$')
    sort_order: str = Field(default='desc', regex='^(asc|desc)$')

class EnhancedBoatResponse(BaseModel):
    # Basic boat info
    id: UUID
    title: str
    description: Union[str, None] = Field(default=None)
    price: Decimal
    original_price: Union[Decimal, None] = Field(default=None)
    negotiable: bool
    
    # Classification
    boat_type: str
    condition: str
    year: Union[int, None] = Field(default=None)
    make: Union[str, None] = Field(default=None)
    model: Union[str, None] = Field(default=None)
    
    # Physical specifications
    length_overall: Union[float, None] = Field(default=None)
    beam: Union[float, None] = Field(default=None)
    draft: Union[float, None] = Field(default=None)
    displacement: Union[int, None] = Field(default=None)
    
    # Hull specifications
    hull_material: Union[str, None] = Field(default=None)
    hull_type: Union[str, None] = Field(default=None)
    
    # Engine specifications
    engine_type: Union[str, None] = Field(default=None)
    fuel_type: Union[str, None] = Field(default=None)
    engine_power: Union[int, None] = Field(default=None)
    engine_hours: Union[int, None] = Field(default=None)
    number_of_engines: Union[int, None] = Field(default=None)
    
    # Accommodation
    berths: Union[int, None] = Field(default=None)
    cabins: Union[int, None] = Field(default=None)
    heads: Union[int, None] = Field(default=None)
    
    # Equipment and features
    navigation_equipment: Union[List[str], None] = Field(default_factory=list)
    safety_equipment: Union[List[str], None] = Field(default_factory=list)
    comfort_features: Union[List[str], None] = Field(default_factory=list)
    
    # Location and mooring
    current_location: Union[str, None] = Field(default=None)
    city: Union[str, None] = Field(default=None)
    country: Union[str, None] = Field(default=None)
    mooring_type: Union[str, None] = Field(default=None)
    mooring_included: bool
    
    # Legal and documentation
    registration_number: Union[str, None] = Field(default=None)
    vat_paid: bool
    ce_certification: bool
    
    # History
    previous_owners: Union[int, None] = Field(default=None)
    service_history: bool
    recent_survey: bool
    
    # Commercial information
    seller_type: str
    ad_type: str
    
    # Status
    is_active: bool
    is_featured: bool
    is_sold: bool
    views_count: int
    favorites_count: int
    
    # Relationships
    category: Union[BoatCategoryResponse, None] = Field(default=None)
    images: List[BoatImageResponse] = Field(default_factory=list)
    specifications: Union[List[BoatSpecification], None] = Field(default_factory=list)
    inspections: Union[List[BoatInspection], None] = Field(default_factory=list)
    
    # Timestamps
    created_at: datetime
    updated_at: Union[datetime, None] = Field(default=None)
    
    class Config:
        from_attributes = True

# Update the forward references
BoatCategoryNestedResponse.update_forward_refs()
