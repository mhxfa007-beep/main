from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from .chat_models import ConversationType, MessageType, MessageStatus

# ==================== Participant Schemas ====================
class ParticipantBase(BaseModel):
    user_id: int

class ParticipantCreate(ParticipantBase):
    notifications_enabled: bool = True

class ParticipantResponse(ParticipantBase):
    id: UUID
    conversation_id: UUID
    is_admin: bool
    joined_at: datetime
    left_at: Optional[datetime] = None
    last_read_at: Optional[datetime] = None
    notifications_enabled: bool

    model_config = ConfigDict(from_attributes=True)

# ==================== Conversation Schemas ====================
class ConversationBase(BaseModel):
    title: Optional[str] = None
    conversation_type: ConversationType = ConversationType.DIRECT

class ConversationCreate(ConversationBase):
    participant_ids: List[int]
    related_listing_id: Optional[str] = None
    related_listing_type: Optional[str] = None
    related_listing_title: Optional[str] = None
    related_listing_price: Optional[Decimal] = None

class ConversationUpdate(BaseModel):
    title: Optional[str] = None
    is_archived: Optional[bool] = None
    is_muted: Optional[bool] = None

class ConversationResponse(ConversationBase):
    id: UUID
    related_listing_id: Optional[str] = None
    related_listing_type: Optional[str] = None
    related_listing_title: Optional[str] = None
    related_listing_price: Optional[Decimal] = None
    is_archived: bool
    is_muted: bool
    is_blocked: bool
    last_message_at: Optional[datetime] = None
    last_message_preview: Optional[str] = None
    unread_count: int
    created_at: datetime
    updated_at: datetime
    participants: List[ParticipantResponse] = []

    model_config = ConfigDict(from_attributes=True)

class ConversationListResponse(BaseModel):
    id: UUID
    title: Optional[str] = None
    conversation_type: ConversationType
    related_listing_title: Optional[str] = None
    last_message_at: Optional[datetime] = None
    last_message_preview: Optional[str] = None
    unread_count: int
    is_archived: bool
    is_muted: bool

    model_config = ConfigDict(from_attributes=True)

# ==================== Message Schemas ====================
class MessageBase(BaseModel):
    content: Optional[str] = None
    message_type: MessageType = MessageType.TEXT

class MessageCreate(MessageBase):
    reply_to_message_id: Optional[UUID] = None
    offer_amount: Optional[Decimal] = None
    offer_message: Optional[str] = None
    offer_expires_at: Optional[datetime] = None

class MessageUpdate(BaseModel):
    content: Optional[str] = None

class MessageAttachmentResponse(BaseModel):
    id: UUID
    file_name: str
    file_url: str
    file_type: str
    file_size: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    thumbnail_url: Optional[str] = None
    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)

class MessageReactionResponse(BaseModel):
    id: UUID
    user_id: int
    reaction: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class MessageResponse(MessageBase):
    id: UUID
    conversation_id: UUID
    sender_id: int
    status: MessageStatus
    is_edited: bool
    edited_at: Optional[datetime] = None
    is_deleted: bool
    deleted_at: Optional[datetime] = None
    reply_to_message_id: Optional[UUID] = None
    offer_amount: Optional[Decimal] = None
    offer_message: Optional[str] = None
    offer_expires_at: Optional[datetime] = None
    system_data: Optional[Dict[str, Any]] = None
    timestamp: datetime
    attachments: List[MessageAttachmentResponse] = []
    reactions: List[MessageReactionResponse] = []

    model_config = ConfigDict(from_attributes=True)

# ==================== Attachment Schemas ====================
class MessageAttachmentCreate(BaseModel):
    file_name: str
    file_url: str
    file_type: str
    file_size: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    thumbnail_url: Optional[str] = None

# ==================== Reaction Schemas ====================
class MessageReactionCreate(BaseModel):
    reaction: str

# ==================== Typing Indicator Schemas ====================
class TypingIndicatorCreate(BaseModel):
    conversation_id: UUID

class TypingIndicatorResponse(BaseModel):
    user_id: int
    started_at: datetime
    expires_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ==================== Settings Schemas ====================
class ConversationSettingsUpdate(BaseModel):
    is_muted: Optional[bool] = None
    is_archived: Optional[bool] = None
    custom_name: Optional[str] = None

class ConversationSettingsResponse(BaseModel):
    id: UUID
    conversation_id: UUID
    user_id: int
    is_muted: bool
    is_archived: bool
    custom_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ==================== Report Schemas ====================
class MessageReportCreate(BaseModel):
    reason: str
    description: Optional[str] = None

class MessageReportResponse(BaseModel):
    id: UUID
    message_id: UUID
    reported_by_user_id: int
    reason: str
    description: Optional[str] = None
    status: str
    created_at: datetime
    reviewed_at: Optional[datetime] = None
    reviewed_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

# ==================== Offer Schemas ====================
class OfferCreate(BaseModel):
    conversation_id: UUID
    offer_amount: Decimal
    offer_message: Optional[str] = None
    expires_in_hours: int = 24

class OfferResponse(BaseModel):
    message_id: UUID
    offer_amount: Decimal
    offer_message: Optional[str] = None
    offer_expires_at: Optional[datetime] = None
    sender_id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

# ==================== Search and Filter Schemas ====================
class ConversationFilter(BaseModel):
    conversation_type: Optional[ConversationType] = None
    is_archived: Optional[bool] = None
    related_listing_type: Optional[str] = None
    search_query: Optional[str] = None

class MessageFilter(BaseModel):
    message_type: Optional[MessageType] = None
    sender_id: Optional[int] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    search_query: Optional[str] = None

# ==================== Pagination Schemas ====================
class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    limit: int
    has_next: bool
    has_prev: bool

# ==================== WebSocket Schemas ====================
class WebSocketMessage(BaseModel):
    type: str  # 'message', 'typing', 'read_receipt', etc.
    conversation_id: UUID
    data: Dict[str, Any]

class ReadReceiptUpdate(BaseModel):
    message_id: UUID
    read_at: datetime
