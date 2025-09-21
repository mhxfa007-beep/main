# File: job-service/src/models/job_models.py

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey, Enum, JSON, DECIMAL, Index, Table
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
from ..database.database import Base
import enum
import uuid
# Add missing imports for relationships
from .analytics_models import JobAnalytics, UserJobInteraction

class CompanyFollow(Base):
    __tablename__ = 'company_follows'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    followed_at = Column(DateTime, default=func.now())
    
    # Relationships
    company = relationship("Company", backref="followers")

# Comprehensive Job Enums for Finn.no features

class JobType(enum.Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time" 
    CONTRACT = "contract"
    TEMPORARY = "temporary"
    INTERNSHIP = "internship"
    FREELANCE = "freelance"
    APPRENTICESHIP = "apprenticeship"
    SEASONAL = "seasonal"
    REMOTE = "remote"
    HYBRID = "hybrid"

class ExperienceLevel(enum.Enum):
    ENTRY = "entry"
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    EXECUTIVE = "executive"
    DIRECTOR = "director"
    VP = "vp"
    C_LEVEL = "c_level"

class JobStatus(enum.Enum):
    ACTIVE = "active"
    CLOSED = "closed"
    DRAFT = "draft"
    PAUSED = "paused"
    EXPIRED = "expired"
    FILLED = "filled"

class WorkArrangement(enum.Enum):
    ON_SITE = "on_site"
    REMOTE = "remote"
    HYBRID = "hybrid"
    FLEXIBLE = "flexible"

class SalaryType(enum.Enum):
    HOURLY = "hourly"
    DAILY = "daily"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    PROJECT = "project"

class CompanySize(enum.Enum):
    STARTUP = "startup"  # 1-10
    SMALL = "small"      # 11-50
    MEDIUM = "medium"    # 51-200
    LARGE = "large"      # 201-1000
    ENTERPRISE = "enterprise"  # 1000+

class IndustryType(enum.Enum):
    TECHNOLOGY = "technology"
    FINANCE = "finance"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"
    RETAIL = "retail"
    MANUFACTURING = "manufacturing"
    CONSULTING = "consulting"
    MEDIA = "media"
    GOVERNMENT = "government"
    NON_PROFIT = "non_profit"
    ENERGY = "energy"
    REAL_ESTATE = "real_estate"
    TRANSPORTATION = "transportation"
    HOSPITALITY = "hospitality"
    AGRICULTURE = "agriculture"
    CONSTRUCTION = "construction"
    TELECOMMUNICATIONS = "telecommunications"
    AUTOMOTIVE = "automotive"
    AEROSPACE = "aerospace"
    PHARMACEUTICAL = "pharmaceutical"

class ApplicationStatus(enum.Enum):
    APPLIED = "applied"
    VIEWED = "viewed"
    SHORTLISTED = "shortlisted"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    INTERVIEWED = "interviewed"
    OFFER_MADE = "offer_made"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"

class BenefitType(enum.Enum):
    HEALTH_INSURANCE = "health_insurance"
    DENTAL_INSURANCE = "dental_insurance"
    VISION_INSURANCE = "vision_insurance"
    RETIREMENT_PLAN = "retirement_plan"
    PAID_TIME_OFF = "paid_time_off"
    FLEXIBLE_SCHEDULE = "flexible_schedule"
    REMOTE_WORK = "remote_work"
    PROFESSIONAL_DEVELOPMENT = "professional_development"
    GYM_MEMBERSHIP = "gym_membership"
    STOCK_OPTIONS = "stock_options"
    BONUS = "bonus"
    COMPANY_CAR = "company_car"
    MEAL_ALLOWANCE = "meal_allowance"
    CHILDCARE = "childcare"
    RELOCATION_ASSISTANCE = "relocation_assistance"

class Company(Base):
    __tablename__ = 'companies'
    
    # Primary key using UUID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Basic Information
    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), nullable=False, unique=True, index=True)
    description = Column(Text)
    short_description = Column(String(500))
    tagline = Column(String(200))
    
    # Contact Information
    website = Column(String(500))
    email = Column(String(255))
    phone = Column(String(50))
    
    # Visual Identity
    logo_url = Column(String(500))
    cover_image_url = Column(String(500))
    brand_colors = Column(JSON)  # Primary, secondary colors
    
    # Company Details
    industry = Column(String(100))
    company_size = Column(String(50))
    founded_year = Column(Integer)
    company_type = Column(String(50))  # public, private, startup, non-profit
    
    # Location Information
    headquarters_address = Column(String(500))
    headquarters_city = Column(String(100))
    headquarters_country = Column(String(100))
    headquarters_location = Column(Geometry('POINT', srid=4326))
    office_locations = Column(ARRAY(String))  # Multiple office locations
    
    # Company Culture & Values
    mission_statement = Column(Text)
    vision_statement = Column(Text)
    core_values = Column(ARRAY(String))
    company_culture = Column(Text)
    work_environment = Column(String(50))  # casual, formal, hybrid
    
    # Benefits & Perks
    benefits = Column(ARRAY(String))
    perks = Column(ARRAY(String))
    remote_work_policy = Column(String(50))  # full_remote, hybrid, on_site
    
    # Social Media & Links
    linkedin_url = Column(String(500))
    twitter_url = Column(String(500))
    facebook_url = Column(String(500))
    instagram_url = Column(String(500))
    youtube_url = Column(String(500))
    
    # Company Statistics
    employee_count = Column(Integer)
    annual_revenue = Column(DECIMAL(15, 2))
    revenue_currency = Column(String(3), default='NOK')
    
    # Ratings & Reviews
    overall_rating = Column(Float, default=0.0)
    culture_rating = Column(Float, default=0.0)
    salary_rating = Column(Float, default=0.0)
    benefits_rating = Column(Float, default=0.0)
    management_rating = Column(Float, default=0.0)
    career_rating = Column(Float, default=0.0)
    total_reviews = Column(Integer, default=0)
    
    # Verification & Status
    is_verified = Column(Boolean, default=False)
    is_premium = Column(Boolean, default=False)
    is_hiring = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    
    # SEO & Marketing
    meta_title = Column(String(255))
    meta_description = Column(String(500))
    keywords = Column(ARRAY(String))
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    verified_at = Column(DateTime)
    
    # Relationships
    jobs = relationship("Job", back_populates="company")
    reviews = relationship("CompanyReview", back_populates="company", cascade="all, delete-orphan")
    salary_reports = relationship("SalaryReport", back_populates="company", cascade="all, delete-orphan")
    
    # Indexes for better performance
    __table_args__ = (
        Index('idx_company_name', 'name'),
        Index('idx_company_industry', 'industry'),
        Index('idx_company_size', 'company_size'),
        Index('idx_company_location', 'headquarters_city'),
        Index('idx_company_rating', 'overall_rating'),
        Index('idx_company_active', 'is_active'),
    )

