from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum, Table, Text, Index, DECIMAL
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
import enum
import uuid
from datetime import datetime

Base = declarative_base()

# Association table for many-to-many relationship between boats and features
boat_feature_association = Table(
    'boat_feature_association',
    Base.metadata,
    Column('boat_id', UUID(as_uuid=True), ForeignKey('boats.id'), primary_key=True),
    Column('feature_id', UUID(as_uuid=True), ForeignKey('boat_features.id'), primary_key=True)
)

# Comprehensive Boat Enums for Finn.no features

class BoatType(enum.Enum):
    MOTOR_YACHT = "motor_yacht"
    SAILING_YACHT = "sailing_yacht"
    CATAMARAN = "catamaran"
    SPEEDBOAT = "speedboat"
    FISHING_BOAT = "fishing_boat"
    PONTOON_BOAT = "pontoon_boat"
    CABIN_CRUISER = "cabin_cruiser"
    BOWRIDER = "bowrider"
    CENTER_CONSOLE = "center_console"
    DECK_BOAT = "deck_boat"
    DINGHY = "dinghy"
    INFLATABLE = "inflatable"
    JET_SKI = "jet_ski"
    KAYAK = "kayak"
    CANOE = "canoe"
    HOUSEBOAT = "houseboat"
    TRAWLER = "trawler"
    SAILBOAT = "sailboat"
    RUNABOUT = "runabout"
    BASS_BOAT = "bass_boat"

class BoatCondition(enum.Enum):
    NEW = "new"
    LIKE_NEW = "like_new"
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    PROJECT_BOAT = "project_boat"
    RESTORATION = "restoration"

class HullMaterial(enum.Enum):
    FIBERGLASS = "fiberglass"
    ALUMINUM = "aluminum"
    WOOD = "wood"
    STEEL = "steel"
    CARBON_FIBER = "carbon_fiber"
    COMPOSITE = "composite"
    INFLATABLE = "inflatable"
    CONCRETE = "concrete"
    PLASTIC = "plastic"

class HullType(enum.Enum):
    MONOHULL = "monohull"
    CATAMARAN = "catamaran"
    TRIMARAN = "trimaran"
    DEEP_V = "deep_v"
    FLAT_BOTTOM = "flat_bottom"
    SEMI_DISPLACEMENT = "semi_displacement"
    DISPLACEMENT = "displacement"
    PLANING = "planing"

class EngineType(enum.Enum):
    OUTBOARD = "outboard"
    INBOARD = "inboard"
    STERNDRIVE = "sterndrive"
    JET_DRIVE = "jet_drive"
    ELECTRIC = "electric"
    HYBRID = "hybrid"
    SAIL_ONLY = "sail_only"

class FuelType(enum.Enum):
    GASOLINE = "gasoline"
    DIESEL = "diesel"
    ELECTRIC = "electric"
    HYBRID = "hybrid"
    NONE = "none"

class PropulsionType(enum.Enum):
    SINGLE_ENGINE = "single_engine"
    TWIN_ENGINE = "twin_engine"
    TRIPLE_ENGINE = "triple_engine"
    QUAD_ENGINE = "quad_engine"
    SAIL = "sail"
    ELECTRIC_MOTOR = "electric_motor"

class SellerType(enum.Enum):
    PRIVATE = "private"
    DEALER = "dealer"
    MANUFACTURER = "manufacturer"
    BROKER = "broker"

class AdType(enum.Enum):
    FOR_SALE = "for_sale"
    FOR_RENT = "for_rent"
    CHARTER = "charter"
    WANTED = "wanted"
    BERTH_RENTAL = "berth_rental"

class MooringType(enum.Enum):
    MARINA_BERTH = "marina_berth"
    MOORING_BUOY = "mooring_buoy"
    ANCHOR = "anchor"
    DRY_STORAGE = "dry_storage"
    TRAILER = "trailer"
    BEACH = "beach"

