import re
import html
from typing import Any, Dict
from fastapi import HTTPException, status

def sanitize_string(text: str, max_length: int = 10000) -> str:
    """Sanitize string input to prevent XSS and injection attacks."""
    if not text:
        return ""
    
    # Trim to max length
    text = text[:max_length]
    
    # Remove null bytes
    text = text.replace('\x00', '')
    
    # HTML escape
    text = html.escape(text)
    
    # Remove potentially dangerous patterns
    dangerous_patterns = [
        r'<script[^>]*>.*?</script>',
        r'javascript:',
        r'on\w+\s*=',
        r'<iframe[^>]*>.*?</iframe>',
    ]
    
    for pattern in dangerous_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.DOTALL)
    
    return text


def sanitize_dict(data: Dict[str, Any], max_depth: int = 5) -> Dict[str, Any]:
    """Recursively sanitize dictionary values."""
    if max_depth <= 0:
        return data
    
    sanitized = {}
    for key, value in data.items():
        # Sanitize key
        clean_key = sanitize_string(str(key), max_length=100)
        
        # Sanitize value based on type
        if isinstance(value, str):
            sanitized[clean_key] = sanitize_string(value)
        elif isinstance(value, dict):
            sanitized[clean_key] = sanitize_dict(value, max_depth - 1)
        elif isinstance(value, list):
            sanitized[clean_key] = [
                sanitize_string(item) if isinstance(item, str) else item
                for item in value[:1000]  # Limit list size
            ]
        else:
            sanitized[clean_key] = value
    
    return sanitized


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_project_name(name: str) -> bool:
    """Validate project name."""
    if not name or len(name) < 3 or len(name) > 100:
        return False
    # Allow alphanumeric, spaces, and some special chars
    pattern = r'^[a-zA-Z0-9\s\-_\.]+$'
    return bool(re.match(pattern, name))


def check_sql_injection(text: str) -> bool:
    """Check for common SQL injection patterns."""
    sql_patterns = [
        r'(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE)\b)',
        r'(--|\#|\/\*)',
        r'(\bOR\b.*=.*)',
        r'(\bAND\b.*=.*)',
        r'(;\s*(SELECT|INSERT|UPDATE|DELETE))',
    ]
    
    for pattern in sql_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    
    return False


def validate_input(text: str, field_name: str = "Input", max_length: int = 10000) -> str:
    """Comprehensive input validation."""
    if not text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{field_name} nie może być pusty"
        )
    
    if len(text) > max_length:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{field_name} jest za długi (max {max_length} znaków)"
        )
    
    if check_sql_injection(text):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{field_name} zawiera niedozwolone znaki"
        )
    
    return sanitize_string(text, max_length)
