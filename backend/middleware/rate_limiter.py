"""
Rate Limiting Middleware
========================

Protect API from abuse with rate limiting
"""

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, Tuple
import time


class RateLimiter(BaseHTTPMiddleware):
    """
    Simple in-memory rate limiter
    
    For production, use Redis-based rate limiting (e.g., slowapi)
    """

    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = defaultdict(list)
        self.cleanup_interval = 60  # seconds
        self.last_cleanup = time.time()

    def _cleanup_old_requests(self):
        """Remove requests older than 1 minute"""
        current_time = time.time()
        
        if current_time - self.last_cleanup < self.cleanup_interval:
            return
        
        cutoff_time = current_time - 60
        for ip in list(self.requests.keys()):
            self.requests[ip] = [
                req_time for req_time in self.requests[ip] 
                if req_time > cutoff_time
            ]
            if not self.requests[ip]:
                del self.requests[ip]
        
        self.last_cleanup = current_time

    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP from request"""
        # Check for forwarded headers (proxy/load balancer)
        forwarded = request.headers.get('X-Forwarded-For')
        if forwarded:
            return forwarded.split(',')[0].strip()
        
        real_ip = request.headers.get('X-Real-IP')
        if real_ip:
            return real_ip
        
        # Fallback to direct connection
        return request.client.host if request.client else 'unknown'

    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for health check
        if request.url.path == '/api/calculator/health':
            return await call_next(request)

        client_ip = self._get_client_ip(request)
        current_time = time.time()

        # Cleanup old requests periodically
        self._cleanup_old_requests()

        # Check rate limit
        recent_requests = [
            req_time for req_time in self.requests[client_ip]
            if current_time - req_time < 60
        ]

        if len(recent_requests) >= self.requests_per_minute:
            return JSONResponse(
                status_code=429,
                content={
                    'error': 'Too Many Requests',
                    'message': f'Rate limit exceeded. Maximum {self.requests_per_minute} requests per minute.',
                    'retry_after': 60
                },
                headers={'Retry-After': '60'}
            )

        # Record this request
        self.requests[client_ip].append(current_time)

        # Process request
        response = await call_next(request)
        
        # Add rate limit headers
        remaining = self.requests_per_minute - len(self.requests[client_ip])
        response.headers['X-RateLimit-Limit'] = str(self.requests_per_minute)
        response.headers['X-RateLimit-Remaining'] = str(max(0, remaining))
        response.headers['X-RateLimit-Reset'] = str(int(current_time) + 60)

        return response


class AdvancedRateLimiter:
    """
    Advanced rate limiter with multiple tiers
    
    Usage with Redis in production:
    - Install: pip install redis slowapi
    - Use slowapi for Redis-backed rate limiting
    """

    LIMITS = {
        'default': 60,      # 60 requests per minute
        'premium': 300,     # 300 requests per minute
        'unlimited': 999999 # Practically unlimited
    }

    def __init__(self, redis_client=None):
        self.redis = redis_client
        self.fallback_limiter = {}  # In-memory fallback

    def get_tier(self, api_key: str) -> str:
        """
        Determine rate limit tier based on API key
        
        For production: Query database or Redis
        """
        # Placeholder - implement actual tier lookup
        if api_key and api_key.startswith('premium_'):
            return 'premium'
        elif api_key and api_key.startswith('unlimited_'):
            return 'unlimited'
        return 'default'

    def check_rate_limit(self, identifier: str, tier: str = 'default') -> Tuple[bool, int]:
        """
        Check if request is within rate limit
        
        Returns:
            (is_allowed, remaining_requests)
        """
        limit = self.LIMITS[tier]
        
        # Redis implementation (for production)
        if self.redis:
            key = f'rate_limit:{identifier}'
            current = self.redis.incr(key)
            if current == 1:
                self.redis.expire(key, 60)  # 60 seconds TTL
            
            remaining = max(0, limit - current)
            return current <= limit, remaining
        
        # Fallback in-memory implementation
        current_time = time.time()
        minute_ago = current_time - 60
        
        if identifier not in self.fallback_limiter:
            self.fallback_limiter[identifier] = []
        
        # Remove old requests
        self.fallback_limiter[identifier] = [
            req_time for req_time in self.fallback_limiter[identifier]
            if req_time > minute_ago
        ]
        
        # Add current request
        self.fallback_limiter[identifier].append(current_time)
        
        current_count = len(self.fallback_limiter[identifier])
        remaining = max(0, limit - current_count)
        
        return current_count <= limit, remaining