class FixRequestStatus(enum.Enum):
    REQUESTED = "requested"
    APPROVED = "approved"
    DECLINED = "declined"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class BoatCategory(Base):
    __tablename__ = 'boat_categories'

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String(255), nullable=False)
    icon = Column(String(255))
    parent_id = Column(Integer, ForeignKey('boat_categories.id', ondelete='CASCADE'), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    children = relationship("BoatCategory", 
                           backref=backref('parent', remote_side=[id]),
                           cascade="all")  # Remove delete-orphan, or add single_parent=True
    boats = relationship("Boat", back_populates="category")
    
class BoatFeature(Base):
    __tablename__ = 'boat_features'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    boats = relationship("Boat", secondary=boat_feature_association, back_populates="features")

class Boat(Base):
    __tablename__ = 'boats'
    
    # Primary key using UUID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Basic Information
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    price = Column(DECIMAL(12, 2), nullable=False)
    original_price = Column(DECIMAL(12, 2))
    negotiable = Column(Boolean, default=True)
    
    # Boat Classification
    category_id = Column(Integer, ForeignKey('boat_categories.id'), nullable=False)
    boat_type = Column(String(100), nullable=False)
    condition = Column(String(50), default='good')
    year = Column(Integer)
    make = Column(String(100))
    model = Column(String(100))
    
    # Physical Specifications
    length_overall = Column(Float)  # LOA in meters
    length_waterline = Column(Float)  # LWL in meters
    beam = Column(Float)  # Width in meters
    draft = Column(Float)  # Depth below waterline in meters
    displacement = Column(Integer)  # Weight in kg
    ballast = Column(Integer)  # Ballast weight in kg
    
    # Hull Specifications
    hull_material = Column(String(50))
    hull_type = Column(String(50))
    hull_color = Column(String(50))
    hull_design = Column(String(100))  # Designer name
    
    # Engine and Propulsion
    engine_type = Column(String(50))
    propulsion_type = Column(String(50))
    fuel_type = Column(String(50), default='gasoline')
    number_of_engines = Column(Integer, default=1)
    engine_make = Column(String(100))
    engine_model = Column(String(100))
    engine_hours = Column(Integer)
    engine_power = Column(Integer)  # Total power in HP
    engine_year = Column(Integer)
    
    # Fuel and Tanks
    fuel_capacity = Column(Integer)  # Liters
    fresh_water_capacity = Column(Integer)  # Liters
    waste_water_capacity = Column(Integer)  # Liters
    
    # Accommodation
    berths = Column(Integer)  # Number of sleeping berths
    cabins = Column(Integer)  # Number of cabins
    heads = Column(Integer)  # Number of toilets/bathrooms
    
    # Sailing Specifications (for sailboats)
    sail_area = Column(Float)  # Square meters
    mast_height = Column(Float)  # Meters above waterline
    keel_type = Column(String(50))  # fin, full, wing, etc.
    
    # Equipment and Features
    navigation_equipment = Column(ARRAY(String))
    safety_equipment = Column(ARRAY(String))
    comfort_features = Column(ARRAY(String))
    electronics = Column(ARRAY(String))
    
    # Mooring and Location
    current_location = Column(String(200))
    home_port = Column(String(100))
    mooring_type = Column(String(50))
    mooring_included = Column(Boolean, default=False)
    mooring_cost_annual = Column(DECIMAL(10, 2))
    
    # Legal and Documentation
    registration_number = Column(String(50))
    registration_country = Column(String(50))
    vat_paid = Column(Boolean, default=False)
    ce_certification = Column(Boolean, default=False)
    insurance_valid_until = Column(DateTime)
    
    # History and Maintenance
    previous_owners = Column(Integer, default=1)
    service_history = Column(Boolean, default=False)
    recent_survey = Column(Boolean, default=False)
    survey_date = Column(DateTime)
    major_refit_year = Column(Integer)
    
    # Commercial Information
    seller_type = Column(String(50), default='private')
    ad_type = Column(String(50), default='for_sale')
    broker_name = Column(String(100))
    broker_contact = Column(String(200))
    
    # Charter Information (if for charter)
    charter_price_daily = Column(DECIMAL(10, 2))
    charter_price_weekly = Column(DECIMAL(10, 2))
    charter_available_from = Column(DateTime)
    charter_available_to = Column(DateTime)
    charter_includes = Column(ARRAY(String))
    
    # Status and Visibility
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    is_sold = Column(Boolean, default=False)
    status = Column(String(50), default="active")
    views_count = Column(Integer, default=0)
    favorites_count = Column(Integer, default=0)
    
    # Location
    location = Column(Geometry('POINT', srid=4326))
    location_name = Column(String(255))
    city = Column(String(100))
    country = Column(String(100))
    postal_code = Column(String(20))
    
    # User Information
    seller_id = Column(UUID(as_uuid=True))  # References user in auth service
    dealer_id = Column(UUID(as_uuid=True))  # References dealer if applicable
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    sold_at = Column(DateTime)
    
    # Relationships
    category = relationship("BoatCategory", back_populates="boats")
    images = relationship("BoatImage", back_populates="boat", cascade="all, delete-orphan")
    features = relationship("BoatFeature", secondary=boat_feature_association, back_populates="boats")
    specifications = relationship("BoatSpecification", back_populates="boat", cascade="all, delete-orphan")
    inspections = relationship("BoatInspection", back_populates="boat", cascade="all, delete-orphan")
    price_history = relationship("BoatPriceHistory", back_populates="boat", cascade="all, delete-orphan")
    views = relationship("BoatView", back_populates="boat", cascade="all, delete-orphan")
    
    # Indexes for better performance
    __table_args__ = (
        Index('idx_boat_make_model', 'make', 'model'),
        Index('idx_boat_price', 'price'),
        Index('idx_boat_year', 'year'),
        Index('idx_boat_type', 'boat_type'),
        Index('idx_boat_location', 'city'),
        Index('idx_boat_created', 'created_at'),
        Index('idx_boat_active', 'is_active'),
    )

class BoatImage(Base):
    __tablename__ = 'boat_images'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    boat_id = Column(UUID(as_uuid=True), ForeignKey('boats.id', ondelete='CASCADE'), nullable=False)
    image_url = Column(String(500), nullable=False)
    is_primary = Column(Boolean, default=False)
    alt_text = Column(String(255))
    image_order = Column(Integer, default=0)
    image_category = Column(String(50))  # exterior, interior, engine, equipment
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    boat = relationship("Boat", back_populates="images")

class BoatSpecification(Base):
    __tablename__ = 'boat_specifications'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    boat_id = Column(UUID(as_uuid=True), ForeignKey('boats.id', ondelete='CASCADE'), nullable=False)
    
    # Detailed Engine Specifications
    engine_configuration = Column(String(100))  # V8, Inline-6, etc.
    engine_displacement = Column(Float)  # Liters
    engine_cooling = Column(String(50))  # Fresh water, raw water, air
    transmission = Column(String(100))
    propeller_type = Column(String(100))
    propeller_material = Column(String(50))
    
    # Electrical System
    electrical_system = Column(String(50))  # 12V, 24V, etc.
    battery_capacity = Column(String(50))
    shore_power = Column(String(50))
    generator = Column(String(100))
    inverter = Column(String(100))
    
    # Plumbing and Water Systems
    fresh_water_system = Column(String(200))
    hot_water_system = Column(String(200))
    waste_system = Column(String(200))
    bilge_pumps = Column(String(200))
    
    # Heating and Cooling
    heating_system = Column(String(200))
    air_conditioning = Column(String(200))
    
    # Construction Details
    construction_method = Column(String(200))
    deck_material = Column(String(100))
    interior_material = Column(String(100))
    
    # Performance Data
    max_speed = Column(Float)  # Knots
    cruise_speed = Column(Float)  # Knots
    fuel_consumption = Column(Float)  # Liters per hour
    range_nautical_miles = Column(Integer)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    boat = relationship("Boat", back_populates="specifications")

class BoatInspection(Base):
    __tablename__ = 'boat_inspections'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    boat_id = Column(UUID(as_uuid=True), ForeignKey('boats.id', ondelete='CASCADE'), nullable=False)
    
    inspection_date = Column(DateTime, nullable=False)
    inspection_type = Column(String(50))  # survey, insurance, pre_purchase
    surveyor_name = Column(String(100))
    surveyor_certification = Column(String(100))
    
    # Inspection Results
    overall_condition = Column(String(20))  # excellent, good, fair, poor
    hull_condition = Column(String(20))
    engine_condition = Column(String(20))
    electrical_condition = Column(String(20))
    plumbing_condition = Column(String(20))
    safety_equipment_condition = Column(String(20))
    
    # Detailed Findings
    findings = Column(Text)
    recommendations = Column(Text)
    estimated_repair_cost = Column(DECIMAL(10, 2))
    estimated_value = Column(DECIMAL(12, 2))
    
    # Documentation
    report_url = Column(String(500))
    images = Column(ARRAY(String))
    
    is_passed = Column(Boolean)
    valid_until = Column(DateTime)
    
    created_at = Column(DateTime, default=func.now())
    
    boat = relationship("Boat", back_populates="inspections")

class BoatPriceHistory(Base):
    __tablename__ = 'boat_price_history'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    boat_id = Column(UUID(as_uuid=True), ForeignKey('boats.id', ondelete='CASCADE'), nullable=False)
    
    old_price = Column(DECIMAL(12, 2))
    new_price = Column(DECIMAL(12, 2), nullable=False)
    change_reason = Column(String(100))  # price_drop, market_adjustment, negotiation
    changed_by = Column(UUID(as_uuid=True))  # user who made the change
    
    created_at = Column(DateTime, default=func.now())
    
    boat = relationship("Boat", back_populates="price_history")

class BoatView(Base):
    __tablename__ = 'boat_views'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    boat_id = Column(UUID(as_uuid=True), ForeignKey('boats.id', ondelete='CASCADE'), nullable=False)
    
    viewer_id = Column(UUID(as_uuid=True))  # null for anonymous views
    ip_address = Column(String(45))  # IPv4 or IPv6
    user_agent = Column(String(500))
    referrer = Column(String(500))
    
    # View details
    view_duration = Column(Integer)  # seconds
    viewed_images = Column(ARRAY(String))
    contacted_seller = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=func.now())
    
    boat = relationship("Boat", back_populates="views")
    
    __table_args__ = (
        Index('idx_boat_views_date', 'created_at'),
        Index('idx_boat_views_boat', 'boat_id'),
    )

