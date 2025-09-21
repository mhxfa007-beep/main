from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum, Table, Text, Index, DECIMAL, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry
import enum
import uuid
from datetime import datetime

Base = declarative_base()

# Association table for many-to-many relationship between cars and features
car_feature_association = Table(
    'car_feature_association',
    Base.metadata,
    Column('car_id', UUID(as_uuid=True), ForeignKey('cars.id'), primary_key=True),
    Column('feature_id', Integer, ForeignKey('car_features.id'), primary_key=True)
)

# Enum for car conditions
class CarCondition(enum.Enum):
    NEW = "new"
    USED = "used"
    DAMAGED = "damaged"
    PARTS_ONLY = "parts_only"

# Enum for seller types
class SellerType(enum.Enum):
    PRIVATE = "private"
    DEALER = "dealer"
    IMPORTER = "importer"

# Enum for ad types
class AdType(enum.Enum):
    FOR_SALE = "for_sale"
    WANTED = "wanted"
    AUCTION = "auction"

# Enum for fuel types
class FuelType(enum.Enum):
    PETROL = "petrol"
    DIESEL = "diesel"
    ELECTRIC = "electric"
    HYBRID = "hybrid"
    PLUGIN_HYBRID = "plugin_hybrid"
    HYDROGEN = "hydrogen"
    GAS = "gas"

# Enum for transmission types
class TransmissionType(enum.Enum):
    MANUAL = "manual"
    AUTOMATIC = "automatic"
    SEMI_AUTOMATIC = "semi_automatic"
    CVT = "cvt"

# Enum for drive types
class DriveType(enum.Enum):
    FRONT_WHEEL = "front_wheel"
    REAR_WHEEL = "rear_wheel"
    ALL_WHEEL = "all_wheel"
    FOUR_WHEEL = "four_wheel"

# Enum for car status
class CarStatus(enum.Enum):
    ACTIVE = "active"
    SOLD = "sold"
    RESERVED = "reserved"
    INACTIVE = "inactive"
    EXPIRED = "expired"

class CarCategory(Base):
    __tablename__ = 'car_categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    parent_id = Column(Integer, ForeignKey('car_categories.id', ondelete='CASCADE'), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    children = relationship("CarCategory", backref=backref('parent', remote_side=[id]), cascade="all, delete-orphan")
    cars = relationship("Car", back_populates="category")

class CarFeature(Base):
    __tablename__ = 'car_features'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    cars = relationship("Car", secondary=car_feature_association, back_populates="features")

class Car(Base):
    __tablename__ = 'cars'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    price = Column(DECIMAL(12, 2), nullable=False)
    
    # Basic car information
    category_id = Column(Integer, ForeignKey('car_categories.id'), nullable=False)
    condition = Column(Enum(CarCondition), default=CarCondition.USED)
    year = Column(Integer, nullable=False)
    make = Column(String(100), nullable=False, index=True)
    model = Column(String(100), nullable=False, index=True)
    variant = Column(String(100), nullable=True)  # e.g., "Sport", "Luxury"
    
    # Technical specifications
    mileage = Column(Integer, nullable=True)
    fuel_type = Column(Enum(FuelType), nullable=True)
    transmission = Column(Enum(TransmissionType), nullable=True)
    engine_size = Column(Float, nullable=True)  # in liters
    engine_power = Column(Integer, nullable=True)  # in HP
    engine_power_kw = Column(Integer, nullable=True)  # in kW
    cylinders = Column(Integer, nullable=True)
    drive_type = Column(Enum(DriveType), nullable=True)
    
    # Physical attributes
    color = Column(String(100), nullable=True)
    interior_color = Column(String(100), nullable=True)
    body_type = Column(String(100), nullable=True)
    doors = Column(Integer, nullable=True)
    seats = Column(Integer, nullable=True)
    
    # Dimensions and weight
    length = Column(Integer, nullable=True)  # in mm
    width = Column(Integer, nullable=True)  # in mm
    height = Column(Integer, nullable=True)  # in mm
    weight = Column(Integer, nullable=True)  # in kg
    trunk_capacity = Column(Integer, nullable=True)  # in liters
    
    # Registration and legal
    vin = Column(String(17), nullable=True, unique=True)
    registration_number = Column(String(20), nullable=True)
    first_registration = Column(DateTime, nullable=True)
    registration_country = Column(String(3), default="NOR")
    
    # Ownership and history
    previous_owners = Column(Integer, default=0)
    service_history = Column(Boolean, default=False)
    accident_history = Column(Boolean, default=False)
    
    # Inspection and certification
    last_inspection = Column(DateTime, nullable=True)
    next_inspection = Column(DateTime, nullable=True)
    inspection_status = Column(String(50), nullable=True)  # passed, failed, pending
    
    # Financial information
    original_price = Column(DECIMAL(12, 2), nullable=True)
    market_value = Column(DECIMAL(12, 2), nullable=True)
    financing_available = Column(Boolean, default=False)
    lease_available = Column(Boolean, default=False)
    warranty_remaining = Column(Integer, nullable=True)  # months
    
    # Seller information
    seller_type = Column(Enum(SellerType), default=SellerType.PRIVATE)
    seller_id = Column(UUID(as_uuid=True), nullable=False)  # Reference to user or dealer
    dealer_id = Column(UUID(as_uuid=True), nullable=True)  # If sold by dealer
    
    # Ad information
    ad_type = Column(Enum(AdType), default=AdType.FOR_SALE)
    status = Column(Enum(CarStatus), default=CarStatus.ACTIVE)
    is_featured = Column(Boolean, default=False)
    is_premium = Column(Boolean, default=False)
    featured_until = Column(DateTime, nullable=True)
    
    # Location
    location = Column(Geometry('POINT', srid=4326))
    location_name = Column(String(255))
    city = Column(String(100), nullable=True)
    postal_code = Column(String(10), nullable=True)
    country = Column(String(3), default="NOR")
    
    # Engagement metrics
    view_count = Column(Integer, default=0)
    favorites_count = Column(Integer, default=0)
    inquiries_count = Column(Integer, default=0)
    
    # SEO and metadata
    slug = Column(String(255), nullable=True, unique=True)
    meta_title = Column(String(255), nullable=True)
    meta_description = Column(String(500), nullable=True)
    
    # Additional data
    additional_info = Column(JSON, nullable=True)  # For flexible additional data
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    published_at = Column(DateTime, nullable=True)
    sold_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)

    # Relationships
    category = relationship("CarCategory", back_populates="cars")
    images = relationship("CarImage", back_populates="car", cascade="all, delete-orphan")
    features = relationship("CarFeature", secondary=car_feature_association, back_populates="cars")
    ratings = relationship("CarRating", back_populates="car", cascade="all, delete-orphan")
    inspections = relationship("CarInspection", back_populates="car", cascade="all, delete-orphan")
    history_records = relationship("CarHistory", back_populates="car", cascade="all, delete-orphan")
    financing_options = relationship("CarFinancing", back_populates="car", cascade="all, delete-orphan")
    inquiries = relationship("CarInquiry", back_populates="car", cascade="all, delete-orphan")

