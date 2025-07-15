"""
Comprehensive input validation utilities for the Agentic Agile System

Provides custom validators, sanitizers, and security checks for all user inputs.
"""

import re
import html
import bleach
from typing import Any, List, Optional, Dict, Union
from pydantic import validator, BaseModel, Field
from datetime import datetime
import structlog

logger = structlog.get_logger()

# Security patterns
DANGEROUS_PATTERNS = [
    r'<script[^>]*>.*?</script>',
    r'javascript:',
    r'on\w+\s*=',
    r'data:text/html',
    r'eval\s*\(',
    r'expression\s*\(',
    r'@import',
    r'<iframe',
    r'<object',
    r'<embed',
    r'<link',
    r'<meta'
]

# SQL injection patterns
SQL_INJECTION_PATTERNS = [
    r"('|(\\')|(--)|(-)|(\;)|(\|)|(\*)|(\%)",
    r"((\%3D)|(=))[^\n]*((\%27)|(')|((\%3B)|(;))",
    r"\w*((\%27)|(\'))((\%6F)|o|(\%4F))((\%72)|r|(\%52))",
    r"((\%27)|(\'))union",
    r"exec(\s|\+)+(s|x)p\w+",
    r"union[\w\s]*select",
    r"select.*from",
    r"insert.*into",
    r"delete.*from",
    r"update.*set",
    r"drop.*table"
]

# Command injection patterns
COMMAND_INJECTION_PATTERNS = [
    r"[;&|`]",
    r"\$\(",
    r"`.*`",
    r"\|\s*(cat|ls|pwd|id|whoami|uname)",
    r"(nc|netcat|wget|curl)\s",
    r"(chmod|chown|rm|mv|cp)\s",
    r"\.\./",
    r"/etc/passwd",
    r"/bin/",
    r"/usr/bin/",
    r"powershell",
    r"cmd\.exe"
]


class ValidationError(Exception):
    """Custom validation error"""
    pass


class SecurityValidationError(ValidationError):
    """Security-related validation error"""
    pass


def sanitize_html(value: str, allowed_tags: List[str] = None) -> str:
    """Sanitize HTML content"""
    if not isinstance(value, str):
        return value
    
    # Default allowed tags (very restrictive)
    if allowed_tags is None:
        allowed_tags = ['b', 'i', 'em', 'strong', 'p', 'br']
    
    # Clean HTML
    cleaned = bleach.clean(
        value,
        tags=allowed_tags,
        attributes={},
        strip=True
    )
    
    # Additional HTML entity encoding
    cleaned = html.escape(cleaned, quote=False)
    
    return cleaned


def validate_no_dangerous_content(value: str) -> str:
    """Validate that content doesn't contain dangerous patterns"""
    if not isinstance(value, str):
        return value
    
    value_lower = value.lower()
    
    # Check for dangerous patterns
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, value_lower, re.IGNORECASE | re.DOTALL):
            logger.warning(
                "Dangerous pattern detected in input",
                pattern=pattern,
                input_preview=value[:100]
            )
            raise SecurityValidationError(f"Input contains potentially dangerous content")
    
    return value


def validate_no_sql_injection(value: str) -> str:
    """Validate that content doesn't contain SQL injection patterns"""
    if not isinstance(value, str):
        return value
    
    value_lower = value.lower()
    
    # Check for SQL injection patterns
    for pattern in SQL_INJECTION_PATTERNS:
        if re.search(pattern, value_lower, re.IGNORECASE):
            logger.warning(
                "SQL injection pattern detected",
                pattern=pattern,
                input_preview=value[:100]
            )
            raise SecurityValidationError("Input contains potentially malicious SQL patterns")
    
    return value


def validate_no_command_injection(value: str) -> str:
    """Validate that content doesn't contain command injection patterns"""
    if not isinstance(value, str):
        return value
    
    # Check for command injection patterns
    for pattern in COMMAND_INJECTION_PATTERNS:
        if re.search(pattern, value, re.IGNORECASE):
            logger.warning(
                "Command injection pattern detected",
                pattern=pattern,
                input_preview=value[:100]
            )
            raise SecurityValidationError("Input contains potentially malicious command patterns")
    
    return value