class JobCategory(Base):
    __tablename__ = 'job_categories'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    slug = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    parent_id = Column(Integer, ForeignKey('job_categories.id'), nullable=True)
    is_active = Column(Boolean, default=True)
    icon = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    parent = relationship("JobCategory", remote_side=[id], backref="children")
    jobs = relationship("Job", back_populates="category")

class Job(Base):
    __tablename__ = 'jobs'
    
    # Primary key using UUID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Basic Information
    title = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=False)
    short_description = Column(String(1000))
    summary = Column(String(500))  # Brief job summary
    
    # Detailed Job Information
    requirements = Column(Text)
    responsibilities = Column(Text)
    qualifications = Column(Text)
    preferred_qualifications = Column(Text)
    benefits = Column(Text)
    company_culture_fit = Column(Text)
    
    # Job Classification
    job_type = Column(String(50), nullable=False)
    experience_level = Column(String(50), nullable=False)
    seniority_level = Column(String(50))
    department = Column(String(100))
    team = Column(String(100))
    
    # Work Arrangement
    work_arrangement = Column(String(50), default='on_site')
    remote_work_percentage = Column(Integer, default=0)  # 0-100%
    travel_requirement = Column(String(50))  # none, occasional, frequent
    
    # Salary Information
    salary_min = Column(DECIMAL(12, 2))
    salary_max = Column(DECIMAL(12, 2))
    salary_currency = Column(String(3), default="NOK")
    salary_type = Column(String(20), default='yearly')
    is_salary_negotiable = Column(Boolean, default=True)
    is_salary_public = Column(Boolean, default=False)
    
    # Additional Compensation
    bonus_structure = Column(String(200))
    equity_offered = Column(Boolean, default=False)
    commission_structure = Column(String(200))
    
    # Location Information
    location = Column(String(255))
    city = Column(String(100))
    state_province = Column(String(100))
    country = Column(String(100))
    postal_code = Column(String(20))
    location_coordinates = Column(Geometry('POINT', srid=4326))
    office_address = Column(String(500))
    
    # Skills and Technologies
    required_skills = Column(ARRAY(String))
    preferred_skills = Column(ARRAY(String))
    technologies = Column(ARRAY(String))
    programming_languages = Column(ARRAY(String))
    tools_software = Column(ARRAY(String))
    certifications = Column(ARRAY(String))
    
    # Education Requirements
    education_level = Column(String(50))  # high_school, bachelor, master, phd
    education_field = Column(String(100))
    education_required = Column(Boolean, default=False)
    
    # Experience Requirements
    years_experience_min = Column(Integer, default=0)
    years_experience_max = Column(Integer)
    industry_experience = Column(ARRAY(String))
    
    # Application Process
    application_deadline = Column(DateTime)
    application_email = Column(String(255))
    application_url = Column(String(500))
    application_instructions = Column(Text)
    contact_person = Column(String(255))
    contact_phone = Column(String(50))
    contact_email = Column(String(255))
    
    # Application Requirements
    requires_cover_letter = Column(Boolean, default=False)
    requires_portfolio = Column(Boolean, default=False)
    requires_references = Column(Boolean, default=False)
    custom_application_fields = Column(JSON)  # Custom form fields
    
    # Job Status and Visibility
    status = Column(String(20), default='active')
    is_featured = Column(Boolean, default=False)
    is_urgent = Column(Boolean, default=False)
    is_confidential = Column(Boolean, default=False)
    visibility = Column(String(20), default='public')  # public, private, internal
    
    # Statistics
    view_count = Column(Integer, default=0)
    application_count = Column(Integer, default=0)
    save_count = Column(Integer, default=0)
    share_count = Column(Integer, default=0)
    
    # SEO and Marketing
    meta_title = Column(String(255))
    meta_description = Column(String(500))
    keywords = Column(ARRAY(String))
    
    # Hiring Process
    hiring_process_steps = Column(ARRAY(String))  # application, phone_screen, interview, etc.
    estimated_hiring_time = Column(String(50))  # 1-2 weeks, 1 month, etc.
    number_of_positions = Column(Integer, default=1)
    
    # Benefits and Perks
    health_benefits = Column(ARRAY(String))
    retirement_benefits = Column(ARRAY(String))
    time_off_benefits = Column(ARRAY(String))
    professional_development = Column(ARRAY(String))
    workplace_perks = Column(ARRAY(String))
    
    # Company Information (denormalized for performance)
    company_name = Column(String(255))
    company_logo_url = Column(String(500))
    company_industry = Column(String(100))
    company_size = Column(String(50))
    
    # Foreign Keys
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('job_categories.id'))
    posted_by = Column(UUID(as_uuid=True))  # User ID from auth service
    recruiter_id = Column(UUID(as_uuid=True))  # Assigned recruiter
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    published_at = Column(DateTime)
    expires_at = Column(DateTime)
    filled_at = Column(DateTime)
    
    # Relationships
    company = relationship("Company", back_populates="jobs")
    category = relationship("JobCategory", back_populates="jobs")
    applications = relationship("JobApplication", back_populates="job", cascade="all, delete-orphan")
    views = relationship("JobView", back_populates="job", cascade="all, delete-orphan")
    saves = relationship("JobSave", back_populates="job", cascade="all, delete-orphan")
    alerts = relationship("JobAlert", back_populates="job", cascade="all, delete-orphan")
    
    # Indexes for better performance
    __table_args__ = (
        Index('idx_job_title', 'title'),
        Index('idx_job_company', 'company_id'),
        Index('idx_job_location', 'city', 'country'),
        Index('idx_job_type', 'job_type'),
        Index('idx_job_experience', 'experience_level'),
        Index('idx_job_salary', 'salary_min', 'salary_max'),
        Index('idx_job_status', 'status'),
        Index('idx_job_created', 'created_at'),
        Index('idx_job_featured', 'is_featured'),
    )

