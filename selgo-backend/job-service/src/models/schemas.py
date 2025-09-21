# File: job-service/src/models/schemas.py

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Any, Union
from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID

# Enums
class JobTypeEnum(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    TEMPORARY = "temporary"
    INTERNSHIP = "internship"
    FREELANCE = "freelance"

class ExperienceLevelEnum(str, Enum):
    ENTRY = "entry"
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    EXECUTIVE = "executive"

class JobStatusEnum(str, Enum):
    ACTIVE = "active"
    CLOSED = "closed"
    DRAFT = "draft"
    PAUSED = "paused"

class ProficiencyLevelEnum(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    FLUENT = "fluent"
    NATIVE = "native"

class CVTemplateEnum(str, Enum):
    MODERN = "modern"
    CLASSIC = "classic"
    CREATIVE = "creative"
    MINIMAL = "minimal"

# Base Schemas
class CompanyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Union[str, None] = Field(default=None)
    website: Union[str, None] = Field(default=None)
    logo_url: Union[str, None] = Field(default=None)
    industry: Union[str, None] = Field(default=None)
    size: Union[str, None] = Field(default=None)
    location: Union[str, None] = Field(default=None)
    founded_year: Union[int, None] = Field(default=None)

class CompanyCreate(CompanyBase):
    pass

class CompanyResponse(CompanyBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Job Schemas
class JobBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=10)
    short_description: Union[str, None] = Field(default=None)
    requirements: Union[str, None] = Field(default=None)
    responsibilities: Union[str, None] = Field(default=None)
    benefits: Union[str, None] = Field(default=None)
    job_type: JobTypeEnum
    experience_level: ExperienceLevelEnum
    salary_min: Union[float, None] = Field(default=None)
    salary_max: Union[float, None] = Field(default=None)
    salary_currency: str = "USD"
    is_salary_negotiable: bool = False
    location: Union[str, None] = Field(default=None)
    is_remote: bool = False
    city: Union[str, None] = Field(default=None)
    state: Union[str, None] = Field(default=None)
    country: Union[str, None] = Field(default=None)
    application_deadline: Union[datetime, None] = Field(default=None)
    application_email: Union[str, None] = Field(default=None)
    application_url: Union[str, None] = Field(default=None)
    contact_person: Union[str, None] = Field(default=None)
    contact_phone: Union[str, None] = Field(default=None)
    featured: bool = False
    tags: Union[List[str, None]] = None

class JobCreate(JobBase):
    company_id: int
    category_id: Union[int, None] = Field(default=None)

class JobUpdate(BaseModel):
    title: Union[str, None] = Field(default=None)
    description: Union[str, None] = Field(default=None)
    short_description: Union[str, None] = Field(default=None)
    requirements: Union[str, None] = Field(default=None)
    responsibilities: Union[str, None] = Field(default=None)
    benefits: Union[str, None] = Field(default=None)
    job_type: Union[JobTypeEnum, None] = Field(default=None)
    experience_level: Union[ExperienceLevelEnum, None] = Field(default=None)
    salary_min: Union[float, None] = Field(default=None)
    salary_max: Union[float, None] = Field(default=None)
    is_salary_negotiable: Union[bool, None] = Field(default=None)
    location: Union[str, None] = Field(default=None)
    is_remote: Union[bool, None] = Field(default=None)
    city: Union[str, None] = Field(default=None)
    state: Union[str, None] = Field(default=None)
    country: Union[str, None] = Field(default=None)
    application_deadline: Union[datetime, None] = Field(default=None)
    application_email: Union[str, None] = Field(default=None)
    application_url: Union[str, None] = Field(default=None)
    contact_person: Union[str, None] = Field(default=None)
    contact_phone: Union[str, None] = Field(default=None)
    status: Union[JobStatusEnum, None] = Field(default=None)
    featured: Union[bool, None] = Field(default=None)
    tags: Union[List[str, None]] = None

class JobResponse(JobBase):
    id: int
    slug: str
    status: JobStatusEnum
    view_count: int = 0
    application_count: int = 0
    company_id: int
    category_id: Union[int, None] = Field(default=None)
    posted_by: int
    created_at: datetime
    updated_at: datetime
    published_at: Union[datetime, None] = Field(default=None)
    
    # Nested objects
    company: Union[CompanyResponse, None] = Field(default=None)
    
    model_config = ConfigDict(from_attributes=True)

# Job Search and Filter Schemas
class JobSearchRequest(BaseModel):
    q: Union[str, None] = Field(default=None)  # Search query
    location: Union[str, None] = Field(default=None)
    job_type: Union[List[JobTypeEnum, None]] = None
    experience_level: Union[List[ExperienceLevelEnum, None]] = None
    salary_min: Union[float, None] = Field(default=None)
    salary_max: Union[float, None] = Field(default=None)
    is_remote: Union[bool, None] = Field(default=None)
    company_id: Union[int, None] = Field(default=None)
    category_id: Union[int, None] = Field(default=None)
    tags: Union[List[str, None]] = None
    posted_within_days: Union[int, None] = Field(default=None)
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)
    sort_by: Union[str, None] = "created_at"  # created_at, salary_max, view_count
    sort_order: Union[str, None] = "desc"  # asc, desc

class JobSearchResponse(BaseModel):
    jobs: List[JobResponse]
    total: int
    page: int
    limit: int
    total_pages: int

# Profile Schemas
class JobProfileBase(BaseModel):
    phone: Union[str, None] = Field(default=None)
    location: Union[str, None] = Field(default=None)
    website: Union[str, None] = Field(default=None)
    linkedin_url: Union[str, None] = Field(default=None)
    github_url: Union[str, None] = Field(default=None)
    professional_summary: Union[str, None] = Field(default=None)
    desired_job_title: Union[str, None] = Field(default=None)
    desired_salary_min: Union[float, None] = Field(default=None)
    desired_salary_max: Union[float, None] = Field(default=None)
    salary_currency: str = "USD"
    willing_to_relocate: bool = False
    available_from: Union[datetime, None] = Field(default=None)
    profile_visibility: str = "private"
    allow_contact: bool = True
    receive_job_alerts: bool = True

class JobProfileCreate(JobProfileBase):
    pass

class JobProfileUpdate(JobProfileBase):
    pass

class JobProfileResponse(JobProfileBase):
    id: int
    user_id: int
    profile_completion: int = 0
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Work Experience Schemas
class WorkExperienceBase(BaseModel):
    job_title: str = Field(..., min_length=1, max_length=255)
    company_name: str = Field(..., min_length=1, max_length=255)
    company_website: Union[str, None] = Field(default=None)
    location: Union[str, None] = Field(default=None)
    start_date: datetime
    end_date: Union[datetime, None] = Field(default=None)
    is_current: bool = False
    description: Union[str, None] = Field(default=None)
    achievements: Union[str, None] = Field(default=None)
    display_order: int = 0

class WorkExperienceCreate(WorkExperienceBase):
    pass

class WorkExperienceUpdate(WorkExperienceBase):
    job_title: Union[str, None] = Field(default=None)
    company_name: Union[str, None] = Field(default=None)
    start_date: Union[datetime, None] = Field(default=None)

class WorkExperienceResponse(WorkExperienceBase):
    id: int
    profile_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Education Schemas
class EducationBase(BaseModel):
    degree: str = Field(..., min_length=1, max_length=255)
    field_of_study: Union[str, None] = Field(default=None)
    institution: str = Field(..., min_length=1, max_length=255)
    location: Union[str, None] = Field(default=None)
    start_date: datetime
    end_date: Union[datetime, None] = Field(default=None)
    is_current: bool = False
    gpa: Union[float, None] = Field(default=None)
    description: Union[str, None] = Field(default=None)
    display_order: int = 0

class EducationCreate(EducationBase):
    pass

class EducationUpdate(EducationBase):
    degree: Union[str, None] = Field(default=None)
    institution: Union[str, None] = Field(default=None)
    start_date: Union[datetime, None] = Field(default=None)

class EducationResponse(EducationBase):
    id: int
    profile_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Skill Schemas
class SkillBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    category: Union[str, None] = Field(default=None)

class SkillCreate(SkillBase):
    pass

class SkillResponse(SkillBase):
    id: int
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class UserSkillBase(BaseModel):
    skill_id: int
    proficiency_level: ProficiencyLevelEnum
    years_of_experience: Union[int, None] = Field(default=None)

class UserSkillCreate(UserSkillBase):
    pass

class UserSkillResponse(UserSkillBase):
    id: int
    profile_id: int
    skill: Union[SkillResponse, None] = Field(default=None)
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Language Schemas
class LanguageBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    code: Union[str, None] = Field(default=None)

class LanguageCreate(LanguageBase):
    pass

class LanguageResponse(LanguageBase):
    id: int
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class UserLanguageBase(BaseModel):
    language_id: int
    proficiency_level: ProficiencyLevelEnum

class UserLanguageCreate(UserLanguageBase):
    pass

class UserLanguageResponse(UserLanguageBase):
    id: int
    profile_id: int
    language: Union[LanguageResponse, None] = Field(default=None)
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# CV Schemas
class CVBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    template: CVTemplateEnum = CVTemplateEnum.MODERN
    cv_data: Union[Dict[str, Any, None]] = None
    is_public: bool = False
    allow_downloads: bool = True

class CVCreate(CVBase):
    pass

class CVUpdate(BaseModel):
    title: Union[str, None] = Field(default=None)
    template: Union[CVTemplateEnum, None] = Field(default=None)
    cv_data: Union[Dict[str, Any, None]] = None
    is_public: Union[bool, None] = Field(default=None)
    allow_downloads: Union[bool, None] = Field(default=None)

class CVResponse(CVBase):
    id: int
    user_id: int
    status: str
    file_path: Union[str, None] = Field(default=None)
    file_size: Union[int, None] = Field(default=None)
    view_count: int = 0
    download_count: int = 0
    created_at: datetime
    updated_at: datetime
    last_generated_at: Union[datetime, None] = Field(default=None)
    
    model_config = ConfigDict(from_attributes=True)

# CV Builder Steps Schemas
class ContactInfoStep(BaseModel):
    email: str
    phone: Union[str, None] = Field(default=None)
    location: Union[str, None] = Field(default=None)
    website: Union[str, None] = Field(default=None)
    linkedin_url: Union[str, None] = Field(default=None)

class WorkExperienceStep(BaseModel):
    experiences: List[WorkExperienceBase] = []

class EducationStep(BaseModel):
    educations: List[EducationBase] = []

class LanguageStep(BaseModel):
    languages: List[UserLanguageBase] = []

class SummaryStep(BaseModel):
    professional_summary: str

class CVBuilderData(BaseModel):
    contact_info: Union[ContactInfoStep, None] = Field(default=None)
    work_experience: Union[WorkExperienceStep, None] = Field(default=None)
    education: Union[EducationStep, None] = Field(default=None)
    languages: Union[LanguageStep, None] = Field(default=None)
    summary: Union[SummaryStep, None] = Field(default=None)

# Article Schemas
class ArticleCategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    slug: str = Field(..., min_length=1, max_length=100)
    description: Union[str, None] = Field(default=None)
    display_order: int = 0

class ArticleCategoryCreate(ArticleCategoryBase):
    pass

class ArticleCategoryResponse(ArticleCategoryBase):
    id: int
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ArticleBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255)
    excerpt: Union[str, None] = Field(default=None)
    content: str = Field(..., min_length=10)
    featured_image: Union[str, None] = Field(default=None)
    image_alt: Union[str, None] = Field(default=None)
    category_id: Union[int, None] = Field(default=None)
    tags: Union[List[str, None]] = None
    meta_title: Union[str, None] = Field(default=None)
    meta_description: Union[str, None] = Field(default=None)
    reading_time: Union[int, None] = Field(default=None)

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(BaseModel):
    title: Union[str, None] = Field(default=None)
    excerpt: Union[str, None] = Field(default=None)
    content: Union[str, None] = Field(default=None)
    featured_image: Union[str, None] = Field(default=None)
    image_alt: Union[str, None] = Field(default=None)
    category_id: Union[int, None] = Field(default=None)
    tags: Union[List[str, None]] = None
    meta_title: Union[str, None] = Field(default=None)
    meta_description: Union[str, None] = Field(default=None)
    status: Union[str, None] = Field(default=None)

