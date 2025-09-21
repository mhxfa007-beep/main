# property-service/src/schemas.py
from pydantic import BaseModel, EmailStr, validator, Field
from typing import List, Union, Dict, Any
from datetime import datetime
from decimal import Decimal
from uuid import UUID
import enum

class PropertyTypeEnum(str, enum.Enum):
    PURCHASE = "purchase"
    RENT = "rent"
    SELL = "sell"
    NUTRITION = "nutrition"

class PropertyCategoryEnum(str, enum.Enum):
    PLOTS = "plots"
    RESIDENCE_ABROAD = "residence_abroad"
    HOUSING_SALE = "housing_sale"
    NEW_HOMES = "new_homes"
    VACATION_HOMES = "vacation_homes"
    LEISURE_PLOTS = "leisure_plots"

class PropertyStatusEnum(str, enum.Enum):
    ACTIVE = "active"
    SOLD = "sold"
    RENTED = "rented"
    PENDING = "pending"
    INACTIVE = "inactive"

# Base Schemas
class PropertyCategoryBase(BaseModel):
    label: str
    type: PropertyTypeEnum
    icon: Union[str, None] = Field(default="", description="Icon URL or class name")
    route: Union[str, None] = Field(default="", description="Route path for category")
    description: Union[str, None] = Field(default="", description="Category description")

class PropertyCategoryCreate(PropertyCategoryBase):
    pass

class PropertyCategoryResponse(PropertyCategoryBase):
    id: int
    is_active: bool
    sort_order: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class PropertyImageBase(BaseModel):
    image_url: str
    alt_text: Union[str, None] = Field(default="", description="Alternative text for image")
    is_primary: bool = False
    sort_order: int = 0

class PropertyImageCreate(PropertyImageBase):
    pass

class PropertyImageResponse(PropertyImageBase):
    id: UUID
    property_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True

class FacilityBase(BaseModel):
    name: str
    icon: Union[str, None] = Field(default="", description="Facility icon")
    category: Union[str, None] = Field(default="general", description="Facility category")

