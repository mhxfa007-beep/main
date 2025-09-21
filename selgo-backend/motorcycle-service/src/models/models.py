# selgo-backend/motorcycle-service/src/models.py
from sqlalchemy import Column, Integer, String, Index, Text, DECIMAL, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.dialects.postgresql import ENUM, UUID, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
import enum
import uuid

Base = declarative_base()

# Define Python enums
class MotorcycleType(enum.Enum):
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

class EngineType(enum.Enum):
    SINGLE_CYLINDER = "single_cylinder"
    PARALLEL_TWIN = "parallel_twin"
    V_TWIN = "v_twin"
    INLINE_THREE = "inline_three"
    INLINE_FOUR = "inline_four"
    V_FOUR = "v_four"
    FLAT_TWIN = "flat_twin"
    TRIPLE = "triple"

class TransmissionType(enum.Enum):
    MANUAL = "manual"
    AUTOMATIC = "automatic"
    CVT = "cvt"
    SEMI_AUTOMATIC = "semi_automatic"

class FuelType(enum.Enum):
    GASOLINE = "gasoline"
    ELECTRIC = "electric"
    HYBRID = "hybrid"

class DriveType(enum.Enum):
    CHAIN = "chain"
    BELT = "belt"
    SHAFT = "shaft"

class ConditionEnum(enum.Enum):
    NEW = "new"
    LIKE_NEW = "like_new"
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    PROJECT_BIKE = "project_bike"

class SellerTypeEnum(enum.Enum):
    PRIVATE = "private"
    DEALER = "dealer"

class MotorcycleCategory(Base):
    __tablename__ = "motorcycle_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    icon = Column(String(255))
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    motorcycles = relationship("Motorcycle", back_populates="category")


class Motorcycle(Base):
    __tablename__ = "motorcycles"
    
    # Primary key using UUID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Basic Information
    title = Column(String(200), nullable=False)
    description = Column(Text)
    brand = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)
    price = Column(DECIMAL(12, 2), nullable=False)
    
    # Motorcycle Type and Condition
    motorcycle_type = Column(String(50), nullable=False)
    condition = Column(String(50), nullable=False)
    seller_type = Column(String(50), default='private')
    
    # Engine Specifications
    engine_size = Column(Integer)  # CC
    engine_type = Column(String(50))
    horsepower = Column(Integer)  # HP
    torque = Column(Integer)  # Nm
    fuel_type = Column(String(50), default='gasoline')
    fuel_capacity = Column(Float)  # Liters
    fuel_consumption = Column(Float)  # L/100km
    
    # Transmission and Drive
    transmission_type = Column(String(50), default='manual')
    gears = Column(Integer)
    drive_type = Column(String(50), default='chain')
    
    # Physical Specifications
    weight_dry = Column(Integer)  # kg
    weight_wet = Column(Integer)  # kg
    seat_height = Column(Integer)  # mm
    wheelbase = Column(Integer)  # mm
    ground_clearance = Column(Integer)  # mm
    
    # Performance
    top_speed = Column(Integer)  # km/h
    acceleration_0_100 = Column(Float)  # seconds
    
    # Mileage and History
    mileage = Column(Integer)  # KM
    previous_owners = Column(Integer, default=1)
    service_history = Column(Boolean, default=False)
    accident_history = Column(Boolean, default=False)
    
    # Features and Equipment
    abs = Column(Boolean, default=False)
    traction_control = Column(Boolean, default=False)
    cruise_control = Column(Boolean, default=False)
    heated_grips = Column(Boolean, default=False)
    windshield = Column(Boolean, default=False)
    luggage_rack = Column(Boolean, default=False)
    crash_bars = Column(Boolean, default=False)
    
    # Additional Equipment
    accessories = Column(ARRAY(String), default=[])
    modifications = Column(Text)
    
    # Location
    city = Column(String(100))
    postal_code = Column(String(10))
    address = Column(String(255))
    location = Column(Geometry('POINT'))
    
    # Registration and Legal
    registration_number = Column(String(20))
    first_registration = Column(DateTime)
    inspection_valid_until = Column(DateTime)
    insurance_class = Column(String(50))
    
    # Pricing and Financing
    original_price = Column(DECIMAL(12, 2))
    negotiable = Column(Boolean, default=True)
    trade_in_accepted = Column(Boolean, default=False)
    financing_available = Column(Boolean, default=False)
    
    # Status and Visibility
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    is_sold = Column(Boolean, default=False)
    views_count = Column(Integer, default=0)
    favorites_count = Column(Integer, default=0)
    
    # Seller Information
    seller_id = Column(UUID(as_uuid=True))  # References user in auth service
    dealer_id = Column(UUID(as_uuid=True))  # References dealer if applicable
    
    # Relationships
    category_id = Column(Integer, ForeignKey("motorcycle_categories.id"))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    sold_at = Column(DateTime(timezone=True))
    
    # Relationships
    category = relationship("MotorcycleCategory", back_populates="motorcycles")
    images = relationship("MotorcycleImage", back_populates="motorcycle", cascade="all, delete-orphan")
    specifications = relationship("MotorcycleSpecification", back_populates="motorcycle", cascade="all, delete-orphan")
    inspections = relationship("MotorcycleInspection", back_populates="motorcycle", cascade="all, delete-orphan")
    price_history = relationship("MotorcyclePriceHistory", back_populates="motorcycle", cascade="all, delete-orphan")
    views = relationship("MotorcycleView", back_populates="motorcycle", cascade="all, delete-orphan")
    
    # Indexes for better performance
    __table_args__ = (
        Index('idx_motorcycle_brand_model', 'brand', 'model'),
        Index('idx_motorcycle_price', 'price'),
        Index('idx_motorcycle_year', 'year'),
        Index('idx_motorcycle_type', 'motorcycle_type'),
        Index('idx_motorcycle_location', 'city'),
        Index('idx_motorcycle_created', 'created_at'),
        Index('idx_motorcycle_active', 'is_active'),
    )