class JobApplication(Base):
    __tablename__ = 'job_applications'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    job_id = Column(UUID(as_uuid=True), ForeignKey('jobs.id'), nullable=False)
    applicant_id = Column(UUID(as_uuid=True), nullable=False)  # User ID from auth service
    
    # Application Data
    cover_letter = Column(Text)
    cv_file_path = Column(String(500))
    portfolio_url = Column(String(500))
    additional_documents = Column(ARRAY(String))
    additional_info = Column(Text)
    
    # Custom Application Fields
    custom_responses = Column(JSON)  # Responses to custom application questions
    
    # Contact Information
    applicant_email = Column(String(255))
    applicant_phone = Column(String(50))
    applicant_name = Column(String(255))
    
    # Status and Tracking
    status = Column(String(50), default="applied")
    stage = Column(String(50))  # application_review, phone_screen, interview, etc.
    priority = Column(String(20), default="normal")  # low, normal, high
    
    # Recruiter Notes
    recruiter_notes = Column(Text)
    internal_rating = Column(Integer)  # 1-5 rating
    tags = Column(ARRAY(String))
    
    # Interview Information
    interview_scheduled_at = Column(DateTime)
    interview_type = Column(String(50))  # phone, video, in_person
    interview_notes = Column(Text)
    
    # Decision Information
    rejection_reason = Column(String(200))
    offer_details = Column(JSON)
    
    # Timestamps
    applied_at = Column(DateTime, default=func.now())
    reviewed_at = Column(DateTime)
    interview_at = Column(DateTime)
    decision_at = Column(DateTime)
    
    # Relationships
    job = relationship("Job", back_populates="applications")
    
    __table_args__ = (
        Index('idx_application_job', 'job_id'),
        Index('idx_application_applicant', 'applicant_id'),
        Index('idx_application_status', 'status'),
        Index('idx_application_date', 'applied_at'),
    )