class ArticleResponse(ArticleBase):
    id: int
    status: str
    published_at: Union[datetime, None] = Field(default=None)
    author_id: int
    view_count: int = 0
    created_at: datetime
    updated_at: datetime
    category: Union[ArticleCategoryResponse, None] = Field(default=None)
    
    model_config = ConfigDict(from_attributes=True)

# Salary Comparison Schemas
class SalaryEntryBase(BaseModel):
    job_title: str = Field(..., min_length=1, max_length=255)
    annual_salary: float = Field(..., gt=0)
    currency: str = "USD"
    bonus: Union[float, None] = Field(default=None)
    stock_options: Union[float, None] = Field(default=None)
    other_compensation: Union[float, None] = Field(default=None)
    company_name: Union[str, None] = Field(default=None)
    location: Union[str, None] = Field(default=None)
    years_of_experience: Union[int, None] = Field(default=None)
    company_size: Union[str, None] = Field(default=None)
    industry: Union[str, None] = Field(default=None)
    is_current: bool = True
    is_anonymous: bool = True

class SalaryEntryCreate(SalaryEntryBase):
    pass

class SalaryEntryResponse(SalaryEntryBase):
    id: int
    profile_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class SalaryComparisonRequest(BaseModel):
    job_title: str
    location: Union[str, None] = Field(default=None)
    years_of_experience: Union[int, None] = Field(default=None)
    industry: Union[str, None] = Field(default=None)

