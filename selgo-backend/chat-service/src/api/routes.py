from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from uuid import UUID
import json
from datetime import datetime, timedelta

from ..services.services import ChatService
from ..models.chat_schemas import (
    ConversationCreate, ConversationResponse, ConversationUpdate, ConversationListResponse,
    MessageCreate, MessageResponse, MessageUpdate, MessageAttachmentCreate,
    MessageReactionCreate, TypingIndicatorCreate, ConversationSettingsUpdate,
    MessageReportCreate, OfferCreate, ConversationFilter, MessageFilter,
    PaginatedResponse, WebSocketMessage, ReadReceiptUpdate
)
from ..database.database import get_db
from ..utils.auth import get_current_user_id

# Create router
router = APIRouter(
    prefix="/api/v1/chats",
    tags=["chats"],
    responses={404: {"description": "Not found"}}
)

# WebSocket connection manager for real-time messaging
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}
        self.user_conversations: Dict[int, List[UUID]] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        if user_id in self.user_conversations:
            del self.user_conversations[user_id]

    async def send_to_user(self, user_id: int, message: WebSocketMessage):
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_text(message.model_dump_json())
            except:
                self.disconnect(user_id)

    async def send_to_conversation(self, conversation_id: UUID, message: WebSocketMessage, exclude_user: Optional[int] = None):
        # In a real implementation, this would query the database for conversation participants
        # For now, we'll send to all connected users
        for user_id, websocket in self.active_connections.items():
            if exclude_user and user_id == exclude_user:
                continue
            try:
                await websocket.send_text(message.model_dump_json())
            except:
                self.disconnect(user_id)

manager = ConnectionManager()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message_data = json.loads(data)
                # Handle different WebSocket message types
                if message_data.get("type") == "typing":
                    # Broadcast typing indicator
                    typing_message = WebSocketMessage(
                        type="typing",
                        conversation_id=UUID(message_data["conversation_id"]),
                        data={"user_id": user_id, "is_typing": message_data.get("is_typing", True)}
                    )
                    await manager.send_to_conversation(
                        UUID(message_data["conversation_id"]), 
                        typing_message, 
                        exclude_user=user_id
                    )
                elif message_data.get("type") == "read_receipt":
                    # Handle read receipts
                    read_message = WebSocketMessage(
                        type="read_receipt",
                        conversation_id=UUID(message_data["conversation_id"]),
                        data={"user_id": user_id, "message_id": message_data["message_id"]}
                    )
                    await manager.send_to_conversation(
                        UUID(message_data["conversation_id"]), 
                        read_message, 
                        exclude_user=user_id
                    )
            except json.JSONDecodeError:
                pass
    except WebSocketDisconnect:
        manager.disconnect(user_id)

# ==================== Conversation Routes ====================

