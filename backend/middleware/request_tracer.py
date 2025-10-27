"""
Request Tracing Middleware
==========================

Add trace IDs to all requests for debugging and monitoring
"""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import uuid
import time
from ..utils.logging_config import set_trace_id, get_logger

logger = get_logger(__name__)


class RequestTracerMiddleware(BaseHTTPMiddleware):
    """Add trace ID to all requests"""

    async def dispatch(self, request: Request, call_next):
        # Generate or extract trace ID
        trace_id = request.headers.get('X-Trace-ID')
        if not trace_id:
            trace_id = str(uuid.uuid4())
        
        # Set trace ID in context
        set_trace_id(trace_id)
        
        # Log request start
        start_time = time.time()
        
        logger.info(
            f"Request started",
            extra={
                'extra_data': {
                    'method': request.method,
                    'path': request.url.path,
                    'client_ip': request.client.host if request.client else 'unknown',
                    'user_agent': request.headers.get('User-Agent', 'unknown')
                }
            }
        )
        
        # Process request
        try:
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Log request completion
            logger.info(
                f"Request completed",
                extra={
                    'extra_data': {
                        'method': request.method,
                        'path': request.url.path,
                        'status_code': response.status_code,
                        'duration_ms': round(duration * 1000, 2)
                    }
                }
            )
            
            # Add trace ID to response headers
            response.headers['X-Trace-ID'] = trace_id
            
            return response
            
        except Exception as e:
            # Log error
            duration = time.time() - start_time
            
            logger.error(
                f"Request failed: {str(e)}",
                extra={
                    'extra_data': {
                        'method': request.method,
                        'path': request.url.path,
                        'duration_ms': round(duration * 1000, 2),
                        'error_type': type(e).__name__
                    }
                },
                exc_info=True
            )
            
            raise