class SalaryComparisonResponse(BaseModel):
    job_title: str
    location: Union[str, None] = Field(default=None)
    average_salary: float
    median_salary: float
    min_salary: float
    max_salary: float
    total_entries: int
    percentile_25: float
    percentile_75: float
    currency: str = "USD"

# Recommendation Schemas
class JobRecommendationResponse(BaseModel):
    id: int
    job_id: int
    score: float
    reason: Union[str, None] = Field(default=None)
    job: Union[JobResponse, None] = Field(default=None)
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Popular Search Schemas
class PopularSearchResponse(BaseModel):
    id: int
    search_term: str
    search_type: str
    search_count: int
    is_featured: bool
    display_order: int
    
    model_config = ConfigDict(from_attributes=True)

class PopularSearchesGrouped(BaseModel):
    positions: List[str] = []
    locations: List[str] = []
    articles: List[str] = []

# File Upload Schemas
class FileUploadResponse(BaseModel):
    filename: str
    file_path: str
    file_size: int
    file_type: str
    upload_url: Union[str, None] = Field(default=None)

# Generic Response Schemas
class MessageResponse(BaseModel):
    message: str
    
class ErrorResponse(BaseModel):
    error: str
    detail: Union[str, None] = Field(default=None)
    
# Job Alert Schemas
class JobAlertCreate(BaseModel):
    alert_name: str = Field(..., min_length=1, max_length=255)
    search_criteria: Dict[str, Any] = Field(..., description="Search parameters for the alert")
    notification_method: str = Field(default="email", description="email, push, both")
    frequency: str = Field(default="daily", description="daily, weekly, monthly")

class JobAlertUpdate(BaseModel):
    alert_name: Union[str, None] = Field(default=None)
    search_criteria: Union[Dict[str, Any, None]] = None
    notification_method: Union[str, None] = Field(default=None)
    frequency: Union[str, None] = Field(default=None)
    is_active: Union[bool, None] = Field(default=None)

class JobAlertResponse(BaseModel):
    id: int
    user_id: int
    alert_name: str
    search_criteria: Dict[str, Any]
    is_active: bool
    notification_method: str
    frequency: str
    total_jobs_sent: int
    last_sent_at: Union[datetime, None] = Field(default=None)
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Job Recommendation Schemas
class JobRecommendationResponse(BaseModel):
    job_id: int
    title: str
    company: Union[str, None] = Field(default=None)
    location: Union[str, None] = Field(default=None)
    salary_min: Union[float, None] = Field(default=None)
    salary_max: Union[float, None] = Field(default=None)
    score: float
    reason: str
    created_at: datetime

# User Job Preferences Schemas
class UserJobPreferencesCreate(BaseModel):
    preferred_job_titles: Union[List[str, None]] = None
    preferred_locations: Union[List[str, None]] = None
    preferred_job_types: Union[List[str, None]] = None
    preferred_experience_levels: Union[List[str, None]] = None
    min_salary: Union[float, None] = Field(default=None)
    max_salary: Union[float, None] = Field(default=None)
    salary_currency: str = "USD"
    remote_preference: str = "no_preference"
    preferred_company_sizes: Union[List[str, None]] = None
    preferred_industries: Union[List[str, None]] = None
    email_notifications: bool = True
    push_notifications: bool = True
    notification_frequency: str = "daily"

class UserJobPreferencesResponse(UserJobPreferencesCreate):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Enhanced Job Response with Analytics
class JobResponseWithAnalytics(JobResponse):
    analytics: Union[Dict[str, Any, None]] = None
    is_saved: Union[bool, None] = Field(default=None)
    is_applied: Union[bool, None] = Field(default=None)
    recommendation_score: Union[float, None] = Field(default=None)
    recommendation_reason: Union[str, None] = Field(default=None)