class CarImage(Base):
    __tablename__ = 'car_images'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    car_id = Column(UUID(as_uuid=True), ForeignKey('cars.id', ondelete='CASCADE'), nullable=False)
    image_url = Column(String(500), nullable=False)
    thumbnail_url = Column(String(500), nullable=True)
    alt_text = Column(String(255), nullable=True)
    is_primary = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    file_size = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=func.now())

    car = relationship("Car", back_populates="images")

class CarRating(Base):
    __tablename__ = 'car_ratings'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    car_id = Column(UUID(as_uuid=True), ForeignKey('cars.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, nullable=False)
    stars = Column(Integer, nullable=False)  # 1-5 stars
    review = Column(Text)
    is_verified_purchase = Column(Boolean, default=False)
    helpful_votes = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())

    car = relationship("Car", back_populates="ratings")

class CarFavorite(Base):
    __tablename__ = 'car_favorites'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(Integer, nullable=False)
    car_id = Column(UUID(as_uuid=True), ForeignKey('cars.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, default=func.now())

    car = relationship("Car", backref="favorited_by")

    __table_args__ = (
        Index('idx_user_car_favorite_unique', 'user_id', 'car_id', unique=True),
    )

class CarInspection(Base):
    __tablename__ = 'car_inspections'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    car_id = Column(UUID(as_uuid=True), ForeignKey('cars.id', ondelete='CASCADE'), nullable=False)
    inspection_date = Column(DateTime, nullable=False)
    inspection_type = Column(String(50), nullable=False)  # annual, pre_purchase, damage
    status = Column(String(50), nullable=False)  # passed, failed, conditional
    mileage_at_inspection = Column(Integer, nullable=True)
    inspector_name = Column(String(255), nullable=True)
    inspection_station = Column(String(255), nullable=True)
    
    # Inspection results
    overall_condition = Column(String(50), nullable=True)
    defects_found = Column(JSON, nullable=True)  # List of defects
    recommendations = Column(Text, nullable=True)
    next_inspection_due = Column(DateTime, nullable=True)
    
    # Documentation
    report_url = Column(String(500), nullable=True)
    certificate_number = Column(String(100), nullable=True)
    
    created_at = Column(DateTime, default=func.now())
    
    car = relationship("Car", back_populates="inspections")

class CarHistory(Base):
    __tablename__ = 'car_history'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    car_id = Column(UUID(as_uuid=True), ForeignKey('cars.id', ondelete='CASCADE'), nullable=False)
    event_date = Column(DateTime, nullable=False)
    event_type = Column(String(50), nullable=False)  # purchase, sale, accident, service, inspection
    description = Column(Text, nullable=True)
    mileage = Column(Integer, nullable=True)
    cost = Column(DECIMAL(10, 2), nullable=True)
    
    # Service/repair specific
    service_provider = Column(String(255), nullable=True)
    parts_replaced = Column(JSON, nullable=True)
    
    # Accident specific
    damage_description = Column(Text, nullable=True)
    repair_cost = Column(DECIMAL(10, 2), nullable=True)
    insurance_claim = Column(Boolean, default=False)
    
    # Documentation
    receipt_url = Column(String(500), nullable=True)
    photos = Column(JSON, nullable=True)  # URLs to photos
    
    created_at = Column(DateTime, default=func.now())
    
    car = relationship("Car", back_populates="history_records")

class CarFinancing(Base):
    __tablename__ = 'car_financing'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    car_id = Column(UUID(as_uuid=True), ForeignKey('cars.id', ondelete='CASCADE'), nullable=False)
    
    # Financing details
    financing_type = Column(String(50), nullable=False)  # loan, lease, hire_purchase
    provider_name = Column(String(255), nullable=False)
    interest_rate = Column(DECIMAL(5, 2), nullable=False)
    term_months = Column(Integer, nullable=False)
    down_payment = Column(DECIMAL(10, 2), nullable=True)
    monthly_payment = Column(DECIMAL(10, 2), nullable=False)
    total_cost = Column(DECIMAL(12, 2), nullable=False)
    
    # Requirements
    min_credit_score = Column(Integer, nullable=True)
    min_income = Column(DECIMAL(10, 2), nullable=True)
    max_age = Column(Integer, nullable=True)
    
    # Terms and conditions
    early_repayment_fee = Column(DECIMAL(8, 2), nullable=True)
    late_payment_fee = Column(DECIMAL(6, 2), nullable=True)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    
    car = relationship("Car", back_populates="financing_options")

class CarInquiry(Base):
    __tablename__ = 'car_inquiries'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    car_id = Column(UUID(as_uuid=True), ForeignKey('cars.id', ondelete='CASCADE'), nullable=False)
    inquirer_id = Column(Integer, nullable=True)  # User ID if logged in
    
    # Contact information
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    
    # Inquiry details
    inquiry_type = Column(String(50), nullable=False)  # viewing, test_drive, purchase, trade_in
    message = Column(Text, nullable=True)
    preferred_contact_method = Column(String(20), default="email")
    preferred_contact_time = Column(String(50), nullable=True)
    
    # Status tracking
    status = Column(String(50), default="new")  # new, contacted, scheduled, completed, closed
    response_sent = Column(Boolean, default=False)
    response_date = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=func.now())
    
    car = relationship("Car", back_populates="inquiries")

class CarComparison(Base):
    __tablename__ = 'car_comparisons'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(Integer, nullable=True)  # Can be null for anonymous users
    session_id = Column(String(255), nullable=True)  # For anonymous tracking
    car_ids = Column(JSON, nullable=False)  # List of car IDs being compared
    created_at = Column(DateTime, default=func.now())

class CarSavedSearch(Base):
    __tablename__ = 'car_saved_searches'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)
    search_criteria = Column(JSON, nullable=False)  # Search filters
    email_alerts = Column(Boolean, default=True)
    alert_frequency = Column(String(20), default="daily")  # daily, weekly, immediate
    last_alert_sent = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())