class BoatAlert(Base):
    __tablename__ = 'boat_alerts'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=False)  # References user in auth service
    
    # Alert criteria
    alert_name = Column(String(200), nullable=False)
    boat_type = Column(String(100))
    make = Column(String(100))
    model = Column(String(100))
    price_min = Column(DECIMAL(12, 2))
    price_max = Column(DECIMAL(12, 2))
    year_min = Column(Integer)
    year_max = Column(Integer)
    length_min = Column(Float)
    length_max = Column(Float)
    engine_power_min = Column(Integer)
    engine_power_max = Column(Integer)
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
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class BoatComparison(Base):
    __tablename__ = 'boat_comparisons'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True))  # References user in auth service
    session_id = Column(String(100))  # For anonymous users
    
    boat_ids = Column(ARRAY(String))  # Array of boat UUIDs
    comparison_name = Column(String(200))
    is_public = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class BoatReport(Base):
    __tablename__ = 'boat_reports'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    boat_id = Column(UUID(as_uuid=True), ForeignKey('boats.id', ondelete='CASCADE'), nullable=False)
    reporter_id = Column(UUID(as_uuid=True))  # References user in auth service
    
    report_type = Column(String(50), nullable=False)  # fraud, inappropriate, spam, sold
    reason = Column(String(200))
    description = Column(Text)
    evidence_urls = Column(ARRAY(String))  # Screenshots, documents
    
    status = Column(String(20), default='pending')  # pending, reviewed, resolved, dismissed
    admin_notes = Column(Text)
    resolved_by = Column(UUID(as_uuid=True))
    resolved_at = Column(DateTime)
    
    created_at = Column(DateTime, default=func.now())
    
    boat = relationship("Boat")