# Job Application Schemas
class JobApplicationCreate(BaseModel):
    cover_letter: Union[str, None] = Field(default=None)
    cv_file_path: Union[str, None] = Field(default=None)
    additional_info: Union[str, None] = Field(default=None)

class JobApplicationUpdate(BaseModel):
    status: Union[str, None] = Field(default=None)
    cover_letter: Union[str, None] = Field(default=None)
    additional_info: Union[str, None] = Field(default=None)

class JobApplicationResponse(BaseModel):
    id: int
    job_id: int
    user_id: int
    cover_letter: Union[str, None] = Field(default=None)
    cv_file_path: Union[str, None] = Field(default=None)
    additional_info: Union[str, None] = Field(default=None)
    status: str
    applied_at: datetime
    reviewed_at: Union[datetime, None] = Field(default=None)
    job: Union[JobResponse, None] = Field(default=None)
    
    model_config = ConfigDict(from_attributes=True)

# Job Category Schemas  
class JobCategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    slug: str = Field(..., min_length=1, max_length=100)
    description: Union[str, None] = Field(default=None)
    parent_id: Union[int, None] = Field(default=None)

class JobCategoryResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: Union[str, None] = Field(default=None)
    parent_id: Union[int, None] = Field(default=None)
    is_active: bool
    job_count: Union[int, None] = Field(default=None)
    created_at: datetime
    children: Union[List['JobCategoryResponse', None]] = None
    
    model_config = ConfigDict(from_attributes=True)

# Company Schemas (Enhanced)
class CompanyUpdate(BaseModel):
    name: Union[str, None] = Field(default=None)
    description: Union[str, None] = Field(default=None)
    website: Union[str, None] = Field(default=None)
    logo_url: Union[str, None] = Field(default=None)
    industry: Union[str, None] = Field(default=None)
    size: Union[str, None] = Field(default=None)
    location: Union[str, None] = Field(default=None)
    founded_year: Union[int, None] = Field(default=None)

class CompanyResponseWithJobs(CompanyResponse):
    jobs: Union[List[JobResponse, None]] = None
    job_count: int = 0
    avg_salary: Union[float, None] = Field(default=None)

# Job Analytics Schemas
class JobAnalyticsResponse(BaseModel):
    job_id: int
    period: Dict[str, Any]
    summary: Dict[str, Any]
    daily_data: List[Dict[str, Any]]
    geographic_data: List[Dict[str, Any]]
    traffic_sources: List[Dict[str, Any]]

class EmployerAnalyticsResponse(BaseModel):
    employer_id: int
    total_jobs: int
    period: Dict[str, Any]
    summary: Dict[str, Any]
    top_performing_jobs: List[Dict[str, Any]]
    job_performance: List[Dict[str, Any]]

# Search and Filter Schemas (Enhanced)
class JobSearchFilters(BaseModel):
    q: Union[str, None] = Field(default=None)
    location: Union[str, None] = Field(default=None)
    job_type: Union[List[str, None]] = None
    experience_level: Union[List[str, None]] = None
    salary_min: Union[float, None] = Field(default=None)
    salary_max: Union[float, None] = Field(default=None)
    is_remote: Union[bool, None] = Field(default=None)
    company_id: Union[int, None] = Field(default=None)
    category_id: Union[int, None] = Field(default=None)
    tags: Union[List[str, None]] = None
    posted_within_days: Union[int, None] = Field(default=None)
    company_size: Union[List[str, None]] = None
    industry: Union[List[str, None]] = None

class JobSearchResponseEnhanced(BaseModel):
    jobs: List[JobResponseWithAnalytics]
    total: int
    page: int
    limit: int
    total_pages: int
    filters_applied: JobSearchFilters
    facets: Union[Dict[str, List[Dict[str, Any, None]]]] = None  # For filter counts

# Saved Job Schemas
class SavedJobResponse(BaseModel):
    id: int
    job_id: int
    user_id: int
    saved_at: datetime
    job: Union[JobResponse, None] = Field(default=None)
    
    model_config = ConfigDict(from_attributes=True)

# Job View History Schemas
class JobViewResponse(BaseModel):
    id: int
    job_id: int
    user_id: Union[int, None] = Field(default=None)
    viewed_at: datetime
    job: Union[JobResponse, None] = Field(default=None)
    
    model_config = ConfigDict(from_attributes=True)

# Job Statistics Schemas
class JobStatisticsResponse(BaseModel):
    total_jobs: int
    active_jobs: int
    jobs_this_month: int
    total_applications: int
    avg_applications_per_job: float
    top_categories: List[Dict[str, Any]]
    top_companies: List[Dict[str, Any]]
    salary_insights: Dict[str, Any]

# Bulk Operations Schemas
class BulkJobAction(BaseModel):
    job_ids: List[int]
    action: str  # activate, deactivate, delete, feature, unfeature
    
class BulkJobResponse(BaseModel):
    successful: List[int]
    failed: List[Dict[str, Any]]
    total_processed: int

# Advanced Filter Options
class FilterOptionsResponse(BaseModel):
    job_types: List[Dict[str, str]]
    experience_levels: List[Dict[str, str]]
    industries: List[Dict[str, Any]]
    company_sizes: List[Dict[str, str]]
    locations: List[Dict[str, Any]]
    salary_ranges: List[Dict[str, Any]]
    categories: List[JobCategoryResponse]
    
# Job Feed Schemas (for homepage/recommendations)
class JobFeedRequest(BaseModel):
    user_location: Union[str, None] = Field(default=None)
    user_skills: Union[List[str, None]] = None
    feed_type: str = "mixed"  # recent, recommended, trending, mixed
    limit: int = Field(default=20, ge=1, le=100)

