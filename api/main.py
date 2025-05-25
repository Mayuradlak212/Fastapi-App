from fastapi import FastAPI, Request, Depends, APIRouter, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
import time
import os
from typing import Annotated, List
import json
from datetime import datetime
from pydantic import BaseModel

# Since Vercel has limitations with file structure, we'll inline the routes and middleware

app = FastAPI(title="Chat App with WebSocket")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple auth middleware inline
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class SimpleAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, excluded_paths: List[str] = None):
        super().__init__(app)
        self.excluded_paths = excluded_paths or ["/docs", "/redoc", "/openapi.json"]
    
    async def dispatch(self, request: Request, call_next):
        if any(request.url.path.startswith(path) for path in self.excluded_paths):
            return await call_next(request)
        
        token = self.get_token(request)
        if not token:
            return JSONResponse(
                status_code=401,
                content={
                    "status_code": 401,
                    "success": False,
                    "message": "Token required",
                    "data": None
                }
            )
        return await call_next(request)
    
    def get_token(self, request: Request) -> str:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            return auth_header.replace("Bearer ", "")
        return request.query_params.get("token")

# Add auth middleware
app.add_middleware(
    SimpleAuthMiddleware,
    excluded_paths=["/", "/chat", "/docs", "/redoc", "/openapi.json", "/api/posts", "/api/products", "/api/users"]
)

# Inline API routes
import aiohttp
from typing import Optional

api_router = APIRouter(prefix="/api", tags=["data"])

@api_router.get("/posts")
async def get_posts():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://dummyjson.com/posts") as response:
                if response.status == 200:
                    data = await response.json()
                    return JSONResponse({
                        "status_code": 200,
                        "success": True,
                        "message": "Posts fetched successfully",
                        "data": data.get("posts", []),
                        "total": data.get("total", 0)
                    })
                else:
                    return JSONResponse({
                        "status_code": response.status,
                        "success": False,
                        "message": f"Failed to fetch posts: {response.status}",
                        "data": []
                    })
    except Exception as e:
        return JSONResponse({
            "status_code": 500,
            "success": False,
            "message": f"Internal server error: {str(e)}",
            "data": []
        })

@api_router.get("/products")
async def get_products(limit: Optional[int] = None, skip: Optional[int] = None):
    try:
        url = "https://dummyjson.com/products"
        params = {}
        if limit is not None:
            params["limit"] = limit
        if skip is not None:
            params["skip"] = skip
            
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return JSONResponse({
                        "status_code": 200,
                        "success": True,
                        "message": "Products fetched successfully",
                        "data": data.get("products", []),
                        "total": data.get("total", 0)
                    })
                else:
                    return JSONResponse({
                        "status_code": response.status,
                        "success": False,
                        "message": f"Failed to fetch products: {response.status}",
                        "data": []
                    })
    except Exception as e:
        return JSONResponse({
            "status_code": 500,
            "success": False,
            "message": f"Internal server error: {str(e)}",
            "data": []
        })

app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "FastAPI app running on Vercel!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Vercel handler
from mangum import Mangum
handler = Mangum(app)