class JobView(Base):
    __tablename__ = 'job_views'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    job_id = Column(UUID(as_uuid=True), ForeignKey('jobs.id'), nullable=False)
    viewer_id = Column(UUID(as_uuid=True))  # User ID from auth service, nullable for anonymous
    
    # View Details
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    referrer = Column(String(500))
    session_id = Column(String(100))
    
    # View Metrics
    view_duration = Column(Integer)  # seconds
    scroll_depth = Column(Integer)  # percentage
    clicked_apply = Column(Boolean, default=False)
    clicked_save = Column(Boolean, default=False)
    clicked_share = Column(Boolean, default=False)
    
    viewed_at = Column(DateTime, default=func.now())
    
    # Relationships
    job = relationship("Job", back_populates="views")
    
    __table_args__ = (
        Index('idx_job_view_job', 'job_id'),
        Index('idx_job_view_date', 'viewed_at'),
    )

class JobSave(Base):
    __tablename__ = 'job_saves'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    job_id = Column(UUID(as_uuid=True), ForeignKey('jobs.id'), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)  # User ID from auth service
    
    # Save Details
    notes = Column(Text)  # Personal notes about the job
    folder = Column(String(100))  # Organization folder
    
    saved_at = Column(DateTime, default=func.now())
    
    # Relationships
    job = relationship("Job", back_populates="saves")
    
    __table_args__ = (
        Index('idx_job_save_unique', 'job_id', 'user_id', unique=True),
        Index('idx_job_save_user', 'user_id'),
    )

class JobAlert(Base):
    __tablename__ = 'job_alerts'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=False)  # User ID from auth service
    
    # Alert Criteria
    alert_name = Column(String(200), nullable=False)
    keywords = Column(ARRAY(String))
    job_title = Column(String(255))
    company_name = Column(String(255))
    location = Column(String(255))
    remote_only = Column(Boolean, default=False)
    
    # Job Type Filters
    job_types = Column(ARRAY(String))
    experience_levels = Column(ARRAY(String))
    salary_min = Column(DECIMAL(12, 2))
    salary_max = Column(DECIMAL(12, 2))
    
    # Company Filters
    company_sizes = Column(ARRAY(String))
    industries = Column(ARRAY(String))
    
    # Skills and Requirements
    required_skills = Column(ARRAY(String))
    excluded_skills = Column(ARRAY(String))
    
    # Alert Settings
    is_active = Column(Boolean, default=True)
    frequency = Column(String(20), default='immediate')  # immediate, daily, weekly
    email_notifications = Column(Boolean, default=True)
    push_notifications = Column(Boolean, default=True)
    
    # Statistics
    matches_found = Column(Integer, default=0)
    last_match_date = Column(DateTime)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    job = relationship("Job", back_populates="alerts")

