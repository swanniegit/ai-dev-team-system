"""
Structured logging configuration
"""

import sys
import structlog
from typing import Any, Dict
from app.config import settings


def setup_logging():
    """Setup structured logging with structlog"""
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Configure standard library logging
    import logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.log_level.upper()),
    )


def get_logger(name: str = None):
    """Get a structured logger"""
    return structlog.get_logger(name)


def log_request(request_id: str, method: str, path: str, **kwargs):
    """Log HTTP request"""
    logger = get_logger("http.request")
    logger.info(
        "HTTP request",
        request_id=request_id,
        method=method,
        path=path,
        **kwargs
    )


def log_response(request_id: str, status_code: int, duration_ms: float, **kwargs):
    """Log HTTP response"""
    logger = get_logger("http.response")
    logger.info(
        "HTTP response",
        request_id=request_id,
        status_code=status_code,
        duration_ms=duration_ms,
        **kwargs
    )


def log_agent_action(agent_id: str, action: str, **kwargs):
    """Log agent action"""
    logger = get_logger("agent.action")
    logger.info(
        "Agent action",
        agent_id=agent_id,
        action=action,
        **kwargs
    )


def log_audit_event(user_id: str = None, agent_id: str = None, action: str = None, **kwargs):
    """Log audit event"""
    logger = get_logger("audit.event")
    logger.info(
        "Audit event",
        user_id=user_id,
        agent_id=agent_id,
        action=action,
        **kwargs
    ) 