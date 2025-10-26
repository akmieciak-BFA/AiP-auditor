"""
Structured Logging Configuration
=================================

Production-ready logging with trace IDs and structured output
"""

import logging
import sys
import json
import uuid
from datetime import datetime
from contextvars import ContextVar
from typing import Any, Dict

# Context variable for trace ID (thread-safe)
trace_id_var: ContextVar[str] = ContextVar('trace_id', default='')


class StructuredFormatter(logging.Formatter):
    """JSON formatter for structured logging"""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'trace_id': trace_id_var.get(''),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)

        # Add custom fields from extra
        if hasattr(record, 'extra_data'):
            log_data.update(record.extra_data)

        return json.dumps(log_data)


def setup_logging(level: str = 'INFO', structured: bool = True) -> None:
    """
    Setup logging configuration
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        structured: Use structured JSON logging (True) or human-readable (False)
    """
    # Remove existing handlers
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create handler
    handler = logging.StreamHandler(sys.stdout)

    if structured:
        formatter = StructuredFormatter()
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(trace_id)s] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    root_logger.setLevel(level)


def get_logger(name: str) -> logging.Logger:
    """Get logger with name"""
    return logging.getLogger(name)


def set_trace_id(trace_id: str = None) -> str:
    """
    Set trace ID for current context
    
    Args:
        trace_id: Optional trace ID, generated if not provided
        
    Returns:
        The trace ID that was set
    """
    if trace_id is None:
        trace_id = str(uuid.uuid4())
    
    trace_id_var.set(trace_id)
    return trace_id


def get_trace_id() -> str:
    """Get current trace ID"""
    return trace_id_var.get('')


def log_with_context(logger: logging.Logger, level: str, message: str, **kwargs) -> None:
    """
    Log message with additional context
    
    Args:
        logger: Logger instance
        level: Log level (debug, info, warning, error, critical)
        message: Log message
        **kwargs: Additional context data
    """
    extra = {'extra_data': kwargs}
    getattr(logger, level.lower())(message, extra=extra)
