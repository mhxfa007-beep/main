# selgo-backend/motorcycle-service/src/models/schemas.py

from pydantic import BaseModel, validator, Field
from typing import List, Union, Dict, Any
from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID

class MotorcycleType(str, Enum):
    ADVENTURE = "adventure"
    NAKED = "naked"
    TOURING = "touring"
    SPORTS = "sports"
    SUPERSPORT = "supersport"
    CRUISER = "cruiser"
    SCOOTER = "scooter"
    CHOPPER = "chopper"
    ENDURO = "enduro"
    MOTOCROSS = "motocross"
    CAFE_RACER = "cafe_racer"
    BOBBER = "bobber"
    STREETFIGHTER = "streetfighter"
    DUAL_SPORT = "dual_sport"

class EngineType(str, Enum):
    SINGLE_CYLINDER = "single_cylinder"
    PARALLEL_TWIN = "parallel_twin"
    V_TWIN = "v_twin"
    INLINE_THREE = "inline_three"
    INLINE_FOUR = "inline_four"
    V_FOUR = "v_four"
    FLAT_TWIN = "flat_twin"
    TRIPLE = "triple"

class TransmissionType(str, Enum):
    MANUAL = "manual"
    AUTOMATIC = "automatic"
    CVT = "cvt"
    SEMI_AUTOMATIC = "semi_automatic"

class FuelType(str, Enum):
    GASOLINE = "gasoline"
    ELECTRIC = "electric"
    HYBRID = "hybrid"

class DriveType(str, Enum):
    CHAIN = "chain"
    BELT = "belt"
    SHAFT = "shaft"

class ConditionEnum(str, Enum):
    NEW = "new"
    LIKE_NEW = "like_new"
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    PROJECT_BIKE = "project_bike"

class SellerTypeEnum(str, Enum):
    PRIVATE = "private"
    DEALER = "dealer"

# Add SellerInfo schema for external user data
class SellerInfo(BaseModel):
    id: int
    name: Union[str, None] = Field(default=None)
    email: Union[str, None] = Field(default=None)
    phone: Union[str, None] = Field(default=None)
    created_at: Union[datetime, None] = Field(default=None)
    
    class Config:
        from_attributes = True

# Base schemas
class MotorcycleCategoryBase(BaseModel):
    name: str
    slug: str
    icon: Union[str, None] = Field(default=None)
    description: Union[str, None] = Field(default=None)

class MotorcycleCategoryCreate(MotorcycleCategoryBase):
    pass

