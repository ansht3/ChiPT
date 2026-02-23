from fastapi import WebSocket
from typing import Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import json
import logging

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections for real-time updates."""
    
    def __init__(self):
        # Map of user_id -> list of WebSocket connections
        self.active_connections: Dict[int, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int):
        """Accept and store a WebSocket connection."""
        await websocket.accept()
        
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        
        self.active_connections[user_id].append(websocket)
        logger.info(f"User {user_id} connected. Total connections: {len(self.active_connections[user_id])}")
    
    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection."""
        for user_id, connections in self.active_connections.items():
            if websocket in connections:
                connections.remove(websocket)
                logger.info(f"User {user_id} disconnected. Remaining connections: {len(connections)}")
                
                # Clean up empty lists
                if not connections:
                    del self.active_connections[user_id]
                
                break
    
    async def send_to_user(self, user_id: int, message: dict):
        """Send a message to all connections for a specific user."""
        if user_id in self.active_connections:
            disconnected = []
            
            for websocket in self.active_connections[user_id]:
                try:
                    await websocket.send_text(json.dumps(message))
                except Exception as e:
                    logger.error(f"Error sending to user {user_id}: {e}")
                    disconnected.append(websocket)
            
            # Clean up disconnected sockets
            for websocket in disconnected:
                self.disconnect(websocket)
    
    async def broadcast_new_question(self, question_data: dict, db: AsyncSession):
        """Broadcast a new question to all instructors."""
        from database import User
        
        # Get all instructor user IDs
        result = await db.execute(
            select(User.id).where(User.global_role == "instructor")
        )
        instructor_ids = [row[0] for row in result.all()]
        
        # Send to all instructors
        message = {
            "type": "new_question",
            "data": question_data
        }
        
        for instructor_id in instructor_ids:
            await self.send_to_user(instructor_id, message)
        
        logger.info(f"Broadcasted new question to {len(instructor_ids)} instructors")
    
    async def broadcast_to_all_instructors(self, message: dict, db: AsyncSession):
        """Broadcast a message to all instructors."""
        from database import User
        
        # Get all instructor user IDs
        result = await db.execute(
            select(User.id).where(User.global_role == "instructor")
        )
        instructor_ids = [row[0] for row in result.all()]
        
        # Send to all instructors
        for instructor_id in instructor_ids:
            await self.send_to_user(instructor_id, message)
        
        logger.info(f"Broadcasted message to {len(instructor_ids)} instructors")


# Global instance
manager = ConnectionManager()