class JobFeedResponse(BaseModel):
    jobs: List[JobResponseWithAnalytics]
    feed_type: str
    personalized: bool
    refresh_token: str  # For pagination/refresh

# Company Follow Schemas
class CompanyFollowResponse(BaseModel):
    id: int
    company_id: int
    user_id: int
    followed_at: datetime
    company: Union[CompanyResponse, None] = Field(default=None)
    
    model_config = ConfigDict(from_attributes=True)

# Job Alert Summary
class JobAlertSummaryResponse(BaseModel):
    total_alerts: int
    active_alerts: int
    total_jobs_sent: int
    alerts_sent_today: int
    most_active_alert: Union[str, None] = Field(default=None)
    
# User Job Activity Summary
class UserJobActivityResponse(BaseModel):
    user_id: int
    jobs_viewed_today: int
    jobs_saved_total: int
    applications_submitted: int
    last_job_viewed: Union[datetime, None] = Field(default=None)
    activity_score: int
    recommended_actions: List[str]

# Enhanced Job Schemas with Finn.no job board features

class EnhancedCompanyBase(BaseModel):
    # Basic Information
    name: str = Field(max_length=255)
    slug: str = Field(max_length=255)
    description: Union[str, None] = Field(default=None)
    short_description: Union[str, None] = Field(default=None, max_length=500)
    tagline: Union[str, None] = Field(default=None, max_length=200)
    
    # Contact Information
    website: Union[str, None] = Field(default=None, max_length=500)
    email: Union[str, None] = Field(default=None, max_length=255)
    phone: Union[str, None] = Field(default=None, max_length=50)
    
    # Visual Identity
    logo_url: Union[str, None] = Field(default=None, max_length=500)
    cover_image_url: Union[str, None] = Field(default=None, max_length=500)
    brand_colors: Union[Dict[str, str], None] = Field(default=None)
    
    # Company Details
    industry: Union[str, None] = Field(default=None, max_length=100)
    company_size: Union[str, None] = Field(default=None, max_length=50)
    founded_year: Union[int, None] = Field(default=None, ge=1800, le=2030)
    company_type: Union[str, None] = Field(default=None, max_length=50)
    
    # Location Information
    headquarters_address: Union[str, None] = Field(default=None, max_length=500)
    headquarters_city: Union[str, None] = Field(default=None, max_length=100)
    headquarters_country: Union[str, None] = Field(default=None, max_length=100)
    office_locations: Union[List[str], None] = Field(default_factory=list)
    
    # Company Culture & Values
    mission_statement: Union[str, None] = Field(default=None)
    vision_statement: Union[str, None] = Field(default=None)
    core_values: Union[List[str], None] = Field(default_factory=list)
    company_culture: Union[str, None] = Field(default=None)
    work_environment: Union[str, None] = Field(default=None, max_length=50)
    
    # Benefits & Perks
    benefits: Union[List[str], None] = Field(default_factory=list)
    perks: Union[List[str], None] = Field(default_factory=list)
    remote_work_policy: Union[str, None] = Field(default=None, max_length=50)
    
    # Social Media & Links
    linkedin_url: Union[str, None] = Field(default=None, max_length=500)
    twitter_url: Union[str, None] = Field(default=None, max_length=500)
    facebook_url: Union[str, None] = Field(default=None, max_length=500)
    
    # Company Statistics
    employee_count: Union[int, None] = Field(default=None, ge=0)
    annual_revenue: Union[Decimal, None] = Field(default=None, ge=0)
    revenue_currency: str = Field(default='NOK', max_length=3)

class EnhancedCompanyCreate(EnhancedCompanyBase):
    pass

class EnhancedCompany(EnhancedCompanyBase):
    id: UUID
    
    # Ratings & Reviews
    overall_rating: float = Field(default=0.0, ge=0.0, le=5.0)
    culture_rating: float = Field(default=0.0, ge=0.0, le=5.0)
    salary_rating: float = Field(default=0.0, ge=0.0, le=5.0)
    benefits_rating: float = Field(default=0.0, ge=0.0, le=5.0)
    management_rating: float = Field(default=0.0, ge=0.0, le=5.0)
    career_rating: float = Field(default=0.0, ge=0.0, le=5.0)
    total_reviews: int = Field(default=0, ge=0)
    
    # Verification & Status
    is_verified: bool = Field(default=False)
    is_premium: bool = Field(default=False)
    is_hiring: bool = Field(default=True)
    is_active: bool = Field(default=True)
    
    # Timestamps
    created_at: datetime
    updated_at: Union[datetime, None] = Field(default=None)
    verified_at: Union[datetime, None] = Field(default=None)
    
    model_config = ConfigDict(from_attributes=True)