class CarPriceAlert(Base):
    __tablename__ = 'car_price_alerts'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(Integer, nullable=False)
    car_id = Column(UUID(as_uuid=True), ForeignKey('cars.id', ondelete='CASCADE'), nullable=False)
    target_price = Column(DECIMAL(12, 2), nullable=False)
    alert_type = Column(String(20), default="below")  # below, above, change
    is_active = Column(Boolean, default=True)
    triggered_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())

class CarDealer(Base):
    __tablename__ = 'car_dealers'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(255), nullable=False)
    business_number = Column(String(20), nullable=True)
    address = Column(String(500), nullable=True)
    city = Column(String(100), nullable=True)
    postal_code = Column(String(10), nullable=True)
    country = Column(String(3), default="NOR")
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    website = Column(String(255), nullable=True)
    
    # Business information
    established_year = Column(Integer, nullable=True)
    specializations = Column(JSON, nullable=True)  # List of car brands/types
    services_offered = Column(JSON, nullable=True)  # financing, warranty, etc.
    
    # Ratings and reviews
    rating = Column(DECIMAL(3, 2), default=0.0)
    review_count = Column(Integer, default=0)
    
    # Status
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class CarReport(Base):
    __tablename__ = 'car_reports'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    car_id = Column(UUID(as_uuid=True), ForeignKey('cars.id', ondelete='CASCADE'), nullable=False)
    reported_by = Column(Integer, nullable=False)  # User ID
    reason = Column(String(100), nullable=False)  # fraud, incorrect_info, spam, etc.
    description = Column(Text, nullable=True)
    status = Column(String(50), default="pending")  # pending, reviewed, resolved, dismissed
    admin_notes = Column(Text, nullable=True)
    reviewed_by = Column(Integer, nullable=True)  # Admin user ID
    reviewed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())