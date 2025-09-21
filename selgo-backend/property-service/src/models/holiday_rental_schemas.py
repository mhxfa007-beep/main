# property-service/src/models/holiday_rental_schemas.py
from pydantic import BaseModel, validator, EmailStr, Field
from typing import List, Union, Dict, Any
from datetime import datetime, date
from decimal import Decimal
from uuid import UUID
import enum

class HolidayRentalTypeEnum(str, enum.Enum):
    CABIN = "cabin"
    COTTAGE = "cottage"
    CHALET = "chalet"
    VILLA = "villa"
    APARTMENT = "apartment"
    HOUSE = "house"
    BOAT = "boat"
    CAMPING = "camping"
    GLAMPING = "glamping"

class SeasonEnum(str, enum.Enum):
    SPRING = "spring"
    SUMMER = "summer"
    AUTUMN = "autumn"
    WINTER = "winter"
    ALL_YEAR = "all_year"

class BookingStatusEnum(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    NO_SHOW = "no_show"

class CancellationPolicyEnum(str, enum.Enum):
    FLEXIBLE = "flexible"
    MODERATE = "moderate"
    STRICT = "strict"

# Holiday Rental Schemas
class HolidayRentalBase(BaseModel):
    rental_type: HolidayRentalTypeEnum
    max_guests: int
    min_nights: int = 1
    max_nights: Union[int, None] = Field(default=None)
    price_per_night: Decimal
    cleaning_fee: Decimal = 0
    security_deposit: Decimal = 0
    extra_guest_fee: Decimal = 0
    pet_fee: Decimal = 0
    summer_price_per_night: Union[Decimal, None] = Field(default=None)
    winter_price_per_night: Union[Decimal, None] = Field(default=None)
    weekend_surcharge: Decimal = 0
    holiday_surcharge: Decimal = 0
    available_seasons: Union[str, None] = Field(default=None)
    check_in_time: str = "15:00"
    check_out_time: str = "11:00"
    instant_booking: bool = False
    
    # Amenities
    has_wifi: bool = False
    has_kitchen: bool = False
    has_washing_machine: bool = False
    has_dishwasher: bool = False
    has_tv: bool = False
    has_heating: bool = False
    has_air_conditioning: bool = False
    has_hot_tub: bool = False
    has_sauna: bool = False
    has_fireplace: bool = False
    has_bbq: bool = False
    has_boat_access: bool = False
    has_ski_access: bool = False
    has_beach_access: bool = False
    
    # Policies
    pets_allowed: bool = False
    smoking_allowed: bool = False
    parties_allowed: bool = False
    children_welcome: bool = True
    
    # Location Features
    distance_to_water: Union[float, None] = Field(default=None)
    distance_to_ski_lift: Union[float, None] = Field(default=None)
    distance_to_town_center: Union[float, None] = Field(default=None)
    distance_to_grocery_store: Union[float, None] = Field(default=None)
    
    # Booking Policies
    cancellation_policy: CancellationPolicyEnum = CancellationPolicyEnum.MODERATE
    advance_booking_days: int = 1

    @validator('max_guests')
    def validate_max_guests(cls, v):
        if v <= 0:
            raise ValueError('Max guests must be greater than 0')
        return v

    @validator('min_nights')
    def validate_min_nights(cls, v):
        if v <= 0:
            raise ValueError('Min nights must be greater than 0')
        return v

    @validator('price_per_night')
    def validate_price_per_night(cls, v):
        if v <= 0:
            raise ValueError('Price per night must be greater than 0')
        return v

class HolidayRentalCreate(HolidayRentalBase):
    property_id: UUID

class HolidayRentalUpdate(BaseModel):
    rental_type: Union[HolidayRentalTypeEnum, None] = Field(default=None)
    max_guests: Union[int, None] = Field(default=None)
    min_nights: Union[int, None] = Field(default=None)
    max_nights: Union[int, None] = Field(default=None)
    price_per_night: Union[Decimal, None] = Field(default=None)
    cleaning_fee: Union[Decimal, None] = Field(default=None)
    security_deposit: Union[Decimal, None] = Field(default=None)
    extra_guest_fee: Union[Decimal, None] = Field(default=None)
    pet_fee: Union[Decimal, None] = Field(default=None)
    summer_price_per_night: Union[Decimal, None] = Field(default=None)
    winter_price_per_night: Union[Decimal, None] = Field(default=None)
    weekend_surcharge: Union[Decimal, None] = Field(default=None)
    holiday_surcharge: Union[Decimal, None] = Field(default=None)
    available_seasons: Union[str, None] = Field(default=None)
    check_in_time: Union[str, None] = Field(default=None)
    check_out_time: Union[str, None] = Field(default=None)
    instant_booking: Union[bool, None] = Field(default=None)
    
    # Amenities
    has_wifi: Union[bool, None] = Field(default=None)
    has_kitchen: Union[bool, None] = Field(default=None)
    has_washing_machine: Union[bool, None] = Field(default=None)
    has_dishwasher: Union[bool, None] = Field(default=None)
    has_tv: Union[bool, None] = Field(default=None)
    has_heating: Union[bool, None] = Field(default=None)
    has_air_conditioning: Union[bool, None] = Field(default=None)
    has_hot_tub: Union[bool, None] = Field(default=None)
    has_sauna: Union[bool, None] = Field(default=None)
    has_fireplace: Union[bool, None] = Field(default=None)
    has_bbq: Union[bool, None] = Field(default=None)
    has_boat_access: Union[bool, None] = Field(default=None)
    has_ski_access: Union[bool, None] = Field(default=None)
    has_beach_access: Union[bool, None] = Field(default=None)
    
    # Policies
    pets_allowed: Union[bool, None] = Field(default=None)
    smoking_allowed: Union[bool, None] = Field(default=None)
    parties_allowed: Union[bool, None] = Field(default=None)
    children_welcome: Union[bool, None] = Field(default=None)
    
    # Location Features
    distance_to_water: Union[float, None] = Field(default=None)
    distance_to_ski_lift: Union[float, None] = Field(default=None)
    distance_to_town_center: Union[float, None] = Field(default=None)
    distance_to_grocery_store: Union[float, None] = Field(default=None)
    
    # Booking Policies
    cancellation_policy: Union[CancellationPolicyEnum, None] = Field(default=None)
    advance_booking_days: Union[int, None] = Field(default=None)
    is_active: Union[bool, None] = Field(default=None)

class HolidayRentalResponse(HolidayRentalBase):
    id: UUID
    property_id: UUID
    owner_id: UUID
    is_active: bool
    is_featured: bool
    total_bookings: int
    average_rating: Decimal
    review_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Booking Schemas
class HolidayRentalBookingBase(BaseModel):
    check_in_date: date
    check_out_date: date
    guests: int
    adults: int
    children: int = 0
    infants: int = 0
    pets: int = 0
    guest_name: str
    guest_email: EmailStr
    guest_phone: Union[str, None] = Field(default=None)
    special_requests: Union[str, None] = Field(default=None)

    @validator('check_out_date')
    def validate_dates(cls, v, values):
        if 'check_in_date' in values and v <= values['check_in_date']:
            raise ValueError('Check-out date must be after check-in date')
        return v

    @validator('guests')
    def validate_guests(cls, v):
        if v <= 0:
            raise ValueError('Number of guests must be greater than 0')
        return v

class HolidayRentalBookingCreate(HolidayRentalBookingBase):
    holiday_rental_id: UUID

class HolidayRentalBookingResponse(HolidayRentalBookingBase):
    id: UUID
    holiday_rental_id: UUID
    guest_id: UUID
    nights: int
    base_price: Decimal
    cleaning_fee: Decimal
    security_deposit: Decimal
    extra_fees: Decimal
    total_price: Decimal
    status: BookingStatusEnum
    payment_status: str
    confirmation_code: Union[str, None] = Field(default="")
    created_at: datetime
    updated_at: datetime
    confirmed_at: Union[datetime, None] = Field(default=None)
    cancelled_at: Union[datetime, None] = Field(default=None)
    
    class Config:
        from_attributes = True

class HolidayRentalBookingListResponse(BaseModel):
    bookings: List[HolidayRentalBookingResponse]
    total: int
    page: int
    per_page: int
    total_pages: int

# Review Schemas
class HolidayRentalReviewBase(BaseModel):
    rating: int
    title: Union[str, None] = Field(default=None)
    comment: Union[str, None] = Field(default=None)
    cleanliness_rating: Union[int, None] = Field(default=None)
    location_rating: Union[int, None] = Field(default=None)
    value_rating: Union[int, None] = Field(default=None)
    communication_rating: Union[int, None] = Field(default=None)
    check_in_rating: Union[int, None] = Field(default=None)
    accuracy_rating: Union[int, None] = Field(default=None)

    @validator('rating')
    def validate_rating(cls, v):
        if v < 1 or v > 5:
            raise ValueError('Rating must be between 1 and 5')
        return v

class HolidayRentalReviewCreate(HolidayRentalReviewBase):
    booking_id: UUID

class HolidayRentalReviewResponse(HolidayRentalReviewBase):
    id: UUID
    holiday_rental_id: UUID
    booking_id: UUID
    reviewer_id: UUID
    is_approved: bool
    is_featured: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Availability Schemas
class HolidayRentalAvailabilityBase(BaseModel):
    start_date: date
    end_date: date
    is_available: bool = True
    price_per_night: Union[Decimal, None] = Field(default=None)
    min_nights: Union[int, None] = Field(default=None)
    reason: Union[str, None] = Field(default=None)
    notes: Union[str, None] = Field(default=None)

    @validator('end_date')
    def validate_dates(cls, v, values):
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError('End date must be after start date')
        return v

class HolidayRentalAvailabilityCreate(HolidayRentalAvailabilityBase):
    holiday_rental_id: UUID

class HolidayRentalAvailabilityResponse(HolidayRentalAvailabilityBase):
    id: UUID
    holiday_rental_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Search and Filter Schemas
class HolidayRentalSearchFilters(BaseModel):
    rental_type: Union[List[HolidayRentalTypeEnum], None] = Field(default_factory=list)
    min_guests: Union[int, None] = Field(default=None)
    max_guests: Union[int, None] = Field(default=None)
    price_from: Union[Decimal, None] = Field(default=None)
    price_to: Union[Decimal, None] = Field(default=None)
    check_in_date: Union[date, None] = Field(default=None)
    check_out_date: Union[date, None] = Field(default=None)
    min_nights: Union[int, None] = Field(default=None)
    max_nights: Union[int, None] = Field(default=None)
    location: Union[str, None] = Field(default=None)
    has_wifi: Union[bool, None] = Field(default=None)
    has_kitchen: Union[bool, None] = Field(default=None)
    has_hot_tub: Union[bool, None] = Field(default=None)
    has_sauna: Union[bool, None] = Field(default=None)
    has_boat_access: Union[bool, None] = Field(default=None)
    has_ski_access: Union[bool, None] = Field(default=None)
    has_beach_access: Union[bool, None] = Field(default=None)
    pets_allowed: Union[bool, None] = Field(default=None)
    instant_booking: Union[bool, None] = Field(default=None)
    min_rating: Union[Decimal, None] = Field(default=None)

class HolidayRentalSearchRequest(BaseModel):
    query: Union[str, None] = Field(default=None)
    filters: Union[HolidayRentalSearchFilters, None] = Field(default=None)
    sort_by: Union[str, None] = Field(default="created_at")
    sort_order: Union[str, None] = Field(default="desc")
    page: int = 1
    per_page: int = 20

class HolidayRentalListResponse(BaseModel):
    rentals: List[HolidayRentalResponse]
    total: int
    page: int
    per_page: int
    total_pages: int

# Statistics Schemas
class HolidayRentalStats(BaseModel):
    total_rentals: int
    active_rentals: int
    total_bookings: int
    confirmed_bookings: int
    average_price: Decimal
    average_rating: Decimal
    popular_locations: List[Dict[str, Any]]
    bookings_by_type: Dict[str, int]
    seasonal_trends: Dict[str, Any]