class EnhancedJobBase(BaseModel):
    # Basic Information
    title: str = Field(max_length=255)
    slug: str = Field(max_length=255)
    description: str
    short_description: Union[str, None] = Field(default=None, max_length=1000)
    summary: Union[str, None] = Field(default=None, max_length=500)
    
    # Detailed Job Information
    requirements: Union[str, None] = Field(default=None)
    responsibilities: Union[str, None] = Field(default=None)
    qualifications: Union[str, None] = Field(default=None)
    preferred_qualifications: Union[str, None] = Field(default=None)
    benefits: Union[str, None] = Field(default=None)
    company_culture_fit: Union[str, None] = Field(default=None)
    
    # Job Classification
    job_type: str = Field(max_length=50)
    experience_level: str = Field(max_length=50)
    seniority_level: Union[str, None] = Field(default=None, max_length=50)
    department: Union[str, None] = Field(default=None, max_length=100)
    team: Union[str, None] = Field(default=None, max_length=100)
    
    # Work Arrangement
    work_arrangement: str = Field(default='on_site', max_length=50)
    remote_work_percentage: int = Field(default=0, ge=0, le=100)
    travel_requirement: Union[str, None] = Field(default=None, max_length=50)
    
    # Salary Information
    salary_min: Union[Decimal, None] = Field(default=None, ge=0)
    salary_max: Union[Decimal, None] = Field(default=None, ge=0)
    salary_currency: str = Field(default="NOK", max_length=3)
    salary_type: str = Field(default='yearly', max_length=20)
    is_salary_negotiable: bool = Field(default=True)
    is_salary_public: bool = Field(default=False)
    
    # Additional Compensation
    bonus_structure: Union[str, None] = Field(default=None, max_length=200)
    equity_offered: bool = Field(default=False)
    commission_structure: Union[str, None] = Field(default=None, max_length=200)
    
    # Location Information
    location: Union[str, None] = Field(default=None, max_length=255)
    city: Union[str, None] = Field(default=None, max_length=100)
    state_province: Union[str, None] = Field(default=None, max_length=100)
    country: Union[str, None] = Field(default=None, max_length=100)
    postal_code: Union[str, None] = Field(default=None, max_length=20)
    office_address: Union[str, None] = Field(default=None, max_length=500)
    
    # Skills and Technologies
    required_skills: Union[List[str], None] = Field(default_factory=list)
    preferred_skills: Union[List[str], None] = Field(default_factory=list)
    technologies: Union[List[str], None] = Field(default_factory=list)
    programming_languages: Union[List[str], None] = Field(default_factory=list)
    tools_software: Union[List[str], None] = Field(default_factory=list)
    certifications: Union[List[str], None] = Field(default_factory=list)
    
    # Education Requirements
    education_level: Union[str, None] = Field(default=None, max_length=50)
    education_field: Union[str, None] = Field(default=None, max_length=100)
    education_required: bool = Field(default=False)
    
    # Experience Requirements
    years_experience_min: int = Field(default=0, ge=0)
    years_experience_max: Union[int, None] = Field(default=None, ge=0)
    industry_experience: Union[List[str], None] = Field(default_factory=list)
    
    # Application Process
    application_deadline: Union[datetime, None] = Field(default=None)
    application_email: Union[str, None] = Field(default=None, max_length=255)
    application_url: Union[str, None] = Field(default=None, max_length=500)
    application_instructions: Union[str, None] = Field(default=None)
    contact_person: Union[str, None] = Field(default=None, max_length=255)
    contact_phone: Union[str, None] = Field(default=None, max_length=50)
    contact_email: Union[str, None] = Field(default=None, max_length=255)
    
    # Application Requirements
    requires_cover_letter: bool = Field(default=False)
    requires_portfolio: bool = Field(default=False)
    requires_references: bool = Field(default=False)
    custom_application_fields: Union[Dict[str, Any], None] = Field(default=None)
    
    # Hiring Process
    hiring_process_steps: Union[List[str], None] = Field(default_factory=list)
    estimated_hiring_time: Union[str, None] = Field(default=None, max_length=50)
    number_of_positions: int = Field(default=1, ge=1)
    
    # Benefits and Perks
    health_benefits: Union[List[str], None] = Field(default_factory=list)
    retirement_benefits: Union[List[str], None] = Field(default_factory=list)
    time_off_benefits: Union[List[str], None] = Field(default_factory=list)
    professional_development: Union[List[str], None] = Field(default_factory=list)
    workplace_perks: Union[List[str], None] = Field(default_factory=list)

class EnhancedJobCreate(EnhancedJobBase):
    company_id: UUID
    category_id: Union[int, None] = Field(default=None)

class EnhancedJob(EnhancedJobBase):
    id: UUID
    company_id: UUID
    category_id: Union[int, None] = Field(default=None)
    posted_by: Union[UUID, None] = Field(default=None)
    recruiter_id: Union[UUID, None] = Field(default=None)
    
    # Job Status and Visibility
    status: str = Field(default='active', max_length=20)
    is_featured: bool = Field(default=False)
    is_urgent: bool = Field(default=False)
    is_confidential: bool = Field(default=False)
    visibility: str = Field(default='public', max_length=20)
    
    # Statistics
    view_count: int = Field(default=0, ge=0)
    application_count: int = Field(default=0, ge=0)
    save_count: int = Field(default=0, ge=0)
    share_count: int = Field(default=0, ge=0)
    
    # Company Information (denormalized)
    company_name: Union[str, None] = Field(default=None, max_length=255)
    company_logo_url: Union[str, None] = Field(default=None, max_length=500)
    company_industry: Union[str, None] = Field(default=None, max_length=100)
    company_size: Union[str, None] = Field(default=None, max_length=50)
    
    # Timestamps
    created_at: datetime
    updated_at: Union[datetime, None] = Field(default=None)
    published_at: Union[datetime, None] = Field(default=None)
    expires_at: Union[datetime, None] = Field(default=None)
    filled_at: Union[datetime, None] = Field(default=None)
    
    model_config = ConfigDict(from_attributes=True)

class JobApplicationCreate(BaseModel):
    job_id: UUID
    cover_letter: Union[str, None] = Field(default=None)
    cv_file_path: Union[str, None] = Field(default=None, max_length=500)
    portfolio_url: Union[str, None] = Field(default=None, max_length=500)
    additional_documents: Union[List[str], None] = Field(default_factory=list)
    additional_info: Union[str, None] = Field(default=None)
    custom_responses: Union[Dict[str, Any], None] = Field(default=None)
    
    # Contact Information
    applicant_email: Union[str, None] = Field(default=None, max_length=255)
    applicant_phone: Union[str, None] = Field(default=None, max_length=50)
    applicant_name: Union[str, None] = Field(default=None, max_length=255)

