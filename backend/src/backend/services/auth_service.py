"""Authentication service for user login and token management."""
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from backend.exceptions import (
    InvalidCredentialsError,
    TokenExpiredError,
    UserNotFoundError,
    ValidationError,
)
from backend.models.user import User
from backend.services.protocols import (
    DatabaseProtocol,
    TokenServiceProtocol,
    EmailServiceProtocol,
)


@dataclass
class LoginResult:
    """Result of a login attempt."""
    
    success: bool
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    user: Optional[User] = None
    message: Optional[str] = None


@dataclass
class PasswordResetResult:
    """Result of a password reset request."""
    
    success: bool
    message: str


@dataclass
class TokenValidationResult:
    """Result of token validation."""
    
    is_valid: bool
    user: Optional[User] = None
    error: Optional[str] = None


class AuthService:
    """Service for handling authentication operations."""
    
    def __init__(
        self, 
        database: DatabaseProtocol, 
        token_service: TokenServiceProtocol, 
        email_service: EmailServiceProtocol
    ):
        """Initialize the authentication service.
        
        Args:
            database: Database service for user operations
            token_service: Service for token operations  
            email_service: Service for sending emails
        """
        self.database = database
        self.token_service = token_service
        self.email_service = email_service
    
    async def login(self, email: str, password: str) -> LoginResult:
        """Authenticate a user with email and password.
        
        Args:
            email: User's email address
            password: User's password
            
        Returns:
            LoginResult with tokens if successful
            
        Raises:
            ValidationError: If email or password format is invalid
            InvalidCredentialsError: If credentials are invalid
        """
        # Validate email and password
        self._validate_email(email)
        self._validate_password(password)
        
        # Get user by email
        user = await self.database.get_user_by_email(email)
        if not user:
            raise InvalidCredentialsError()
        
        # Check if user is active
        if not user.is_active:
            raise InvalidCredentialsError("Account has been deactivated")
        
        # Verify password
        if not self.token_service.verify_password(password, user.hashed_password):
            raise InvalidCredentialsError()
        
        # Update last login
        await self.database.update_user(
            user.id,
            {"last_login": datetime.utcnow()}
        )
        
        # Generate tokens
        access_token = self.token_service.create_access_token(user.id, user.email)
        refresh_token = self.token_service.create_refresh_token(user.id, user.email)
        
        return LoginResult(
            success=True,
            access_token=access_token,
            refresh_token=refresh_token,
            user=user
        )
    
    async def request_password_reset(self, email: str) -> PasswordResetResult:
        """Request a password reset for the given email.
        
        Args:
            email: User's email address
            
        Returns:
            PasswordResetResult indicating success
        """
        # Always return success to prevent user enumeration
        user = await self.database.get_user_by_email(email)
        
        if user:
            # Generate reset token and send email
            reset_token = self.token_service.create_reset_token(user.id)
            await self.email_service.send_reset_email(
                email=user.email,
                name=user.name,
                reset_token=reset_token
            )
        
        return PasswordResetResult(
            success=True,
            message="Password reset email sent"
        )
    
    async def validate_token(self, token: str) -> TokenValidationResult:
        """Validate an authentication token.
        
        Args:
            token: JWT token to validate
            
        Returns:
            TokenValidationResult with user info if valid
            
        Raises:
            TokenExpiredError: If token has expired
        """
        try:
            payload = self.token_service.decode_token(token)
            user_id = payload.get("sub")
            
            if not user_id:
                return TokenValidationResult(is_valid=False, error="Invalid token")
            
            user = await self.database.get_user_by_id(user_id)
            if not user:
                return TokenValidationResult(is_valid=False, error="User not found")
            
            return TokenValidationResult(is_valid=True, user=user)
            
        except TokenExpiredError:
            raise
        except Exception as e:
            return TokenValidationResult(is_valid=False, error=str(e))
    
    async def validate_password_strength(self, password: str) -> None:
        """Validate password meets security requirements.
        
        Args:
            password: Password to validate
            
        Raises:
            ValidationError: If password doesn't meet requirements
        """
        if not password:
            raise ValidationError("Password is required")
        
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters")
        
        if not re.search(r"[a-zA-Z]", password):
            raise ValidationError("Password must contain letters")
        
        if not re.search(r"\d", password):
            raise ValidationError("Password must contain numbers")
        
        if not re.search(r"[a-z]", password) or not re.search(r"[A-Z]", password):
            raise ValidationError("Password must contain uppercase and lowercase letters")
    
    def _validate_email(self, email: str) -> None:
        """Validate email format.
        
        Args:
            email: Email to validate
            
        Raises:
            ValidationError: If email format is invalid
        """
        if not email:
            raise ValidationError("Email is required")
        
        # Simple email regex pattern
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, email):
            raise ValidationError("Invalid email format")
    
    def _validate_password(self, password: str) -> None:
        """Basic password validation for login.
        
        Args:
            password: Password to validate
            
        Raises:
            ValidationError: If password is empty
        """
        if not password:
            raise ValidationError("Password is required")