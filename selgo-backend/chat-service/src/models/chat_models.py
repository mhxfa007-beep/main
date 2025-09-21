from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Enum, JSON, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum

Base = declarative_base()

class ConversationType(str, enum.Enum):
    DIRECT = "direct"  # Direct message between two users
    LISTING = "listing"  # Conversation about a specific listing
    GROUP = "group"  # Group conversation (future feature)

class MessageType(str, enum.Enum):
    TEXT = "text"
    IMAGE = "image"
    FILE = "file"
    OFFER = "offer"  # Price offer for a listing
    SYSTEM = "system"  # System generated messages
    LOCATION = "location"

class MessageStatus(str, enum.Enum):
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"

class Conversation(Base):
    __tablename__ = 'conversations'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    conversation_type = Column(Enum(ConversationType), default=ConversationType.DIRECT)
    title = Column(String(255), nullable=True)  # Optional conversation title
    
    # Listing-related fields (for Finn.no-like functionality)
    related_listing_id = Column(String(255), nullable=True)  # ID from property/car/etc service
    related_listing_type = Column(String(50), nullable=True)  # 'property', 'car', 'job', etc.
    related_listing_title = Column(String(255), nullable=True)  # Cached listing title
    related_listing_price = Column(DECIMAL(12, 2), nullable=True)  # Cached listing price
    
    # Conversation settings
    is_archived = Column(Boolean, default=False)
    is_muted = Column(Boolean, default=False)
    is_blocked = Column(Boolean, default=False)
    
    # Metadata
    last_message_at = Column(DateTime, nullable=True)
    last_message_preview = Column(String(500), nullable=True)
    unread_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    participants = relationship("Participant", back_populates="conversation", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Participant(Base):
    __tablename__ = 'participants'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey('conversations.id'), nullable=False)
    user_id = Column(Integer, nullable=False)
    
    # Participant settings
    is_admin = Column(Boolean, default=False)  # For group conversations
    joined_at = Column(DateTime, default=func.now())
    left_at = Column(DateTime, nullable=True)
    last_read_at = Column(DateTime, nullable=True)
    
    # Notification settings
    notifications_enabled = Column(Boolean, default=True)
    
    conversation = relationship("Conversation", back_populates="participants")

class Message(Base):
    __tablename__ = 'messages'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey('conversations.id'), nullable=False)
    sender_id = Column(Integer, nullable=False)
    
    # Message content
    message_type = Column(Enum(MessageType), default=MessageType.TEXT)
    content = Column(Text, nullable=True)  # Text content
    
    # For offers (Finn.no-like feature)
    offer_amount = Column(DECIMAL(12, 2), nullable=True)
    offer_message = Column(Text, nullable=True)
    offer_expires_at = Column(DateTime, nullable=True)
    
    # Message metadata
    status = Column(Enum(MessageStatus), default=MessageStatus.SENT)
    is_edited = Column(Boolean, default=False)
    edited_at = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)
    
    # Reply/thread functionality
    reply_to_message_id = Column(UUID(as_uuid=True), ForeignKey('messages.id'), nullable=True)
    
    # System message data
    system_data = Column(JSON, nullable=True)  # For system messages
    
    timestamp = Column(DateTime, default=func.now())

    conversation = relationship("Conversation", back_populates="messages")
    reply_to = relationship("Message", remote_side=[id])
    attachments = relationship("MessageAttachment", back_populates="message", cascade="all, delete-orphan")
    reactions = relationship("MessageReaction", back_populates="message", cascade="all, delete-orphan")

class MessageAttachment(Base):
    __tablename__ = 'message_attachments'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    message_id = Column(UUID(as_uuid=True), ForeignKey('messages.id'), nullable=False)
    
    file_name = Column(String(255), nullable=False)
    file_url = Column(String(500), nullable=False)
    file_type = Column(String(100), nullable=False)  # image/jpeg, application/pdf, etc.
    file_size = Column(Integer, nullable=True)  # Size in bytes
    
    # Image-specific fields
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    thumbnail_url = Column(String(500), nullable=True)
    
    uploaded_at = Column(DateTime, default=func.now())
    
    message = relationship("Message", back_populates="attachments")

class MessageReaction(Base):
    __tablename__ = 'message_reactions'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    message_id = Column(UUID(as_uuid=True), ForeignKey('messages.id'), nullable=False)
    user_id = Column(Integer, nullable=False)
    
    reaction = Column(String(10), nullable=False)  # Emoji or reaction type
    created_at = Column(DateTime, default=func.now())
    
    message = relationship("Message", back_populates="reactions")

class TypingIndicator(Base):
    __tablename__ = 'typing_indicators'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey('conversations.id'), nullable=False)
    user_id = Column(Integer, nullable=False)
    
    started_at = Column(DateTime, default=func.now())
    expires_at = Column(DateTime, nullable=False)  # Auto-expire after 30 seconds

class ConversationSettings(Base):
    __tablename__ = 'conversation_settings'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey('conversations.id'), nullable=False)
    user_id = Column(Integer, nullable=False)
    
    # User-specific conversation settings
    is_muted = Column(Boolean, default=False)
    is_archived = Column(Boolean, default=False)
    custom_name = Column(String(255), nullable=True)  # User can rename conversation
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class MessageReport(Base):
    __tablename__ = 'message_reports'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    message_id = Column(UUID(as_uuid=True), ForeignKey('messages.id'), nullable=False)
    reported_by_user_id = Column(Integer, nullable=False)
    
    reason = Column(String(100), nullable=False)  # spam, inappropriate, etc.
    description = Column(Text, nullable=True)
    status = Column(String(50), default="pending")  # pending, reviewed, resolved
    
    created_at = Column(DateTime, default=func.now())
    reviewed_at = Column(DateTime, nullable=True)
    reviewed_by = Column(Integer, nullable=True)  # Admin user ID