@router.post("/conversations", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    conversation: ConversationCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Create a new conversation."""
    return ChatService.create_conversation(db, conversation, current_user_id)

@router.get("/conversations", response_model=List[ConversationListResponse])
async def get_user_conversations(
    filters: ConversationFilter = Depends(),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Get user's conversations with filtering and pagination."""
    return ChatService.get_user_conversations(db, current_user_id, filters, page, limit)

@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: UUID,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Get conversation details."""
    conversation = ChatService.get_conversation(db, conversation_id, current_user_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@router.put("/conversations/{conversation_id}", response_model=ConversationResponse)
async def update_conversation(
    conversation_id: UUID,
    update_data: ConversationUpdate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Update conversation settings."""
    conversation = ChatService.update_conversation(db, conversation_id, update_data, current_user_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@router.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: UUID,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Delete/leave a conversation."""
    success = ChatService.delete_conversation(db, conversation_id, current_user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")

# ==================== Message Routes ====================

@router.post("/conversations/{conversation_id}/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_message(
    conversation_id: UUID,
    message: MessageCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Send a new message."""
    new_message = ChatService.create_message(db, conversation_id, message, current_user_id)
    if not new_message:
        raise HTTPException(status_code=404, detail="Conversation not found or user not a participant")

    # Send real-time notification via WebSocket
    ws_message = WebSocketMessage(
        type="new_message",
        conversation_id=conversation_id,
        data={
            "message_id": str(new_message.id),
            "sender_id": current_user_id,
            "content": new_message.content,
            "message_type": new_message.message_type,
            "timestamp": new_message.timestamp.isoformat()
        }
    )
    await manager.send_to_conversation(conversation_id, ws_message, exclude_user=current_user_id)

    return new_message

@router.get("/conversations/{conversation_id}/messages", response_model=PaginatedResponse)
async def get_messages(
    conversation_id: UUID,
    filters: MessageFilter = Depends(),
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Get messages from a conversation with filtering and pagination."""
    result = ChatService.get_messages(db, conversation_id, current_user_id, filters, page, limit)
    if result is None:
        raise HTTPException(status_code=404, detail="Conversation not found or user not a participant")
    return result

@router.put("/messages/{message_id}", response_model=MessageResponse)
async def update_message(
    message_id: UUID,
    update_data: MessageUpdate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Edit a message."""
    message = ChatService.update_message(db, message_id, update_data, current_user_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found or permission denied")
    
    # Notify via WebSocket
    ws_message = WebSocketMessage(
        type="message_updated",
        conversation_id=message.conversation_id,
        data={
            "message_id": str(message.id),
            "content": message.content,
            "is_edited": True,
            "edited_at": message.edited_at.isoformat() if message.edited_at else None
        }
    )
    await manager.send_to_conversation(message.conversation_id, ws_message)
    
    return message

@router.delete("/messages/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(
    message_id: UUID,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Delete a message."""
    success = ChatService.delete_message(db, message_id, current_user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Message not found or permission denied")

# ==================== Attachment Routes ====================

@router.post("/messages/{message_id}/attachments")
async def upload_attachment(
    message_id: UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Upload file attachment to a message."""
    attachment = await ChatService.upload_attachment(db, message_id, file, current_user_id)
    if not attachment:
        raise HTTPException(status_code=404, detail="Message not found or permission denied")
    return attachment

# ==================== Reaction Routes ====================

@router.post("/messages/{message_id}/reactions")
async def add_reaction(
    message_id: UUID,
    reaction_data: MessageReactionCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Add reaction to a message."""
    reaction = ChatService.add_reaction(db, message_id, reaction_data, current_user_id)
    if not reaction:
        raise HTTPException(status_code=404, detail="Message not found")
    return reaction

@router.delete("/messages/{message_id}/reactions/{reaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_reaction(
    message_id: UUID,
    reaction_id: UUID,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Remove reaction from a message."""
    success = ChatService.remove_reaction(db, reaction_id, current_user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reaction not found or permission denied")

# ==================== Offer Routes (Finn.no-like feature) ====================

@router.post("/offers", response_model=MessageResponse)
async def create_offer(
    offer_data: OfferCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Create a price offer for a listing."""
    offer_message = ChatService.create_offer(db, offer_data, current_user_id)
    if not offer_message:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Notify via WebSocket
    ws_message = WebSocketMessage(
        type="new_offer",
        conversation_id=offer_data.conversation_id,
        data={
            "message_id": str(offer_message.id),
            "offer_amount": str(offer_message.offer_amount),
            "offer_message": offer_message.offer_message,
            "expires_at": offer_message.offer_expires_at.isoformat() if offer_message.offer_expires_at else None
        }
    )
    await manager.send_to_conversation(offer_data.conversation_id, ws_message, exclude_user=current_user_id)
    
    return offer_message

@router.get("/conversations/{conversation_id}/offers")
async def get_conversation_offers(
    conversation_id: UUID,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Get all offers in a conversation."""
    offers = ChatService.get_conversation_offers(db, conversation_id, current_user_id)
    if offers is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return offers

# ==================== Typing Indicators ====================

@router.post("/conversations/{conversation_id}/typing")
async def set_typing_indicator(
    conversation_id: UUID,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Set typing indicator for a conversation."""
    success = ChatService.set_typing_indicator(db, conversation_id, current_user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Send via WebSocket
    ws_message = WebSocketMessage(
        type="typing",
        conversation_id=conversation_id,
        data={"user_id": current_user_id, "is_typing": True}
    )
    await manager.send_to_conversation(conversation_id, ws_message, exclude_user=current_user_id)
    
    return {"message": "Typing indicator set"}

# ==================== Read Receipts ====================

@router.post("/messages/{message_id}/read")
async def mark_message_read(
    message_id: UUID,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Mark a message as read."""
    success = ChatService.mark_message_read(db, message_id, current_user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"message": "Message marked as read"}

@router.post("/conversations/{conversation_id}/read-all")
async def mark_conversation_read(
    conversation_id: UUID,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Mark all messages in conversation as read."""
    success = ChatService.mark_conversation_read(db, conversation_id, current_user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"message": "All messages marked as read"}

# ==================== Reporting ====================

@router.post("/messages/{message_id}/report")
async def report_message(
    message_id: UUID,
    report_data: MessageReportCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Report a message for inappropriate content."""
    report = ChatService.report_message(db, message_id, report_data, current_user_id)
    if not report:
        raise HTTPException(status_code=404, detail="Message not found")
    return report

# ==================== Search ====================

@router.get("/search/messages")
async def search_messages(
    query: str = Query(..., min_length=2),
    conversation_id: Optional[UUID] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Search messages across conversations."""
    results = ChatService.search_messages(db, query, current_user_id, conversation_id, page, limit)
    return results

@router.get("/search/conversations")
async def search_conversations(
    query: str = Query(..., min_length=2),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Search conversations by title or participant."""
    results = ChatService.search_conversations(db, query, current_user_id, page, limit)
    return results

# ==================== Statistics ====================

@router.get("/stats")
async def get_chat_statistics(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Get user's chat statistics."""
    stats = ChatService.get_user_chat_stats(db, current_user_id)
    return stats