def validate_safe_filename(filename: str) -> str:
    """Validate that filename is safe"""
    if not isinstance(filename, str):
        raise ValidationError("Filename must be a string")
    
    # Check for path traversal
    if '..' in filename or '/' in filename or '\\' in filename:
        raise SecurityValidationError("Filename contains path traversal characters")
    
    # Check for dangerous characters
    dangerous_chars = ['<', '>', ':', '"', '|', '?', '*', '\0']
    if any(char in filename for char in dangerous_chars):
        raise SecurityValidationError("Filename contains dangerous characters")
    
    # Check length
    if len(filename) > 255:
        raise ValidationError("Filename too long")
    
    # Check for empty or whitespace-only
    if not filename.strip():
        raise ValidationError("Filename cannot be empty")
    
    return filename.strip()


def validate_safe_url(url: str) -> str:
    """Validate that URL is safe"""
    if not isinstance(url, str):
        return url
    
    url_lower = url.lower()
    
    # Only allow http/https
    if not (url_lower.startswith('http://') or url_lower.startswith('https://')):
        raise SecurityValidationError("URL must use HTTP or HTTPS protocol")
    
    # Block dangerous protocols
    dangerous_protocols = ['javascript:', 'data:', 'file:', 'ftp:']
    if any(url_lower.startswith(proto) for proto in dangerous_protocols):
        raise SecurityValidationError("URL uses dangerous protocol")
    
    # Check for suspicious patterns
    if re.search(r'[<>\'"&]', url):
        raise SecurityValidationError("URL contains suspicious characters")
    
    return url


def validate_alphanumeric_with_special(value: str, allowed_special: str = "_-") -> str:
    """Validate alphanumeric string with specific special characters"""
    if not isinstance(value, str):
        return value
    
    pattern = f"^[a-zA-Z0-9{re.escape(allowed_special)}]+$"
    if not re.match(pattern, value):
        raise ValidationError(f"Value must contain only letters, numbers, and {allowed_special}")
    
    return value


def validate_json_safe(value: Any) -> Any:
    """Validate that a value is JSON-safe"""
    try:
        import json
        json.dumps(value)
        return value
    except (TypeError, ValueError) as e:
        raise ValidationError(f"Value is not JSON serializable: {e}")


def normalize_whitespace(value: str) -> str:
    """Normalize whitespace in string"""
    if not isinstance(value, str):
        return value
    
    # Replace multiple whitespace with single space
    value = re.sub(r'\s+', ' ', value)
    # Strip leading/trailing whitespace
    return value.strip()


class SecureStr(str):
    """A string type that automatically applies security validation"""
    
    def __new__(cls, value):
        if isinstance(value, str):
            # Apply all security validations
            value = validate_no_dangerous_content(value)
            value = validate_no_sql_injection(value)
            value = validate_no_command_injection(value)
            value = normalize_whitespace(value)
        return super().__new__(cls, value)


class SafeHTML(str):
    """A string type for safe HTML content"""
    
    def __new__(cls, value, allowed_tags=None):
        if isinstance(value, str):
            value = sanitize_html(value, allowed_tags)
        return super().__new__(cls, value)


# Custom Pydantic validators
def validate_secure_string(cls, v):
    """Pydantic validator for secure strings"""
    if v is None:
        return v
    return SecureStr(v)


def validate_safe_html(cls, v):
    """Pydantic validator for safe HTML"""
    if v is None:
        return v
    return SafeHTML(v)


def validate_username(cls, v):
    """Validate username format"""
    if not isinstance(v, str):
        raise ValueError("Username must be a string")
    
    if len(v) < 3:
        raise ValueError("Username must be at least 3 characters")
    
    if len(v) > 50:
        raise ValueError("Username must be less than 50 characters")
    
    # Only allow alphanumeric and underscore
    if not re.match(r"^[a-zA-Z0-9_]+$", v):
        raise ValueError("Username can only contain letters, numbers, and underscores")
    
    # Must start with letter
    if not v[0].isalpha():
        raise ValueError("Username must start with a letter")
    
    return v.lower()