class MotorcycleImage(Base):
    __tablename__ = "motorcycle_images"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    motorcycle_id = Column(UUID(as_uuid=True), ForeignKey("motorcycles.id", ondelete="CASCADE"))
    image_url = Column(String(500), nullable=False)
    is_primary = Column(Boolean, default=False)
    alt_text = Column(String(255))
    image_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    motorcycle = relationship("Motorcycle", back_populates="images")

class MotorcycleSpecification(Base):
    __tablename__ = "motorcycle_specifications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    motorcycle_id = Column(UUID(as_uuid=True), ForeignKey("motorcycles.id", ondelete="CASCADE"))
    
    # Detailed Engine Specs
    engine_configuration = Column(String(100))  # e.g., "Liquid-cooled, 4-stroke"
    bore_stroke = Column(String(50))  # e.g., "81.0 x 48.5 mm"
    compression_ratio = Column(String(20))  # e.g., "12.8:1"
    valve_system = Column(String(100))  # e.g., "DOHC, 4 valves per cylinder"
    
    # Electrical System
    ignition_system = Column(String(100))
    starting_system = Column(String(50))  # Electric/Kick
    battery = Column(String(50))  # e.g., "12V 8.6Ah"
    
    # Suspension
    front_suspension = Column(String(200))
    rear_suspension = Column(String(200))
    front_travel = Column(Integer)  # mm
    rear_travel = Column(Integer)  # mm
    
    # Brakes
    front_brake = Column(String(200))
    rear_brake = Column(String(200))
    brake_assist = Column(Boolean, default=False)
    
    # Wheels and Tires
    front_tire = Column(String(50))  # e.g., "120/70ZR17"
    rear_tire = Column(String(50))   # e.g., "190/50ZR17"
    front_rim = Column(String(50))   # e.g., "17 x 3.50"
    rear_rim = Column(String(50))    # e.g., "17 x 5.50"
    
    # Colors and Options
    available_colors = Column(ARRAY(String))
    optional_equipment = Column(ARRAY(String))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    motorcycle = relationship("Motorcycle", back_populates="specifications")

class MotorcycleInspection(Base):
    __tablename__ = "motorcycle_inspections"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    motorcycle_id = Column(UUID(as_uuid=True), ForeignKey("motorcycles.id", ondelete="CASCADE"))
    
    inspection_date = Column(DateTime, nullable=False)
    inspection_type = Column(String(50))  # annual, pre_purchase, damage
    inspector_name = Column(String(100))
    inspector_certification = Column(String(100))
    
    # Inspection Results
    overall_condition = Column(String(20))  # excellent, good, fair, poor
    engine_condition = Column(String(20))
    transmission_condition = Column(String(20))
    brake_condition = Column(String(20))
    tire_condition = Column(String(20))
    electrical_condition = Column(String(20))
    
    # Detailed Findings
    findings = Column(Text)
    recommendations = Column(Text)
    estimated_repair_cost = Column(DECIMAL(10, 2))
    
    # Documentation
    report_url = Column(String(500))
    images = Column(ARRAY(String))
    
    is_passed = Column(Boolean)
    valid_until = Column(DateTime)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    motorcycle = relationship("Motorcycle", back_populates="inspections")

class MotorcyclePriceHistory(Base):
    __tablename__ = "motorcycle_price_history"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    motorcycle_id = Column(UUID(as_uuid=True), ForeignKey("motorcycles.id", ondelete="CASCADE"))
    
    old_price = Column(DECIMAL(12, 2))
    new_price = Column(DECIMAL(12, 2), nullable=False)
    change_reason = Column(String(100))  # price_drop, market_adjustment, negotiation
    changed_by = Column(UUID(as_uuid=True))  # user who made the change
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    motorcycle = relationship("Motorcycle", back_populates="price_history")

