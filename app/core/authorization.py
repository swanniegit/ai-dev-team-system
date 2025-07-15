"""
Authorization and role-based access control (RBAC) for the Agentic Agile System

Provides fine-grained authorization checks, role permissions, and resource access control.
"""

from typing import List, Optional, Dict, Any, Callable
from functools import wraps
from enum import Enum
import structlog
from fastapi import HTTPException, status, Depends

from app.models.user import User, UserRole
from app.core.security import get_current_active_user

logger = structlog.get_logger()


class Permission(str, Enum):
    """System permissions"""
    # User management
    USER_CREATE = "user:create"
    USER_READ = "user:read"
    USER_UPDATE = "user:update"
    USER_DELETE = "user:delete"
    USER_LIST = "user:list"
    
    # Agent management
    AGENT_CREATE = "agent:create"
    AGENT_READ = "agent:read"
    AGENT_UPDATE = "agent:update"
    AGENT_DELETE = "agent:delete"
    AGENT_LIST = "agent:list"
    AGENT_TRIGGER = "agent:trigger"
    AGENT_REGISTER = "agent:register"
    
    # Corporate memory
    MEMORY_CREATE = "memory:create"
    MEMORY_READ = "memory:read"
    MEMORY_UPDATE = "memory:update"
    MEMORY_DELETE = "memory:delete"
    MEMORY_LIST = "memory:list"
    
    # Wellness data
    WELLNESS_CREATE = "wellness:create"
    WELLNESS_READ = "wellness:read"
    WELLNESS_UPDATE = "wellness:update"
    WELLNESS_DELETE = "wellness:delete"
    WELLNESS_LIST = "wellness:list"
    
    # Events and git integration
    EVENT_READ = "event:read"
    EVENT_LIST = "event:list"
    GIT_WEBHOOK = "git:webhook"
    
    # System administration
    SYSTEM_HEALTH = "system:health"
    SYSTEM_ADMIN = "system:admin"
    SYSTEM_METRICS = "system:metrics"


class AuthorizationError(Exception):
    """Authorization error"""
    pass


class InsufficientPermissionsError(AuthorizationError):
    """User lacks required permissions"""
    pass


class ResourceAccessError(AuthorizationError):
    """User cannot access specific resource"""
    pass


# Role-based permissions mapping
ROLE_PERMISSIONS: Dict[UserRole, List[Permission]] = {
    UserRole.ADMIN: [
        # Admins have all permissions
        *list(Permission)
    ],
    
    UserRole.MANAGER: [
        # Managers can manage users, agents, and view most data
        Permission.USER_CREATE,
        Permission.USER_READ,
        Permission.USER_UPDATE,
        Permission.USER_LIST,
        Permission.AGENT_CREATE,
        Permission.AGENT_READ,
        Permission.AGENT_UPDATE,
        Permission.AGENT_DELETE,
        Permission.AGENT_LIST,
        Permission.AGENT_TRIGGER,
        Permission.MEMORY_CREATE,
        Permission.MEMORY_READ,
        Permission.MEMORY_UPDATE,
        Permission.MEMORY_DELETE,
        Permission.MEMORY_LIST,
        Permission.WELLNESS_READ,
        Permission.WELLNESS_LIST,
        Permission.EVENT_READ,
        Permission.EVENT_LIST,
        Permission.SYSTEM_HEALTH,
        Permission.SYSTEM_METRICS,
    ],
    
    UserRole.DEVELOPER: [
        # Developers can manage agents and access development data
        Permission.USER_READ,  # Own profile only
        Permission.AGENT_READ,
        Permission.AGENT_LIST,
        Permission.AGENT_TRIGGER,
        Permission.MEMORY_CREATE,
        Permission.MEMORY_READ,
        Permission.MEMORY_UPDATE,
        Permission.MEMORY_LIST,
        Permission.WELLNESS_CREATE,  # Own wellness data
        Permission.WELLNESS_READ,
        Permission.EVENT_READ,
        Permission.EVENT_LIST,
        Permission.GIT_WEBHOOK,
        Permission.SYSTEM_HEALTH,
    ],
    
    UserRole.QA: [
        # QA can read most data and manage testing-related resources
        Permission.USER_READ,  # Own profile only
        Permission.AGENT_READ,
        Permission.AGENT_LIST,
        Permission.MEMORY_READ,
        Permission.MEMORY_LIST,
        Permission.WELLNESS_CREATE,  # Own wellness data
        Permission.WELLNESS_READ,
        Permission.EVENT_READ,
        Permission.EVENT_LIST,
        Permission.SYSTEM_HEALTH,
    ],
    
    UserRole.VIEWER: [
        # Viewers have minimal read-only access
        Permission.USER_READ,  # Own profile only
        Permission.AGENT_READ,
        Permission.AGENT_LIST,
        Permission.MEMORY_READ,
        Permission.WELLNESS_READ,  # Own wellness data only
        Permission.EVENT_READ,
    ],
}


def get_user_permissions(user: User) -> List[Permission]:
    """Get all permissions for a user based on their role"""
    return ROLE_PERMISSIONS.get(user.role, [])


def has_permission(user: User, permission: Permission) -> bool:
    """Check if user has a specific permission"""
    user_permissions = get_user_permissions(user)
    return permission in user_permissions


def check_permission(user: User, permission: Permission, resource_id: Optional[str] = None):
    """Check permission and raise exception if not authorized"""
    if not has_permission(user, permission):
        logger.warning(
            "Permission denied",
            user_id=user.id,
            username=user.username,
            role=user.role,
            permission=permission,
            resource_id=resource_id
        )
        raise InsufficientPermissionsError(
            f"User {user.username} lacks permission: {permission}"
        )


