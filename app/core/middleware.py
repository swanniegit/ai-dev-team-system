"""
Custom middleware for the Agentic Agile System API Hub
"""

import time
import uuid
import json
from typing import Callable, Dict, Optional
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import structlog
import redis.asyncio as redis
from datetime import datetime, timedelta

from app.config import settings
from app.core.logging import log_request, log_response, log_audit_event

logger = structlog.get_logger()


class AuditMiddleware(BaseHTTPMiddleware):
    """Middleware for audit logging"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Generate request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # Log request
        start_time = time.time()
        log_request(
            request_id=request_id,
            method=request.method,
            path=str(request.url.path),
            query_params=dict(request.query_params),
            client_ip=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent")
        )
        
        # Process request
        try:
            response = await call_next(request)
            
            # Calculate duration
            duration_ms = (time.time() - start_time) * 1000
            
            # Log response
            log_response(
                request_id=request_id,
                status_code=response.status_code,
                duration_ms=duration_ms
            )
            
            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id
            
            return response
            
        except Exception as e:
            # Log error
            duration_ms = (time.time() - start_time) * 1000
            logger.error(
                "Request failed",
                request_id=request_id,
                error=str(e),
                duration_ms=duration_ms
            )
            raise


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware for rate limiting with Redis backend"""
    
    def __init__(self, app, redis_client: Optional[redis.Redis] = None):
        super().__init__(app)
        self.redis_client = redis_client
        self.rate_limits = {
            'default': {'requests': 100, 'window': 3600},  # 100 requests per hour
            'auth': {'requests': 20, 'window': 300},       # 20 auth requests per 5 minutes
            'api': {'requests': 1000, 'window': 3600},     # 1000 API requests per hour
        }
        
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/ready", "/metrics", "/docs", "/openapi.json"]:
            return await call_next(request)
        
        # Get client identifier and rate limit type
        client_id = await self._get_client_id(request)
        rate_limit_type = self._get_rate_limit_type(request)
        
        # Check rate limit
        is_allowed, retry_after = await self._check_rate_limit(client_id, rate_limit_type)
        
        if not is_allowed:
            logger.warning(
                "Rate limit exceeded",
                client_id=client_id,
                path=request.url.path,
                method=request.method,
                rate_limit_type=rate_limit_type
            )
            
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": "Too many requests. Please try again later.",
                    "retry_after": retry_after,
                    "limit_type": rate_limit_type
                },
                headers={
                    "Retry-After": str(retry_after),
                    "X-RateLimit-Limit": str(self.rate_limits[rate_limit_type]['requests']),
                    "X-RateLimit-Window": str(self.rate_limits[rate_limit_type]['window'])
                }
            )
        
        response = await call_next(request)
        
        # Add rate limit headers to successful responses
        limit_info = self.rate_limits[rate_limit_type]
        response.headers["X-RateLimit-Limit"] = str(limit_info['requests'])
        response.headers["X-RateLimit-Window"] = str(limit_info['window'])
        
        return response
    
    async def _get_client_id(self, request: Request) -> str:
        """Get client identifier for rate limiting"""
        # Try to get user ID from JWT token
        auth_header = request.headers.get("authorization")
        if auth_header and auth_header.startswith("Bearer "):
            try:
                from app.core.security import verify_token
                token = auth_header.split(" ")[1]
                token_data = verify_token(token)
                if token_data and token_data.username:
                    return f"user:{token_data.username}"
            except Exception:
                pass  # Fall back to IP address
        
        # Fall back to IP address
        client_ip = request.client.host if request.client else "unknown"
        
        # Include User-Agent hash for better client identification
        user_agent = request.headers.get("user-agent", "")
        import hashlib
        ua_hash = hashlib.md5(user_agent.encode()).hexdigest()[:8]
        
        return f"ip:{client_ip}:{ua_hash}"
    
    def _get_rate_limit_type(self, request: Request) -> str:
        """Determine rate limit type based on request path"""
        path = request.url.path
        
        if path.startswith("/v1/auth/"):
            return "auth"
        elif path.startswith("/v1/"):
            return "api"
        else:
            return "default"
    
    async def _check_rate_limit(self, client_id: str, rate_limit_type: str) -> tuple[bool, int]:
        """Check if client is within rate limits using sliding window"""
        if not self.redis_client:
            # If no Redis client, allow all requests (fallback)
            return True, 0
        
        try:
            limit_config = self.rate_limits[rate_limit_type]
            max_requests = limit_config['requests']
            window_seconds = limit_config['window']
            
            # Use sliding window rate limiting with Redis
            current_time = int(time.time())
            window_start = current_time - window_seconds
            
            # Redis key for this client and rate limit type
            key = f"rate_limit:{rate_limit_type}:{client_id}"
            
            # Use Redis pipeline for atomic operations
            pipe = self.redis_client.pipeline()
            
            # Remove expired entries
            pipe.zremrangebyscore(key, 0, window_start)
            
            # Count current requests in window
            pipe.zcard(key)
            
            # Add current request
            pipe.zadd(key, {str(current_time): current_time})
            
            # Set expiration
            pipe.expire(key, window_seconds + 10)  # Add buffer
            
            # Execute pipeline
            results = await pipe.execute()
            current_requests = results[1]
            
            # Check if limit exceeded
            if current_requests >= max_requests:
                # Calculate retry after time
                # Get oldest request in current window
                oldest_request = await self.redis_client.zrange(key, 0, 0, withscores=True)
                if oldest_request:
                    oldest_time = int(oldest_request[0][1])
                    retry_after = oldest_time + window_seconds - current_time
                    return False, max(retry_after, 1)
                else:
                    return False, window_seconds
            
            return True, 0
            
        except Exception as e:
            logger.error("Rate limiting error", error=str(e), client_id=client_id)
            # On error, allow the request (fail open)
            return True, 0