class CompanyReview(Base):
    __tablename__ = 'company_reviews'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), nullable=False)
    reviewer_id = Column(UUID(as_uuid=True), nullable=False)  # User ID from auth service
    
    # Review Content
    title = Column(String(255), nullable=False)
    review_text = Column(Text, nullable=False)
    pros = Column(Text)
    cons = Column(Text)
    advice_to_management = Column(Text)
    
    # Ratings (1-5 scale)
    overall_rating = Column(Float, nullable=False)
    culture_rating = Column(Float)
    salary_rating = Column(Float)
    benefits_rating = Column(Float)
    management_rating = Column(Float)
    career_opportunities_rating = Column(Float)
    work_life_balance_rating = Column(Float)
    
    # Reviewer Information
    job_title = Column(String(255))
    employment_status = Column(String(50))  # current, former
    employment_duration = Column(String(50))  # 1-2 years, 3-5 years, etc.
    department = Column(String(100))
    location = Column(String(255))
    
    # Review Status
    is_verified = Column(Boolean, default=False)
    is_anonymous = Column(Boolean, default=True)
    is_approved = Column(Boolean, default=False)
    
    # Helpfulness
    helpful_count = Column(Integer, default=0)
    not_helpful_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    company = relationship("Company", back_populates="reviews")
    
    __table_args__ = (
        Index('idx_company_review_company', 'company_id'),
        Index('idx_company_review_rating', 'overall_rating'),
        Index('idx_company_review_date', 'created_at'),
    )

class SalaryReport(Base):
    __tablename__ = 'salary_reports'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), nullable=False)
    reporter_id = Column(UUID(as_uuid=True))  # User ID from auth service, nullable for anonymous
    
    # Job Information
    job_title = Column(String(255), nullable=False)
    department = Column(String(100))
    experience_level = Column(String(50))
    years_experience = Column(Integer)
    years_at_company = Column(Integer)
    
    # Location
    location = Column(String(255))
    city = Column(String(100))
    country = Column(String(100))
    
    # Salary Information
    base_salary = Column(DECIMAL(12, 2), nullable=False)
    bonus = Column(DECIMAL(12, 2))
    stock_options = Column(DECIMAL(12, 2))
    other_compensation = Column(DECIMAL(12, 2))
    total_compensation = Column(DECIMAL(12, 2))
    currency = Column(String(3), default='NOK')
    
    # Employment Details
    employment_type = Column(String(50))  # full_time, part_time, contract
    work_arrangement = Column(String(50))  # remote, hybrid, on_site
    
    # Additional Information
    education_level = Column(String(50))
    skills = Column(ARRAY(String))
    certifications = Column(ARRAY(String))
    
    # Verification
    is_verified = Column(Boolean, default=False)
    verification_method = Column(String(50))  # email, linkedin, document
    
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    company = relationship("Company", back_populates="salary_reports")
    
    __table_args__ = (
        Index('idx_salary_report_company', 'company_id'),
        Index('idx_salary_report_title', 'job_title'),
        Index('idx_salary_report_salary', 'base_salary'),
        Index('idx_salary_report_location', 'city'),
    )

class JobMarketStats(Base):
    __tablename__ = 'job_market_stats'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Market Segment
    job_title = Column(String(255))
    industry = Column(String(100))
    experience_level = Column(String(50))
    location = Column(String(255))
    city = Column(String(100))
    country = Column(String(100))
    
    # Salary Statistics
    avg_salary = Column(DECIMAL(12, 2))
    median_salary = Column(DECIMAL(12, 2))
    min_salary = Column(DECIMAL(12, 2))
    max_salary = Column(DECIMAL(12, 2))
    salary_trend = Column(String(20))  # increasing, decreasing, stable
    
    # Job Market Activity
    total_jobs = Column(Integer)
    new_jobs_this_month = Column(Integer)
    avg_time_to_fill = Column(Integer)  # days
    competition_level = Column(String(20))  # low, medium, high
    
    # Skills in Demand
    top_skills = Column(ARRAY(String))
    emerging_skills = Column(ARRAY(String))
    
    # Time Period
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    
    created_at = Column(DateTime, default=func.now())
    
    __table_args__ = (
        Index('idx_job_market_stats_title', 'job_title'),
        Index('idx_job_market_stats_location', 'city'),
        Index('idx_job_market_stats_period', 'period_start', 'period_end'),
    )