class MotorcycleCategory(MotorcycleCategoryBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class MotorcycleImageBase(BaseModel):
    image_url: str
    is_primary: bool = False
    alt_text: Union[str, None] = Field(default=None)

class MotorcycleImageCreate(MotorcycleImageBase):
    pass

class MotorcycleImage(MotorcycleImageBase):
    id: int
    motorcycle_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class MotorcycleBase(BaseModel):
    title: str
    description: Union[str, None] = Field(default=None)
    brand: str
    model: str
    year: int
    engine_size: Union[int, None] = Field(default=None)
    mileage: Union[int, None] = Field(default=None)
    price: Decimal
    condition: ConditionEnum
    motorcycle_type: MotorcycleType
    seller_type: SellerTypeEnum = SellerTypeEnum.PRIVATE
    city: Union[str, None] = Field(default=None)
    address: Union[str, None] = Field(default=None)
    netbill: bool = False

class MotorcycleCreate(MotorcycleBase):
    category_id: int
    seller_id: int
    images: Union[List[MotorcycleImageCreate], None] = Field(default_factory=list)

class MotorcycleUpdate(BaseModel):
    title: Union[str, None] = Field(default=None)
    description: Union[str, None] = Field(default=None)
    brand: Union[str, None] = Field(default=None)
    model: Union[str, None] = Field(default=None)
    year: Union[int, None] = Field(default=None)
    engine_size: Union[int, None] = Field(default=None)
    mileage: Union[int, None] = Field(default=None)
    price: Union[Decimal, None] = Field(default=None)
    condition: Union[ConditionEnum, None] = Field(default=None)
    motorcycle_type: Union[MotorcycleType, None] = Field(default=None)
    seller_type: Union[SellerTypeEnum, None] = Field(default=None)
    city: Union[str, None] = Field(default=None)
    address: Union[str, None] = Field(default=None)
    netbill: Union[bool, None] = Field(default=None)
    is_featured: Union[bool, None] = Field(default=None)

class Motorcycle(MotorcycleBase):
    id: int
    category_id: int
    seller_id: int
    is_active: bool
    is_featured: bool
    views_count: int
    created_at: datetime
    updated_at: Union[datetime, None] = Field(default=None)
    
    category: Union[MotorcycleCategory, None] = Field(default=None)
    seller: Union[SellerInfo, None] = Field(default=None)
    images: List[MotorcycleImage] = []
    
    class Config:
        from_attributes = True

class MotorcycleListResponse(BaseModel):
    id: int
    title: str
    brand: str
    model: str
    year: int
    price: Decimal
    condition: ConditionEnum
    motorcycle_type: MotorcycleType
    city: Union[str, None] = Field(default=None)
    is_featured: bool
    views_count: int
    created_at: datetime
    primary_image: Union[str, None] = Field(default=None)
    
    class Config:
        from_attributes = True

class MotorcycleSearchFilters(BaseModel):
    category_id: Union[int, None] = Field(default=None)
    category_name: Union[str, None] = Field(default=None)
    motorcycle_type: Union[MotorcycleType, None] = Field(default=None)
    brand: Union[str, None] = Field(default=None)
    model: Union[str, None] = Field(default=None)
    city: Union[str, None] = Field(default=None)
    condition: Union[ConditionEnum, None] = Field(default=None)
    seller_type: Union[SellerTypeEnum, None] = Field(default=None)
    price_min: Union[Decimal, None] = Field(default=None)
    price_max: Union[Decimal, None] = Field(default=None)
    year_min: Union[int, None] = Field(default=None)
    year_max: Union[int, None] = Field(default=None)
    mileage_min: Union[int, None] = Field(default=None)
    mileage_max: Union[int, None] = Field(default=None)
    engine_size_min: Union[int, None] = Field(default=None)
    engine_size_max: Union[int, None] = Field(default=None)
    search_term: Union[str, None] = Field(default=None)

class MapFilterRequest(BaseModel):
    latitude: float
    longitude: float
    radius_km: int = 50
    filters: Union[MotorcycleSearchFilters, None] = Field(default=None)

class LoanCalculationRequest(BaseModel):
    price: Decimal
    term_months: int = 36
    interest_rate: Union[Decimal, None] = Field(default=None)

class LoanCalculationResponse(BaseModel):
    price: Decimal
    term_months: int
    interest_rate: Decimal
    monthly_payment: Decimal
    total_amount: Decimal
    total_interest: Decimal

class PaginatedResponse(BaseModel):
    items: List[MotorcycleListResponse]
    total: int
    page: int
    per_page: int
    pages: int
    has_next: bool
    has_prev: bool
    
class UserFavoriteMotorcycleCreate(BaseModel):
    motorcycle_id: int

class FavoriteMotorcycleInfo(BaseModel):
    id: int
    title: str
    brand: str
    model: str
    year: int
    price: Decimal
    city: Union[str, None] = Field(default=None)
    motorcycle_type: MotorcycleType
    condition: ConditionEnum
    created_at: str  # Use string for JSON compatibility
    primary_image: Union[str, None] = Field(default=None)

class UserFavoriteMotorcycleResponse(BaseModel):
    id: int
    user_id: int
    motorcycle_id: int
    created_at: str  # Use string for JSON compatibility
    motorcycle: FavoriteMotorcycleInfo

class FavoriteToggleResponse(BaseModel):
    is_favorite: bool
    message: str

# Enhanced Motorcycle Schemas with Finn.no features

class MotorcycleSpecificationBase(BaseModel):
    # Detailed Engine Specs
    engine_configuration: Union[str, None] = Field(default=None, max_length=100)
    bore_stroke: Union[str, None] = Field(default=None, max_length=50)
    compression_ratio: Union[str, None] = Field(default=None, max_length=20)
    valve_system: Union[str, None] = Field(default=None, max_length=100)
    
    # Electrical System
    ignition_system: Union[str, None] = Field(default=None, max_length=100)
    starting_system: Union[str, None] = Field(default=None, max_length=50)
    battery: Union[str, None] = Field(default=None, max_length=50)
    
    # Suspension
    front_suspension: Union[str, None] = Field(default=None, max_length=200)
    rear_suspension: Union[str, None] = Field(default=None, max_length=200)
    front_travel: Union[int, None] = Field(default=None, ge=0, le=500)
    rear_travel: Union[int, None] = Field(default=None, ge=0, le=500)
    
    # Brakes
    front_brake: Union[str, None] = Field(default=None, max_length=200)
    rear_brake: Union[str, None] = Field(default=None, max_length=200)
    brake_assist: bool = Field(default=False)
    
    # Wheels and Tires
    front_tire: Union[str, None] = Field(default=None, max_length=50)
    rear_tire: Union[str, None] = Field(default=None, max_length=50)
    front_rim: Union[str, None] = Field(default=None, max_length=50)
    rear_rim: Union[str, None] = Field(default=None, max_length=50)
    
    # Colors and Options
    available_colors: Union[List[str], None] = Field(default_factory=list)
    optional_equipment: Union[List[str], None] = Field(default_factory=list)

class MotorcycleSpecificationCreate(MotorcycleSpecificationBase):
    motorcycle_id: UUID

class MotorcycleSpecification(MotorcycleSpecificationBase):
    id: UUID
    motorcycle_id: UUID
    created_at: datetime
    updated_at: Union[datetime, None] = Field(default=None)
    
    class Config:
        from_attributes = True

class MotorcycleInspectionBase(BaseModel):
    inspection_date: datetime
    inspection_type: Union[str, None] = Field(default=None, max_length=50)
    inspector_name: Union[str, None] = Field(default=None, max_length=100)
    inspector_certification: Union[str, None] = Field(default=None, max_length=100)
    
    # Inspection Results
    overall_condition: Union[str, None] = Field(default=None, max_length=20)
    engine_condition: Union[str, None] = Field(default=None, max_length=20)
    transmission_condition: Union[str, None] = Field(default=None, max_length=20)
    brake_condition: Union[str, None] = Field(default=None, max_length=20)
    tire_condition: Union[str, None] = Field(default=None, max_length=20)
    electrical_condition: Union[str, None] = Field(default=None, max_length=20)
    
    # Detailed Findings
    findings: Union[str, None] = Field(default=None)
    recommendations: Union[str, None] = Field(default=None)
    estimated_repair_cost: Union[Decimal, None] = Field(default=None, ge=0)
    
    # Documentation
    report_url: Union[str, None] = Field(default=None, max_length=500)
    images: Union[List[str], None] = Field(default_factory=list)
    
    is_passed: Union[bool, None] = Field(default=None)
    valid_until: Union[datetime, None] = Field(default=None)

class MotorcycleInspectionCreate(MotorcycleInspectionBase):
    motorcycle_id: UUID

class MotorcycleInspection(MotorcycleInspectionBase):
    id: UUID
    motorcycle_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True

class MotorcycleComparisonCreate(BaseModel):
    motorcycle_ids: List[str] = Field(min_items=2, max_items=5)
    comparison_name: Union[str, None] = Field(default=None, max_length=200)
    is_public: bool = Field(default=False)

class MotorcycleComparison(BaseModel):
    id: UUID
    user_id: Union[UUID, None] = Field(default=None)
    session_id: Union[str, None] = Field(default=None)
    motorcycle_ids: List[str]
    comparison_name: Union[str, None] = Field(default=None)
    is_public: bool
    created_at: datetime
    updated_at: Union[datetime, None] = Field(default=None)
    
    class Config:
        from_attributes = True

class MotorcycleAlertCreate(BaseModel):
    alert_name: str = Field(max_length=200)
    brand: Union[str, None] = Field(default=None, max_length=100)
    model: Union[str, None] = Field(default=None, max_length=100)
    motorcycle_type: Union[MotorcycleType, None] = Field(default=None)
    price_min: Union[Decimal, None] = Field(default=None, ge=0)
    price_max: Union[Decimal, None] = Field(default=None, ge=0)
    year_min: Union[int, None] = Field(default=None, ge=1900, le=2030)
    year_max: Union[int, None] = Field(default=None, ge=1900, le=2030)
    mileage_max: Union[int, None] = Field(default=None, ge=0)
    engine_size_min: Union[int, None] = Field(default=None, ge=0)
    engine_size_max: Union[int, None] = Field(default=None, ge=0)
    city: Union[str, None] = Field(default=None, max_length=100)
    radius_km: int = Field(default=50, ge=1, le=500)
    
    # Alert settings
    email_notifications: bool = Field(default=True)
    push_notifications: bool = Field(default=True)
    frequency: str = Field(default='immediate', regex='^(immediate|daily|weekly)$')

class MotorcycleAlert(BaseModel):
    id: UUID
    user_id: UUID
    alert_name: str
    brand: Union[str, None] = Field(default=None)
    model: Union[str, None] = Field(default=None)
    motorcycle_type: Union[str, None] = Field(default=None)
    price_min: Union[Decimal, None] = Field(default=None)
    price_max: Union[Decimal, None] = Field(default=None)
    year_min: Union[int, None] = Field(default=None)
    year_max: Union[int, None] = Field(default=None)
    mileage_max: Union[int, None] = Field(default=None)
    engine_size_min: Union[int, None] = Field(default=None)
    engine_size_max: Union[int, None] = Field(default=None)
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

class MotorcycleReportCreate(BaseModel):
    motorcycle_id: UUID
    report_type: str = Field(regex='^(fraud|inappropriate|spam|sold)$')
    reason: Union[str, None] = Field(default=None, max_length=200)
    description: Union[str, None] = Field(default=None)
    evidence_urls: Union[List[str], None] = Field(default_factory=list)

class MotorcycleReport(BaseModel):
    id: UUID
    motorcycle_id: UUID
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

class MotorcycleMarketStats(BaseModel):
    id: UUID
    brand: Union[str, None] = Field(default=None)
    model: Union[str, None] = Field(default=None)
    year: Union[int, None] = Field(default=None)
    motorcycle_type: Union[str, None] = Field(default=None)
    engine_size_range: Union[str, None] = Field(default=None)
    
    average_price: Union[Decimal, None] = Field(default=None)
    median_price: Union[Decimal, None] = Field(default=None)
    min_price: Union[Decimal, None] = Field(default=None)
    max_price: Union[Decimal, None] = Field(default=None)
    price_trend: Union[str, None] = Field(default=None)
    
    listings_count: Union[int, None] = Field(default=None)
    sold_count: Union[int, None] = Field(default=None)
    average_days_on_market: Union[int, None] = Field(default=None)
    
    city: Union[str, None] = Field(default=None)
    region: Union[str, None] = Field(default=None)
    
    period_start: datetime
    period_end: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

class EnhancedMotorcycleResponse(BaseModel):
    # Basic motorcycle info
    id: UUID
    title: str
    description: Union[str, None] = Field(default=None)
    brand: str
    model: str
    year: int
    price: Decimal
    
    # Type and condition
    motorcycle_type: MotorcycleType
    condition: ConditionEnum
    seller_type: SellerTypeEnum
    
    # Enhanced specifications
    engine_size: Union[int, None] = Field(default=None)
    engine_type: Union[EngineType, None] = Field(default=None)
    horsepower: Union[int, None] = Field(default=None)
    torque: Union[int, None] = Field(default=None)
    fuel_type: Union[FuelType, None] = Field(default=None)
    transmission_type: Union[TransmissionType, None] = Field(default=None)
    drive_type: Union[DriveType, None] = Field(default=None)
    
    # Physical specs
    weight_dry: Union[int, None] = Field(default=None)
    seat_height: Union[int, None] = Field(default=None)
    
    # History and condition
    mileage: Union[int, None] = Field(default=None)
    previous_owners: Union[int, None] = Field(default=None)
    service_history: bool
    accident_history: bool
    
    # Features
    abs: bool
    traction_control: bool
    accessories: Union[List[str], None] = Field(default_factory=list)
    
    # Location
    city: Union[str, None] = Field(default=None)
    postal_code: Union[str, None] = Field(default=None)
    
    # Status
    is_active: bool
    is_featured: bool
    is_sold: bool
    views_count: int
    favorites_count: int
    
    # Relationships
    category: Union[MotorcycleCategory, None] = Field(default=None)
    seller: Union[SellerInfo, None] = Field(default=None)
    images: List[MotorcycleImage] = Field(default_factory=list)
    specifications: Union[List[MotorcycleSpecification], None] = Field(default_factory=list)
    inspections: Union[List[MotorcycleInspection], None] = Field(default_factory=list)
    
    # Timestamps
    created_at: datetime
    updated_at: Union[datetime, None] = Field(default=None)
    
    class Config:
        from_attributes = True

class AdvancedSearchFilters(BaseModel):
    # Basic filters
    category_id: Union[int, None] = Field(default=None)
    motorcycle_type: Union[MotorcycleType, None] = Field(default=None)
    brand: Union[str, None] = Field(default=None)
    model: Union[str, None] = Field(default=None)
    condition: Union[ConditionEnum, None] = Field(default=None)
    seller_type: Union[SellerTypeEnum, None] = Field(default=None)
    
    # Price and year
    price_min: Union[Decimal, None] = Field(default=None, ge=0)
    price_max: Union[Decimal, None] = Field(default=None, ge=0)
    year_min: Union[int, None] = Field(default=None, ge=1900, le=2030)
    year_max: Union[int, None] = Field(default=None, ge=1900, le=2030)
    
    # Engine and performance
    engine_size_min: Union[int, None] = Field(default=None, ge=0)
    engine_size_max: Union[int, None] = Field(default=None, ge=0)
    engine_type: Union[EngineType, None] = Field(default=None)
    fuel_type: Union[FuelType, None] = Field(default=None)
    horsepower_min: Union[int, None] = Field(default=None, ge=0)
    horsepower_max: Union[int, None] = Field(default=None, ge=0)
    
    # Mileage and history
    mileage_min: Union[int, None] = Field(default=None, ge=0)
    mileage_max: Union[int, None] = Field(default=None, ge=0)
    max_owners: Union[int, None] = Field(default=None, ge=1)
    service_history_required: Union[bool, None] = Field(default=None)
    no_accidents: Union[bool, None] = Field(default=None)
    
    # Features
    abs_required: Union[bool, None] = Field(default=None)
    traction_control_required: Union[bool, None] = Field(default=None)
    
    # Location
    city: Union[str, None] = Field(default=None)
    postal_code: Union[str, None] = Field(default=None)
    radius_km: Union[int, None] = Field(default=50, ge=1, le=500)
    
    # Status
    include_sold: bool = Field(default=False)
    featured_only: bool = Field(default=False)
    
    # Search term
    search_term: Union[str, None] = Field(default=None, max_length=200)
    
    # Sorting
    sort_by: str = Field(default='created_at', regex='^(created_at|price|year|mileage|views_count)$')
    sort_order: str = Field(default='desc', regex='^(asc|desc)$')