class MotorcycleView(Base):
    __tablename__ = "motorcycle_views"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    motorcycle_id = Column(UUID(as_uuid=True), ForeignKey("motorcycles.id", ondelete="CASCADE"))
    
    viewer_id = Column(UUID(as_uuid=True))  # null for anonymous views
    ip_address = Column(String(45))  # IPv4 or IPv6
    user_agent = Column(String(500))
    referrer = Column(String(500))
    
    # View details
    view_duration = Column(Integer)  # seconds
    viewed_images = Column(ARRAY(String))
    contacted_seller = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    motorcycle = relationship("Motorcycle", back_populates="views")
    
    __table_args__ = (
        Index('idx_motorcycle_views_date', 'created_at'),
        Index('idx_motorcycle_views_motorcycle', 'motorcycle_id'),
    )

class MotorcycleComparison(Base):
    __tablename__ = "motorcycle_comparisons"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True))  # References user in auth service
    session_id = Column(String(100))  # For anonymous users
    
    motorcycle_ids = Column(ARRAY(String))  # Array of motorcycle UUIDs
    comparison_name = Column(String(200))
    is_public = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class MotorcycleAlert(Base):
    __tablename__ = "motorcycle_alerts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=False)  # References user in auth service
    
    # Alert criteria
    alert_name = Column(String(200), nullable=False)
    brand = Column(String(100))
    model = Column(String(100))
    motorcycle_type = Column(String(50))
    price_min = Column(DECIMAL(12, 2))
    price_max = Column(DECIMAL(12, 2))
    year_min = Column(Integer)
    year_max = Column(Integer)
    mileage_max = Column(Integer)
    engine_size_min = Column(Integer)
    engine_size_max = Column(Integer)
    city = Column(String(100))
    radius_km = Column(Integer, default=50)
    
    # Alert settings
    is_active = Column(Boolean, default=True)
    email_notifications = Column(Boolean, default=True)
    push_notifications = Column(Boolean, default=True)
    frequency = Column(String(20), default='immediate')  # immediate, daily, weekly
    
    # Statistics
    matches_found = Column(Integer, default=0)
    last_match_date = Column(DateTime)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class MotorcycleReport(Base):
    __tablename__ = "motorcycle_reports"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    motorcycle_id = Column(UUID(as_uuid=True), ForeignKey("motorcycles.id", ondelete="CASCADE"))
    reporter_id = Column(UUID(as_uuid=True))  # References user in auth service
    
    report_type = Column(String(50), nullable=False)  # fraud, inappropriate, spam, sold
    reason = Column(String(200))
    description = Column(Text)
    evidence_urls = Column(ARRAY(String))  # Screenshots, documents
    
    status = Column(String(20), default='pending')  # pending, reviewed, resolved, dismissed
    admin_notes = Column(Text)
    resolved_by = Column(UUID(as_uuid=True))
    resolved_at = Column(DateTime)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    motorcycle = relationship("Motorcycle")

class MotorcycleFinancing(Base):
    __tablename__ = "motorcycle_financing"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    motorcycle_id = Column(UUID(as_uuid=True), ForeignKey("motorcycles.id", ondelete="CASCADE"))
    
    # Financing options
    provider_name = Column(String(100), nullable=False)
    provider_logo = Column(String(500))
    min_down_payment = Column(DECIMAL(10, 2))
    max_loan_amount = Column(DECIMAL(12, 2))
    min_interest_rate = Column(DECIMAL(5, 2))
    max_interest_rate = Column(DECIMAL(5, 2))
    min_term_months = Column(Integer)
    max_term_months = Column(Integer)
    
    # Requirements
    min_credit_score = Column(Integer)
    min_income = Column(DECIMAL(10, 2))
    employment_required = Column(Boolean, default=True)
    
    # Features
    pre_approval_available = Column(Boolean, default=False)
    online_application = Column(Boolean, default=True)
    same_day_approval = Column(Boolean, default=False)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    motorcycle = relationship("Motorcycle")

class UserFavoriteMotorcycle(Base):
    __tablename__ = 'user_favorite_motorcycles'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=False)  # References user in auth service
    motorcycle_id = Column(UUID(as_uuid=True), ForeignKey('motorcycles.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    motorcycle = relationship("Motorcycle", backref="favorited_by")
    
    # Ensure a user can only favorite a motorcycle once
    __table_args__ = (
        Index('idx_user_motorcycle_unique', 'user_id', 'motorcycle_id', unique=True),
    )

class MotorcycleMarketStats(Base):
    __tablename__ = "motorcycle_market_stats"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Market segment
    brand = Column(String(100))
    model = Column(String(100))
    year = Column(Integer)
    motorcycle_type = Column(String(50))
    engine_size_range = Column(String(50))  # e.g., "600-750cc"
    
    # Statistics
    average_price = Column(DECIMAL(12, 2))
    median_price = Column(DECIMAL(12, 2))
    min_price = Column(DECIMAL(12, 2))
    max_price = Column(DECIMAL(12, 2))
    price_trend = Column(String(20))  # increasing, decreasing, stable
    
    # Market activity
    listings_count = Column(Integer)
    sold_count = Column(Integer)
    average_days_on_market = Column(Integer)
    
    # Regional data
    city = Column(String(100))
    region = Column(String(100))
    
    # Time period
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        Index('idx_market_stats_brand_model', 'brand', 'model'),
        Index('idx_market_stats_period', 'period_start', 'period_end'),
    )