class JobApplication(BaseModel):
    id: UUID
    job_id: UUID
    applicant_id: UUID
    
    # Application Data
    cover_letter: Union[str, None] = Field(default=None)
    cv_file_path: Union[str, None] = Field(default=None)
    portfolio_url: Union[str, None] = Field(default=None)
    additional_documents: Union[List[str], None] = Field(default=None)
    additional_info: Union[str, None] = Field(default=None)
    custom_responses: Union[Dict[str, Any], None] = Field(default=None)
    
    # Contact Information
    applicant_email: Union[str, None] = Field(default=None)
    applicant_phone: Union[str, None] = Field(default=None)
    applicant_name: Union[str, None] = Field(default=None)
    
    # Status and Tracking
    status: str = Field(default="applied")
    stage: Union[str, None] = Field(default=None)
    priority: str = Field(default="normal")
    
    # Recruiter Information
    recruiter_notes: Union[str, None] = Field(default=None)
    internal_rating: Union[int, None] = Field(default=None, ge=1, le=5)
    tags: Union[List[str], None] = Field(default=None)
    
    # Interview Information
    interview_scheduled_at: Union[datetime, None] = Field(default=None)
    interview_type: Union[str, None] = Field(default=None)
    interview_notes: Union[str, None] = Field(default=None)
    
    # Decision Information
    rejection_reason: Union[str, None] = Field(default=None)
    offer_details: Union[Dict[str, Any], None] = Field(default=None)
    
    # Timestamps
    applied_at: datetime
    reviewed_at: Union[datetime, None] = Field(default=None)
    interview_at: Union[datetime, None] = Field(default=None)
    decision_at: Union[datetime, None] = Field(default=None)
    
    model_config = ConfigDict(from_attributes=True)

class JobAlertCreate(BaseModel):
    alert_name: str = Field(max_length=200)
    keywords: Union[List[str], None] = Field(default_factory=list)
    job_title: Union[str, None] = Field(default=None, max_length=255)
    company_name: Union[str, None] = Field(default=None, max_length=255)
    location: Union[str, None] = Field(default=None, max_length=255)
    remote_only: bool = Field(default=False)
    
    # Job Type Filters
    job_types: Union[List[str], None] = Field(default_factory=list)
    experience_levels: Union[List[str], None] = Field(default_factory=list)
    salary_min: Union[Decimal, None] = Field(default=None, ge=0)
    salary_max: Union[Decimal, None] = Field(default=None, ge=0)
    
    # Company Filters
    company_sizes: Union[List[str], None] = Field(default_factory=list)
    industries: Union[List[str], None] = Field(default_factory=list)
    
    # Skills and Requirements
    required_skills: Union[List[str], None] = Field(default_factory=list)
    excluded_skills: Union[List[str], None] = Field(default_factory=list)
    
    # Alert Settings
    frequency: str = Field(default='immediate', regex='^(immediate|daily|weekly)$')
    email_notifications: bool = Field(default=True)
    push_notifications: bool = Field(default=True)

class JobAlert(BaseModel):
    id: UUID
    user_id: UUID
    alert_name: str
    keywords: Union[List[str], None] = Field(default=None)
    job_title: Union[str, None] = Field(default=None)
    company_name: Union[str, None] = Field(default=None)
    location: Union[str, None] = Field(default=None)
    remote_only: bool
    
    job_types: Union[List[str], None] = Field(default=None)
    experience_levels: Union[List[str], None] = Field(default=None)
    salary_min: Union[Decimal, None] = Field(default=None)
    salary_max: Union[Decimal, None] = Field(default=None)
    
    company_sizes: Union[List[str], None] = Field(default=None)
    industries: Union[List[str], None] = Field(default=None)
    
    required_skills: Union[List[str], None] = Field(default=None)
    excluded_skills: Union[List[str], None] = Field(default=None)
    
    is_active: bool
    frequency: str
    email_notifications: bool
    push_notifications: bool
    
    matches_found: int
    last_match_date: Union[datetime, None] = Field(default=None)
    
    created_at: datetime
    updated_at: Union[datetime, None] = Field(default=None)
    
    model_config = ConfigDict(from_attributes=True)

class CompanyReviewCreate(BaseModel):
    company_id: UUID
    title: str = Field(max_length=255)
    review_text: str
    pros: Union[str, None] = Field(default=None)
    cons: Union[str, None] = Field(default=None)
    advice_to_management: Union[str, None] = Field(default=None)
    
    # Ratings (1-5 scale)
    overall_rating: float = Field(ge=1.0, le=5.0)
    culture_rating: Union[float, None] = Field(default=None, ge=1.0, le=5.0)
    salary_rating: Union[float, None] = Field(default=None, ge=1.0, le=5.0)
    benefits_rating: Union[float, None] = Field(default=None, ge=1.0, le=5.0)
    management_rating: Union[float, None] = Field(default=None, ge=1.0, le=5.0)
    career_opportunities_rating: Union[float, None] = Field(default=None, ge=1.0, le=5.0)
    work_life_balance_rating: Union[float, None] = Field(default=None, ge=1.0, le=5.0)
    
    # Reviewer Information
    job_title: Union[str, None] = Field(default=None, max_length=255)
    employment_status: Union[str, None] = Field(default=None, max_length=50)
    employment_duration: Union[str, None] = Field(default=None, max_length=50)
    department: Union[str, None] = Field(default=None, max_length=100)
    location: Union[str, None] = Field(default=None, max_length=255)
    
    is_anonymous: bool = Field(default=True)

