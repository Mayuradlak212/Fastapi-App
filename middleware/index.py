from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import List

class SimpleAuthMiddleware(BaseHTTPMiddleware):
    """
    Simple middleware to check if token exists in request
    """
    
    def __init__(self, app, excluded_paths: List[str] = None):
        super().__init__(app)
        self.excluded_paths = excluded_paths or ["/docs", "/redoc", "/openapi.json"]
    
    async def dispatch(self, request: Request, call_next):
        # Skip auth for excluded paths
        if any(request.url.path.startswith(path) for path in self.excluded_paths):
            return await call_next(request)
        
        # Check if token exists
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
        
        # Token exists, continue
        return await call_next(request)
    
    def get_token(self, request: Request) -> str:
        """Get token from header or query parameter"""
        # Check Authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            return auth_header.replace("Bearer ", "")
        
        # Check query parameter
        return request.query_params.get("token")