class SecurityMiddleware(BaseHTTPMiddleware):
    """Middleware for security headers and CORS"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Handle preflight CORS requests
        if request.method == "OPTIONS":
            response = Response()
            self._add_cors_headers(response, request)
            return response
        
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        
        # Content Security Policy - restrictive but functional
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "frame-ancestors 'none'"
        )
        response.headers["Content-Security-Policy"] = csp
        
        # Add CORS headers for actual requests
        self._add_cors_headers(response, request)
        
        return response
    
    def _add_cors_headers(self, response: Response, request: Request):
        """Add CORS headers based on configuration"""
        origin = request.headers.get("origin")
        
        # Check if origin is allowed
        allowed_origins = getattr(settings, 'cors_origins', [])
        
        if origin and self._is_origin_allowed(origin, allowed_origins):
            response.headers["Access-Control-Allow-Origin"] = origin
        elif not allowed_origins or "*" in allowed_origins:
            response.headers["Access-Control-Allow-Origin"] = "*"
        
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = (
            "Accept, Accept-Language, Content-Language, Content-Type, "
            "Authorization, X-Requested-With, X-Request-ID"
        )
        response.headers["Access-Control-Max-Age"] = "86400"  # 24 hours
        response.headers["Access-Control-Allow-Credentials"] = "true"
    
    def _is_origin_allowed(self, origin: str, allowed_origins: list) -> bool:
        """Check if origin is in allowed list"""
        for allowed_origin in allowed_origins:
            if allowed_origin == "*":
                return True
            elif allowed_origin == origin:
                return True
            elif allowed_origin.startswith("*.") and origin.endswith(allowed_origin[1:]):
                return True
        return False


class RequestSizeLimitMiddleware(BaseHTTPMiddleware):
    """Middleware to limit request body size"""
    
    def __init__(self, app, max_size: int = 10 * 1024 * 1024):  # 10MB default
        super().__init__(app)
        self.max_size = max_size
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Check Content-Length header
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self.max_size:
            return JSONResponse(
                status_code=413,
                content={
                    "error": "Request too large",
                    "message": f"Request body size exceeds maximum allowed size of {self.max_size} bytes",
                    "max_size": self.max_size
                }
            )
        
        return await call_next(request) 