class CompanyReview(BaseModel):
    id: UUID
    company_id: UUID
    reviewer_id: UUID
    title: str
    review_text: str
    pros: Union[str, None] = Field(default=None)
    cons: Union[str, None] = Field(default=None)
    advice_to_management: Union[str, None] = Field(default=None)
    
    overall_rating: float
    culture_rating: Union[float, None] = Field(default=None)
    salary_rating: Union[float, None] = Field(default=None)
    benefits_rating: Union[float, None] = Field(default=None)
    management_rating: Union[float, None] = Field(default=None)
    career_opportunities_rating: Union[float, None] = Field(default=None)
    work_life_balance_rating: Union[float, None] = Field(default=None)
    
    job_title: Union[str, None] = Field(default=None)
    employment_status: Union[str, None] = Field(default=None)
    employment_duration: Union[str, None] = Field(default=None)
    department: Union[str, None] = Field(default=None)
    location: Union[str, None] = Field(default=None)
    
    is_verified: bool
    is_anonymous: bool
    is_approved: bool
    
    helpful_count: int
    not_helpful_count: int
    
    created_at: datetime
    updated_at: Union[datetime, None] = Field(default=None)
    
    model_config = ConfigDict(from_attributes=True)

class SalaryReportCreate(BaseModel):
    company_id: UUID
    job_title: str = Field(max_length=255)
    department: Union[str, None] = Field(default=None, max_length=100)
    experience_level: Union[str, None] = Field(default=None, max_length=50)
    years_experience: Union[int, None] = Field(default=None, ge=0)
    years_at_company: Union[int, None] = Field(default=None, ge=0)
    
    location: Union[str, None] = Field(default=None, max_length=255)
    city: Union[str, None] = Field(default=None, max_length=100)
    country: Union[str, None] = Field(default=None, max_length=100)
    
    base_salary: Decimal = Field(ge=0)
    bonus: Union[Decimal, None] = Field(default=None, ge=0)
    stock_options: Union[Decimal, None] = Field(default=None, ge=0)
    other_compensation: Union[Decimal, None] = Field(default=None, ge=0)
    currency: str = Field(default='NOK', max_length=3)
    
    employment_type: Union[str, None] = Field(default=None, max_length=50)
    work_arrangement: Union[str, None] = Field(default=None, max_length=50)
    
    education_level: Union[str, None] = Field(default=None, max_length=50)
    skills: Union[List[str], None] = Field(default_factory=list)
    certifications: Union[List[str], None] = Field(default_factory=list)

class SalaryReport(BaseModel):
    id: UUID
    company_id: UUID
    reporter_id: Union[UUID, None] = Field(default=None)
    
    job_title: str
    department: Union[str, None] = Field(default=None)
    experience_level: Union[str, None] = Field(default=None)
    years_experience: Union[int, None] = Field(default=None)
    years_at_company: Union[int, None] = Field(default=None)
    
    location: Union[str, None] = Field(default=None)
    city: Union[str, None] = Field(default=None)
    country: Union[str, None] = Field(default=None)
    
    base_salary: Decimal
    bonus: Union[Decimal, None] = Field(default=None)
    stock_options: Union[Decimal, None] = Field(default=None)
    other_compensation: Union[Decimal, None] = Field(default=None)
    total_compensation: Union[Decimal, None] = Field(default=None)
    currency: str
    
    employment_type: Union[str, None] = Field(default=None)
    work_arrangement: Union[str, None] = Field(default=None)
    
    education_level: Union[str, None] = Field(default=None)
    skills: Union[List[str], None] = Field(default=None)
    certifications: Union[List[str], None] = Field(default=None)
    
    is_verified: bool
    verification_method: Union[str, None] = Field(default=None)
    
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class AdvancedJobSearchFilters(BaseModel):
    # Basic filters
    keywords: Union[str, None] = Field(default=None, max_length=200)
    job_title: Union[str, None] = Field(default=None, max_length=255)
    company_name: Union[str, None] = Field(default=None, max_length=255)
    location: Union[str, None] = Field(default=None, max_length=255)
    remote_only: bool = Field(default=False)
    
    # Job classification
    job_types: Union[List[str], None] = Field(default_factory=list)
    experience_levels: Union[List[str], None] = Field(default_factory=list)
    departments: Union[List[str], None] = Field(default_factory=list)
    
    # Salary filters
    salary_min: Union[Decimal, None] = Field(default=None, ge=0)
    salary_max: Union[Decimal, None] = Field(default=None, ge=0)
    salary_currency: str = Field(default='NOK', max_length=3)
    
    # Company filters
    company_sizes: Union[List[str], None] = Field(default_factory=list)
    industries: Union[List[str], None] = Field(default_factory=list)
    company_rating_min: Union[float, None] = Field(default=None, ge=1.0, le=5.0)
    
    # Skills and requirements
    required_skills: Union[List[str], None] = Field(default_factory=list)
    preferred_skills: Union[List[str], None] = Field(default_factory=list)
    technologies: Union[List[str], None] = Field(default_factory=list)
    programming_languages: Union[List[str], None] = Field(default_factory=list)
    
    # Education and experience
    education_levels: Union[List[str], None] = Field(default_factory=list)
    years_experience_min: Union[int, None] = Field(default=None, ge=0)
    years_experience_max: Union[int, None] = Field(default=None, ge=0)
    
    # Work arrangement
    work_arrangements: Union[List[str], None] = Field(default_factory=list)
    remote_work_percentage_min: Union[int, None] = Field(default=None, ge=0, le=100)
    
    # Benefits and perks
    health_benefits: Union[List[str], None] = Field(default_factory=list)
    workplace_perks: Union[List[str], None] = Field(default_factory=list)
    
    # Job status
    include_expired: bool = Field(default=False)
    featured_only: bool = Field(default=False)
    urgent_only: bool = Field(default=False)
    
    # Date filters
    posted_after: Union[datetime, None] = Field(default=None)
    posted_before: Union[datetime, None] = Field(default=None)
    
    # Sorting
    sort_by: str = Field(default='created_at', regex='^(created_at|salary_min|view_count|application_count|relevance)$')
    sort_order: str = Field(default='desc', regex='^(asc|desc)$')
    
    # Pagination
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)