def validate_email_format(cls, v):
    """Enhanced email validation"""
    if not isinstance(v, str):
        raise ValueError("Email must be a string")
    
    # Basic email pattern (more restrictive than RFC)
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_pattern, v):
        raise ValueError("Invalid email format")
    
    # Additional security checks
    if len(v) > 254:
        raise ValueError("Email address too long")
    
    # Check for dangerous characters
    if re.search(r'[<>"\'\\\x00-\x1f\x7f-\x9f]', v):
        raise ValueError("Email contains invalid characters")
    
    return v.lower()


def validate_password_strength(cls, v):
    """Validate password strength"""
    if not isinstance(v, str):
        raise ValueError("Password must be a string")
    
    if len(v) < 8:
        raise ValueError("Password must be at least 8 characters long")
    
    if len(v) > 128:
        raise ValueError("Password must be less than 128 characters")
    
    # Check for at least one uppercase, lowercase, digit, and special character
    has_upper = re.search(r'[A-Z]', v)
    has_lower = re.search(r'[a-z]', v)
    has_digit = re.search(r'\d', v)
    has_special = re.search(r'[!@#$%^&*(),.?":{}|<>]', v)
    
    if not all([has_upper, has_lower, has_digit, has_special]):
        raise ValueError(
            "Password must contain at least one uppercase letter, "
            "one lowercase letter, one digit, and one special character"
        )
    
    # Check for common weak patterns
    weak_patterns = [
        r'(.)\1{2,}',  # Three or more repeated characters
        r'(012|123|234|345|456|567|678|789|890)',  # Sequential numbers
        r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)',  # Sequential letters
    ]
    
    for pattern in weak_patterns:
        if re.search(pattern, v.lower()):
            raise ValueError("Password contains weak patterns")
    
    return v


def validate_agent_name(cls, v):
    """Validate agent name"""
    if not isinstance(v, str):
        raise ValueError("Agent name must be a string")
    
    if len(v) < 2:
        raise ValueError("Agent name must be at least 2 characters")
    
    if len(v) > 100:
        raise ValueError("Agent name must be less than 100 characters")
    
    # Allow letters, numbers, spaces, hyphens, underscores
    if not re.match(r"^[a-zA-Z0-9\s\-_]+$", v):
        raise ValueError("Agent name can only contain letters, numbers, spaces, hyphens, and underscores")
    
    return normalize_whitespace(v)


def validate_project_name(cls, v):
    """Validate project name"""
    if not isinstance(v, str):
        raise ValueError("Project name must be a string")
    
    if len(v) < 2:
        raise ValueError("Project name must be at least 2 characters")
    
    if len(v) > 200:
        raise ValueError("Project name must be less than 200 characters")
    
    # Allow letters, numbers, spaces, and common punctuation
    if not re.match(r"^[a-zA-Z0-9\s\-_.()]+$", v):
        raise ValueError("Project name contains invalid characters")
    
    return normalize_whitespace(v)


# Common validation mixins
class SecureInputMixin(BaseModel):
    """Mixin for models that need secure input validation"""
    
    @validator('*', pre=True)
    def validate_strings(cls, v):
        """Apply security validation to all string fields"""
        if isinstance(v, str) and len(v.strip()) > 0:
            return validate_secure_string(cls, v)
        return v


class TimestampMixin(BaseModel):
    """Mixin for models with timestamp validation"""
    
    @validator('created_at', 'updated_at', 'timestamp', pre=True)
    def validate_timestamps(cls, v):
        """Validate timestamp fields"""
        if v is None:
            return v
        
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                raise ValueError("Invalid timestamp format")
        
        if isinstance(v, datetime):
            return v
        
        raise ValueError("Timestamp must be a datetime object or ISO format string")


# Export commonly used validators
__all__ = [
    'sanitize_html',
    'validate_no_dangerous_content',
    'validate_no_sql_injection',
    'validate_no_command_injection',
    'validate_safe_filename',
    'validate_safe_url',
    'validate_alphanumeric_with_special',
    'validate_json_safe',
    'normalize_whitespace',
    'SecureStr',
    'SafeHTML',
    'validate_secure_string',
    'validate_safe_html',
    'validate_username',
    'validate_email_format',
    'validate_password_strength',
    'validate_agent_name',
    'validate_project_name',
    'SecureInputMixin',
    'TimestampMixin',
    'ValidationError',
    'SecurityValidationError'
]