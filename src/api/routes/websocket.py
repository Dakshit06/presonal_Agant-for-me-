"""
WebSocket route for real-time chat with AI agents
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict
import structlog
import json

from src.agents.autogen_chat_agents import get_agent_platform

logger = structlog.get_logger()
router = APIRouter()


class ConnectionManager:
    """Manage WebSocket connections"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logger.info("websocket_connected", client_id=client_id)
    
    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            logger.info("websocket_disconnected", client_id=client_id)
    
    async def send_message(self, message: dict, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_json(message)


manager = ConnectionManager()


@router.websocket("/ws/chat/{client_id}")
async def websocket_chat(websocket: WebSocket, client_id: str):
    """
    WebSocket endpoint for real-time chat with AI agents
    
    Message format:
    {
        "type": "chat",
        "message": "user message here",
        "context": {...}
    }
    
    Response format:
    {
        "type": "response",
        "message": "agent response",
        "timestamp": "ISO datetime"
    }
    """
    await manager.connect(websocket, client_id)
    agent_platform = get_agent_platform()
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            
            message_type = data.get("type", "chat")
            user_message = data.get("message", "")
            context = data.get("context", {})
            
            logger.info("websocket_message_received", 
                       client_id=client_id, 
                       message=user_message[:100])
            
            # Send typing indicator
            await manager.send_message({
                "type": "typing",
                "status": True
            }, client_id)
            
            # Process with agent
            response = await agent_platform.chat(
                message=user_message,
                user_id=client_id
            )
            
            # Send response
            await manager.send_message({
                "type": "response",
                "message": response,
                "timestamp": json.dumps({"_": "now"})  # Simplified
            }, client_id)
            
            # Stop typing indicator
            await manager.send_message({
                "type": "typing",
                "status": False
            }, client_id)
            
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        logger.info("client_disconnected", client_id=client_id)
    except Exception as e:
        logger.error("websocket_error", client_id=client_id, error=str(e))
        manager.disconnect(client_id)