class BoatMarketStats(Base):
    __tablename__ = 'boat_market_stats'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Market segment
    boat_type = Column(String(100))
    make = Column(String(100))
    model = Column(String(100))
    year = Column(Integer)
    length_range = Column(String(50))  # e.g., "20-25ft"
    
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
    country = Column(String(100))
    
    # Time period
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    
    created_at = Column(DateTime, default=func.now())
    
    __table_args__ = (
        Index('idx_boat_market_stats_type_make', 'boat_type', 'make'),
        Index('idx_boat_market_stats_period', 'period_start', 'period_end'),
    )

class UserFavoriteBoat(Base):
    __tablename__ = 'user_favorite_boats'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=False)  # References user in auth service
    boat_id = Column(UUID(as_uuid=True), ForeignKey('boats.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    boat = relationship("Boat", backref="favorited_by")
    
    # Ensure a user can only favorite a boat once
    __table_args__ = (
        Index('idx_user_boat_unique', 'user_id', 'boat_id', unique=True),
    )

class BoatFinancing(Base):
    __tablename__ = 'boat_financing'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    boat_id = Column(UUID(as_uuid=True), ForeignKey('boats.id', ondelete='CASCADE'), nullable=False)
    
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
    created_at = Column(DateTime, default=func.now())
    
    boat = relationship("Boat")

class Marina(Base):
    __tablename__ = 'marinas'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Basic Information
    name = Column(String(200), nullable=False)
    description = Column(Text)
    website = Column(String(500))
    phone = Column(String(50))
    email = Column(String(200))
    
    # Location
    address = Column(String(500))
    city = Column(String(100))
    postal_code = Column(String(20))
    country = Column(String(100))
    location = Column(Geometry('POINT', srid=4326))
    
    # Marina Details
    total_berths = Column(Integer)
    available_berths = Column(Integer)
    max_boat_length = Column(Float)  # meters
    max_draft = Column(Float)  # meters
    
    # Facilities
    facilities = Column(ARRAY(String))  # fuel, water, electricity, wifi, etc.
    services = Column(ARRAY(String))  # maintenance, storage, etc.
    
    # Pricing
    daily_rate = Column(DECIMAL(8, 2))
    weekly_rate = Column(DECIMAL(8, 2))
    monthly_rate = Column(DECIMAL(8, 2))
    annual_rate = Column(DECIMAL(10, 2))
    
    # Status
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())