def check_resource_access(user: User, resource_type: str, resource_id: str, owner_id: Optional[str] = None):
    """Check if user can access a specific resource"""
    # Admins can access everything
    if user.role == UserRole.ADMIN:
        return
    
    # Managers can access most resources
    if user.role == UserRole.MANAGER:
        return
    
    # For other roles, check ownership or specific rules
    if resource_type in ["user", "wellness"] and owner_id:
        # Users can only access their own user profile and wellness data
        if user.id != owner_id:
            logger.warning(
                "Resource access denied",
                user_id=user.id,
                username=user.username,
                resource_type=resource_type,
                resource_id=resource_id,
                owner_id=owner_id
            )
            raise ResourceAccessError(
                f"User {user.username} cannot access {resource_type} {resource_id}"
            )


def require_permission(permission: Permission):
    """Decorator to require specific permission for endpoint access"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract current user from dependencies
            current_user = None
            for key, value in kwargs.items():
                if isinstance(value, User):
                    current_user = value
                    break
            
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            check_permission(current_user, permission)
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator


def require_role(required_role: UserRole):
    """Decorator to require specific role for endpoint access"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract current user from dependencies
            current_user = None
            for key, value in kwargs.items():
                if isinstance(value, User):
                    current_user = value
                    break
            
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            # Check if user has required role or higher
            role_hierarchy = {
                UserRole.VIEWER: 1,
                UserRole.QA: 2,
                UserRole.DEVELOPER: 3,
                UserRole.MANAGER: 4,
                UserRole.ADMIN: 5
            }
            
            user_level = role_hierarchy.get(current_user.role, 0)
            required_level = role_hierarchy.get(required_role, 5)
            
            if user_level < required_level:
                logger.warning(
                    "Role requirement not met",
                    user_id=current_user.id,
                    username=current_user.username,
                    user_role=current_user.role,
                    required_role=required_role
                )
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Role {required_role} or higher required"
                )
            
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator


def require_owner_or_admin(resource_owner_field: str = "user_id"):
    """Decorator to require resource ownership or admin role"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract current user
            current_user = None
            for key, value in kwargs.items():
                if isinstance(value, User):
                    current_user = value
                    break
            
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            # Admins can access everything
            if current_user.role == UserRole.ADMIN:
                return await func(*args, **kwargs)
            
            # Extract resource owner ID from kwargs
            resource_owner_id = kwargs.get(resource_owner_field)
            if not resource_owner_id:
                # If no owner specified, only admins can access
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied"
                )
            
            # Check ownership
            if current_user.id != resource_owner_id:
                logger.warning(
                    "Ownership requirement not met",
                    user_id=current_user.id,
                    username=current_user.username,
                    resource_owner_id=resource_owner_id
                )
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only access your own resources"
                )
            
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator


# Dependency injection functions for FastAPI
async def require_authenticated_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Dependency that ensures user is authenticated"""
    return current_user


async def require_admin_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Dependency that ensures user is admin"""
    if current_user.role != UserRole.ADMIN:
        logger.warning(
            "Admin access denied",
            user_id=current_user.id,
            username=current_user.username,
            role=current_user.role
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required"
        )
    return current_user


async def require_manager_or_admin(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Dependency that ensures user is manager or admin"""
    if current_user.role not in [UserRole.MANAGER, UserRole.ADMIN]:
        logger.warning(
            "Manager access denied",
            user_id=current_user.id,
            username=current_user.username,
            role=current_user.role
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Manager or Administrator access required"
        )
    return current_user


def check_user_permission(permission: Permission):
    """Dependency factory for permission checking"""
    async def permission_checker(
        current_user: User = Depends(get_current_active_user)
    ) -> User:
        try:
            check_permission(current_user, permission)
            return current_user
        except InsufficientPermissionsError as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )
    
    return permission_checker


def log_access_attempt(
    user: User,
    resource_type: str,
    resource_id: Optional[str] = None,
    action: str = "access",
    success: bool = True
):
    """Log access attempts for audit purposes"""
    logger.info(
        "Resource access attempt",
        user_id=user.id,
        username=user.username,
        role=user.role,
        resource_type=resource_type,
        resource_id=resource_id,
        action=action,
        success=success
    )


# Context manager for authorization
class AuthorizationContext:
    """Context manager for handling authorization in complex operations"""
    
    def __init__(self, user: User, operation: str):
        self.user = user
        self.operation = operation
        self.permissions_checked = []
        self.resources_accessed = []
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Log the authorization context
        logger.info(
            "Authorization context completed",
            user_id=self.user.id,
            username=self.user.username,
            operation=self.operation,
            permissions_checked=self.permissions_checked,
            resources_accessed=self.resources_accessed,
            success=exc_type is None
        )
    
    def check_permission(self, permission: Permission):
        """Check permission within context"""
        check_permission(self.user, permission)
        self.permissions_checked.append(permission)
    
    def access_resource(self, resource_type: str, resource_id: str, owner_id: Optional[str] = None):
        """Access resource within context"""
        check_resource_access(self.user, resource_type, resource_id, owner_id)
        self.resources_accessed.append({
            "type": resource_type,
            "id": resource_id,
            "owner_id": owner_id
        })


__all__ = [
    'Permission',
    'UserRole',
    'AuthorizationError',
    'InsufficientPermissionsError',
    'ResourceAccessError',
    'get_user_permissions',
    'has_permission',
    'check_permission',
    'check_resource_access',
    'require_permission',
    'require_role',
    'require_owner_or_admin',
    'require_authenticated_user',
    'require_admin_user',
    'require_manager_or_admin',
    'check_user_permission',
    'log_access_attempt',
    'AuthorizationContext'
]