class FacilityResponse(FacilityBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class PropertyFacilityBase(BaseModel):
    facility_id: int
    value: Union[str, None] = Field(default="", description="Facility value or description")

class PropertyFacilityCreate(PropertyFacilityBase):
    pass

class PropertyFacilityResponse(PropertyFacilityBase):
    id: UUID
    property_id: UUID
    facility: Union[FacilityResponse, None] = Field(default=None, description="Associated facility details")
    created_at: datetime
    
    class Config:
        from_attributes = True

class PropertyBase(BaseModel):
    title: str
    description: Union[str, None] = Field(default="", description="Property description")
    price: Decimal
    property_type: PropertyTypeEnum
    property_category: PropertyCategoryEnum
    
    # Property Details
    bedrooms: Union[int, None] = Field(default=0, ge=0, description="Number of bedrooms")
    bathrooms: Union[int, None] = Field(default=0, ge=0, description="Number of bathrooms")
    rooms: Union[int, None] = Field(default=0, ge=0, description="Total number of rooms")
    use_area: Union[float, None] = Field(default=0.0, ge=0, description="Usable area in square meters")
    plot_area: Union[float, None] = Field(default=0.0, ge=0, description="Plot area in square meters")
    year_built: Union[int, None] = Field(default=0, ge=1800, le=2030, description="Year the property was built")
    
    # Property Type and Features
    housing_type: Union[str, None] = Field(default="", description="Type of housing (apartment, house, etc.)")
    ownership_form: Union[str, None] = Field(default="owned", description="Ownership form")
    condition: Union[str, None] = Field(default="good", description="Property condition")
    
    # Location
    address: Union[str, None] = Field(default="", description="Property address")
    city: Union[str, None] = Field(default="", description="City")
    state: Union[str, None] = Field(default="", description="State or region")
    postal_code: Union[str, None] = Field(default="", description="Postal code")
    country: str = Field(default="Norway", description="Country")
    latitude: Union[float, None] = Field(default=0.0, ge=-90, le=90, description="Latitude coordinate")
    longitude: Union[float, None] = Field(default=0.0, ge=-180, le=180, description="Longitude coordinate")
    
    # Features
    is_furnished: bool = False
    has_balcony: bool = False
    has_terrace: bool = False
    has_fireplace: bool = False
    has_parking: bool = False
    parking_spaces: int = Field(default=0, ge=0, description="Number of parking spaces")
    has_garden: bool = False
    has_basement: bool = False
    has_garage: bool = False
    
    # Energy and Utilities
    energy_rating: Union[str, None] = Field(default="", description="Energy efficiency rating (A-G)")
    heating_type: Union[str, None] = Field(default="", description="Type of heating system")
    
    # Financial
    monthly_costs: Union[Decimal, None] = Field(default=Decimal('0'), ge=0, description="Monthly costs")
    deposit_amount: Union[Decimal, None] = Field(default=Decimal('0'), ge=0, description="Security deposit amount")
    shared_costs: Union[Decimal, None] = Field(default=Decimal('0'), ge=0, description="Shared/common costs")
    property_tax: Union[Decimal, None] = Field(default=Decimal('0'), ge=0, description="Annual property tax")
    
    # Owner Information
    owner_name: Union[str, None] = Field(default="", description="Property owner name")
    owner_phone: Union[str, None] = Field(default="", description="Owner phone number")
    owner_email: Union[EmailStr, None] = Field(default=None, description="Owner email address")
    is_agent: bool = False
    agent_company: Union[str, None] = Field(default="", description="Real estate agency name")

class PropertyCreate(PropertyBase):
    owner_id: UUID
    category_id: Union[int, None] = Field(default=None, description="Property category ID")
    images: List[PropertyImageCreate] = Field(default_factory=list, description="Property images")
    facilities: List[PropertyFacilityCreate] = Field(default_factory=list, description="Property facilities")

class PropertyUpdate(BaseModel):
    title: Union[str, None] = Field(default=None, description="Updated property title")
    description: Union[str, None] = Field(default=None, description="Updated property description")
    price: Union[Decimal, None] = Field(default=None, ge=0, description="Updated price")
    status: Union[PropertyStatusEnum, None] = Field(default=None, description="Updated property status")
    
    # Property Details
    bedrooms: Union[int, None] = Field(default=None, ge=0, description="Updated number of bedrooms")
    bathrooms: Union[int, None] = Field(default=None, ge=0, description="Updated number of bathrooms")
    rooms: Union[int, None] = Field(default=None, ge=0, description="Updated total rooms")
    use_area: Union[float, None] = Field(default=None, ge=0, description="Updated usable area")
    plot_area: Union[float, None] = Field(default=None, ge=0, description="Updated plot area")
    year_built: Union[int, None] = Field(default=None, ge=1800, le=2030, description="Updated year built")
    
    # Features
    is_furnished: Union[bool, None] = Field(default=None, description="Updated furnished status")
    has_balcony: Union[bool, None] = Field(default=None, description="Updated balcony status")
    has_terrace: Union[bool, None] = Field(default=None, description="Updated terrace status")
    has_fireplace: Union[bool, None] = Field(default=None, description="Updated fireplace status")
    has_parking: Union[bool, None] = Field(default=None, description="Updated parking status")
    parking_spaces: Union[int, None] = Field(default=None, ge=0, description="Updated parking spaces")
    has_garden: Union[bool, None] = Field(default=None, description="Updated garden status")
    has_basement: Union[bool, None] = Field(default=None, description="Updated basement status")
    has_garage: Union[bool, None] = Field(default=None, description="Updated garage status")
    
    # Financial
    monthly_costs: Union[Decimal, None] = Field(default=None, ge=0, description="Updated monthly costs")
    deposit_amount: Union[Decimal, None] = Field(default=None, ge=0, description="Updated deposit amount")
    shared_costs: Union[Decimal, None] = Field(default=None, ge=0, description="Updated shared costs")
    property_tax: Union[Decimal, None] = Field(default=None, ge=0, description="Updated property tax")

class PropertyResponse(PropertyBase):
    id: UUID
    status: PropertyStatusEnum
    slug: Union[str, None] = Field(default="", description="Property URL slug")
    category_id: Union[int, None] = Field(default=None, description="Category ID")
    is_featured: bool
    is_premium: bool
    views_count: int
    favorites_count: int
    created_at: datetime
    updated_at: datetime
    published_at: Union[datetime, None] = Field(default=None, description="Publication date")
    
    # Relationships
    category: Union[PropertyCategoryResponse, None] = Field(default=None, description="Property category details")
    images: List[PropertyImageResponse] = Field(default_factory=list, description="Property images")
    facilities: List[PropertyFacilityResponse] = Field(default_factory=list, description="Property facilities")
    
    class Config:
        from_attributes = True

class PropertySummaryResponse(BaseModel):
    id: UUID
    title: str
    price: Decimal
    property_type: PropertyTypeEnum
    property_category: PropertyCategoryEnum
    city: Union[str, None] = Field(default="", description="Property city")
    bedrooms: Union[int, None] = Field(default=0, description="Number of bedrooms")
    use_area: Union[float, None] = Field(default=0.0, description="Usable area")
    primary_image: Union[str, None] = Field(default="", description="Primary image URL")
    is_featured: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class PropertySearchParams(BaseModel):
    property_type: Union[PropertyTypeEnum, None] = Field(default=None, description="Filter by property type")
    property_category: Union[PropertyCategoryEnum, None] = Field(default=None, description="Filter by property category")
    min_price: Union[Decimal, None] = Field(default=None, ge=0, description="Minimum price filter")
    max_price: Union[Decimal, None] = Field(default=None, ge=0, description="Maximum price filter")
    city: Union[str, None] = Field(default=None, description="Filter by city")
    bedrooms: Union[int, None] = Field(default=None, ge=0, description="Filter by number of bedrooms")
    min_area: Union[float, None] = Field(default=None, ge=0, description="Minimum area filter")
    max_area: Union[float, None] = Field(default=None, ge=0, description="Maximum area filter")
    keyword: Union[str, None] = Field(default=None, description="Search keyword")
    page: int = Field(default=1, ge=1, description="Page number")
    size: int = Field(default=20, ge=1, le=100, description="Items per page")
    sort_by: str = Field(default="created_at", description="Sort field")
    sort_order: str = Field(default="desc", regex="^(asc|desc)$", description="Sort order")

class PropertyMessageBase(BaseModel):
    sender_name: str
    sender_email: EmailStr
    sender_phone: Union[str, None] = Field(default="", description="Sender phone number")
    message: str

class PropertyMessageCreate(PropertyMessageBase):
    property_id: UUID

class PropertyMessageResponse(PropertyMessageBase):
    id: UUID
    property_id: UUID
    is_read: bool
    is_replied: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class PropertyComparisonCreate(BaseModel):
    property_ids: List[UUID]
    user_id: Union[UUID, None] = Field(default=None, description="User ID for logged-in users")
    session_id: Union[str, None] = Field(default=None, description="Session ID for anonymous users")

class PropertyComparisonResponse(BaseModel):
    id: UUID
    properties: List[PropertyResponse]
    created_at: datetime
    
    class Config:
        from_attributes = True

class PropertyLoanEstimateRequest(BaseModel):
    property_id: UUID
    loan_amount: Decimal = Field(ge=0, description="Loan amount requested")
    duration_months: int = Field(ge=1, le=480, description="Loan duration in months")
    interest_rate: Union[Decimal, None] = Field(default=Decimal("3.5"), ge=0, le=20, description="Interest rate percentage")
    email: Union[EmailStr, None] = Field(default=None, description="Contact email")
    phone: Union[str, None] = Field(default="", description="Contact phone number")

class PropertyLoanEstimateResponse(BaseModel):
    property_id: UUID
    loan_amount: Decimal
    duration_months: int
    interest_rate: Decimal
    monthly_payment: Decimal
    total_payment: Decimal
    total_interest: Decimal
    
    class Config:
        from_attributes = True

class PopularCityResponse(BaseModel):
    id: int
    name: str
    state: Union[str, None] = Field(default="", description="State or region")
    country: str
    image_url: Union[str, None] = Field(default="", description="City image URL")
    rental_count: int
    avg_price: Union[Decimal, None] = Field(default=Decimal('0'), ge=0, description="Average rental price")
    
    class Config:
        from_attributes = True

class RentalTipResponse(BaseModel):
    id: int
    title: str
    content: str
    tip_number: Union[int, None] = Field(default=0, description="Tip number")
    category: Union[str, None] = Field(default="general", description="Tip category")
    
    class Config:
        from_attributes = True

class FeedbackCreate(BaseModel):
    message: str
    page_url: Union[str, None] = Field(default="", description="Page URL where feedback was given")
    email: Union[EmailStr, None] = Field(default=None, description="User email")
    rating: Union[int, None] = Field(default=None, ge=1, le=5, description="Rating from 1 to 5")
    
    @validator('rating')
    def validate_rating(cls, v):
        if v is not None and (v < 1 or v > 5):
            raise ValueError('Rating must be between 1 and 5')
        return v

class FeedbackResponse(BaseModel):
    id: UUID
    message: str
    page_url: Union[str, None] = Field(default="", description="Page URL")
    rating: Union[int, None] = Field(default=None, description="User rating")
    created_at: datetime
    
    class Config:
        from_attributes = True

class PropertyPriceInsightResponse(BaseModel):
    city: str
    area: Union[str, None] = Field(default=None)
    avg_price_per_sqm: Decimal
    currency: str
    period_description: str
    sample_size: int
    property_type: Union[str, None] = Field(default=None)
    
    class Config:
        from_attributes = True

class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int
    
# Additional schemas for points 6-10

# Point 6: Property Map Location Schemas
class PropertyMapLocationBase(BaseModel):
    latitude: float
    longitude: float
    address_components: Union[str, None] = Field(default=None)
    google_place_id: Union[str, None] = Field(default=None)
    is_approximate: bool = False

class PropertyMapLocationCreate(PropertyMapLocationBase):
    property_id: UUID

class PropertyMapLocationResponse(PropertyMapLocationBase):
    id: UUID
    property_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True

class PropertyMapSearchRequest(BaseModel):
    center_lat: float
    center_lng: float
    radius_km: float
    filters: Union[Dict[str, Any], None] = Field(default_factory=dict)
    user_id: Union[UUID, None] = Field(default=None)
    session_id: Union[str, None] = Field(default=None)

class PropertyNearbyPlaceResponse(BaseModel):
    id: UUID
    place_name: str
    place_type: str
    distance_km: float
    
    class Config:
        from_attributes = True

# Point 7: Property Comparison Schemas
class PropertyComparisonSessionCreate(BaseModel):
    property_ids: List[UUID]
    comparison_name: Union[str, None] = Field(default=None)
    user_id: Union[UUID, None] = Field(default=None)
    session_id: Union[str, None] = Field(default=None)

class PropertyComparisonItemResponse(BaseModel):
    id: UUID
    property_id: UUID
    sort_order: int
    is_favorite: bool
    user_rating: Union[int, None] = Field(default=None)
    
    class Config:
        from_attributes = True

class PropertyComparisonNoteCreate(BaseModel):
    property_id: UUID
    note_text: str
    note_category: Union[str, None] = Field(default=None)

class PropertyComparisonNoteResponse(BaseModel):
    id: UUID
    property_id: UUID
    note_text: str
    note_category: Union[str, None] = Field(default=None)
    created_at: datetime
    
    class Config:
        from_attributes = True

class PropertyComparisonSessionResponse(BaseModel):
    id: UUID
    comparison_name: Union[str, None] = Field(default=None)
    is_saved: bool
    created_at: datetime
    comparison_items: List[PropertyComparisonItemResponse] = []
    comparison_notes: List[PropertyComparisonNoteResponse] = []
    
    class Config:
        from_attributes = True

# Point 8: Property Loan Estimator Schemas
class PropertyLoanEstimateRequest(BaseModel):
    property_id: UUID
    property_price: Decimal
    down_payment: Decimal
    interest_rate: Decimal
    loan_term_years: int
    property_tax_monthly: Union[Decimal, None] = Field(default=None)
    insurance_monthly: Union[Decimal, None] = Field(default=None)
    hoa_fees_monthly: Union[Decimal, None] = Field(default=None)
    user_id: Union[UUID, None] = Field(default=None)
    session_id: Union[str, None] = Field(default=None)

class PropertyLoanEstimateResponse(BaseModel):
    id: UUID
    property_id: UUID
    loan_amount: Decimal
    monthly_payment: Decimal
    total_payment: Decimal
    total_interest: Decimal
    total_monthly_cost: Union[Decimal, None] = Field(default=None)
    calculation_date: datetime
    
    class Config:
        from_attributes = True

class LoanProviderResponse(BaseModel):
    id: int
    provider_name: str
    provider_type: str
    base_interest_rate: Decimal
    min_down_payment_percent: Decimal
    website_url: Union[str, None] = Field(default=None)
    contact_phone: Union[str, None] = Field(default=None)
    
    class Config:
        from_attributes = True

class PropertyLoanApplicationCreate(BaseModel):
    estimate_id: UUID
    provider_id: int
    applicant_name: str
    applicant_email: EmailStr
    applicant_phone: Union[str, None] = Field(default=None)
    annual_income: Union[Decimal, None] = Field(default=None)
    credit_score: Union[int, None] = Field(default=None)
    employment_status: Union[str, None] = Field(default=None)

class PropertyLoanApplicationResponse(BaseModel):
    id: UUID
    status: str
    application_date: datetime
    approved_amount: Union[Decimal, None] = Field(default=None)
    approved_rate: Union[Decimal, None] = Field(default=None)
    
    class Config:
        from_attributes = True

# Point 9: New Rental Ad Schemas
class RentalPropertyCreate(BaseModel):
    property_id: UUID
    monthly_rent: Decimal
    security_deposit: Decimal
    first_month_rent: Union[Decimal, None] = Field(default=None)
    last_month_rent: Union[Decimal, None] = Field(default=None)
    min_lease_duration_months: int = 12
    max_lease_duration_months: Union[int, None] = Field(default=None)
    available_from: date
    lease_type: str = "fixed"
    pets_allowed: bool = False
    smoking_allowed: bool = False
    max_occupants: Union[int, None] = Field(default=None)
    utilities_included: Union[List[str], None] = Field(default_factory=list)
    parking_included: bool = False
    internet_included: bool = False
    minimum_income_multiple: Decimal = Decimal("3.0")
    credit_score_minimum: Union[int, None] = Field(default=None)
    background_check_required: bool = True
    references_required: int = 2

class RentalPropertyResponse(BaseModel):
    id: UUID
    property_id: UUID
    monthly_rent: Decimal
    security_deposit: Decimal
    available_from: date
    lease_type: str
    pets_allowed: bool
    is_available: bool
    view_count: int
    inquiry_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class RentalApplicationCreate(BaseModel):
    rental_property_id: UUID
    desired_move_in_date: date
    lease_duration_months: int
    annual_income: Decimal
    employment_status: str
    employer_name: Union[str, None] = Field(default=None)
    credit_score: Union[int, None] = Field(default=None)
    previous_address: Union[str, None] = Field(default=None)
    reason_for_moving: Union[str, None] = Field(default=None)
    pets_description: Union[str, None] = Field(default=None)
    special_requests: Union[str, None] = Field(default=None)

class RentalApplicationResponse(BaseModel):
    id: UUID
    rental_property_id: UUID
    application_date: datetime
    desired_move_in_date: date
    status: str
    annual_income: Decimal
    employment_status: str
    
    class Config:
        from_attributes = True

# Point 10: Lease Contract Schemas
class LeaseContractCreate(BaseModel):
    rental_property_id: UUID
    application_id: Union[UUID, None] = Field(default=None)
    tenant_id: UUID
    lease_start_date: date
    lease_end_date: date
    monthly_rent: Decimal
    security_deposit: Decimal
    lease_terms: str
    special_conditions: Union[str, None] = Field(default=None)
    pets_clause: Union[str, None] = Field(default=None)
    maintenance_responsibilities: Union[str, None] = Field(default=None)

class LeaseContractTemplateResponse(BaseModel):
    id: int
    template_name: str
    template_type: str
    jurisdiction: str
    is_default: bool
    is_active: bool
    version: str
    approved_by_legal: bool
    
    class Config:
        from_attributes = True

class RentalSuggestionRequest(BaseModel):
    preferred_location: Union[str, None] = Field(default=None)
    max_rent: Union[Decimal, None] = Field(default=None)
    min_bedrooms: Union[int, None] = Field(default=None)
    max_bedrooms: Union[int, None] = Field(default=None)
    property_type: Union[str, None] = Field(default=None)
    amenities_required: Union[List[str], None] = Field(default_factory=list)
    user_id: Union[UUID, None] = Field(default=None)
    session_id: Union[str, None] = Field(default=None)

class RentalSuggestionResponse(BaseModel):
    id: UUID
    suggested_properties: List[UUID]
    suggestion_algorithm: Union[str, None] = Field(default=None)
    suggestion_score: Union[Decimal, None] = Field(default=None)
    created_at: datetime
    
    class Config:
        from_attributes = True

# Authentication-related schemas
class AuthenticatedUser(BaseModel):
    user_id: UUID
    email: str
    is_verified: bool
    roles: List[str] = []

# Common response schemas
class SuccessResponse(BaseModel):
    success: bool
    message: str
    data: Union[Dict[str, Any], None] = Field(default=None)

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    details: Union[Dict[str, Any], None] = Field(default=None)