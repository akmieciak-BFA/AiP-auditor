from fastapi import Request, HTTPException, status
from datetime import datetime, timedelta
from collections import defaultdict
import threading

# Simple in-memory rate limiter (for production use Redis)
class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)
        self.lock = threading.Lock()
    
    def is_allowed(self, key: str, max_requests: int, window_seconds: int) -> bool:
        """Check if request is allowed based on rate limit."""
        now = datetime.utcnow()
        cutoff = now - timedelta(seconds=window_seconds)
        
        with self.lock:
            # Clean old requests
            self.requests[key] = [
                req_time for req_time in self.requests[key]
                if req_time > cutoff
            ]
            
            # Check if limit exceeded
            if len(self.requests[key]) >= max_requests:
                return False
            
            # Add current request
            self.requests[key].append(now)
            return True
    
    def get_retry_after(self, key: str, window_seconds: int) -> int:
        """Get seconds until rate limit resets."""
        if not self.requests[key]:
            return 0
        
        oldest = min(self.requests[key])
        reset_time = oldest + timedelta(seconds=window_seconds)
        retry_after = (reset_time - datetime.utcnow()).total_seconds()
        return max(0, int(retry_after))

# Global rate limiter instance
rate_limiter = RateLimiter()


def rate_limit(max_requests: int = 60, window_seconds: int = 60):
    """
    Rate limiting decorator.
    Default: 60 requests per minute per IP.
    """
    async def dependency(request: Request):
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"
        
        # Check rate limit
        if not rate_limiter.is_allowed(client_ip, max_requests, window_seconds):
            retry_after = rate_limiter.get_retry_after(client_ip, window_seconds)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "Przekroczono limit żądań",
                    "message": f"Maksymalnie {max_requests} żądań na {window_seconds} sekund",
                    "retry_after": retry_after
                },
                headers={"Retry-After": str(retry_after)}
            )
        
        return True
    
    return dependency


# Specific rate limiters for different endpoints
ai_analysis_rate_limit = rate_limit(max_requests=10, window_seconds=300)  # 10 per 5 min
form_generation_rate_limit = rate_limit(max_requests=5, window_seconds=300)  # 5 per 5 min
auth_rate_limit = rate_limit(max_requests=5, window_seconds=60)  # 5 per minute
