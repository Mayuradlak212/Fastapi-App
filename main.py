from fastapi import FastAPI, Request, Depends, APIRouter, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import time
from typing import Annotated, List
import json
from datetime import datetime
from pydantic import BaseModel

# Import your existing routes and middleware
from controller.index import routes
from middleware.index import SimpleAuthMiddleware

app = FastAPI(title="Chat App with WebSocket")

# Templates setup
templates = Jinja2Templates(directory="templates")

# Static files (for CSS, JS, images)
# app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth middleware (exclude chat routes from token requirement)
app.add_middleware(
    SimpleAuthMiddleware,
    excluded_paths=["/", "/chat", "/docs", "/redoc", "/openapi.json", "/static"]
)

# Pydantic models
class Message(BaseModel):
    username: str
    message: str
    timestamp: str

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.chat_history: List[dict] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: dict):
        # Add to chat history
        self.chat_history.append(message)
        # Keep only last 100 messages
        if len(self.chat_history) > 100:
            self.chat_history.pop(0)
        
        # Broadcast to all connected clients
        message_json = json.dumps(message)
        for connection in self.active_connections:
            try:
                await connection.send_text(message_json)
            except:
                # Remove broken connections
                self.active_connections.remove(connection)

    def get_chat_history(self):
        return self.chat_history

manager = ConnectionManager()

# Chat routes
@app.get("/", response_class=HTMLResponse)
async def get_chat_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/chat", response_class=HTMLResponse)
async def get_chat_room(request: Request):
    chat_history = manager.get_chat_history()
    return templates.TemplateResponse("chat.html", {
        "request": request, 
        "chat_history": chat_history
    })

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    
    # Send welcome message
    welcome_msg = {
        "username": "System",
        "message": f"{client_id} joined the chat!",
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "type": "system"
    }
    await manager.broadcast(welcome_msg)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Create message object
            chat_message = {
                "username": client_id,
                "message": message_data.get("message", ""),
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "type": "user"
            }
            
            # Broadcast message to all clients
            await manager.broadcast(chat_message)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        
        # Send disconnect message
        disconnect_msg = {
            "username": "System",
            "message": f"{client_id} left the chat!",
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "type": "system"
        }
        await manager.broadcast(disconnect_msg)

# API to get online users count
@app.get("/api/online-users")
async def get_online_users():
    return {
        "success": True,
        "online_users": len(manager.active_connections),
        "timestamp": time.asctime()
    }

# Include your existing API routes
app.include_router(routes)

# Your existing routes
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    print("All Common ", commons["q"])
    return commons

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)