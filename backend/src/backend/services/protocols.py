"""Protocol definitions for service interfaces."""
from typing import Protocol, Optional, Dict, Any
from datetime import datetime

from backend.models.user import User


class DatabaseProtocol(Protocol):
    """Protocol for database operations."""
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by their email address.
        
        Args:
            email: User's email address
            
        Returns:
            User object if found, None otherwise
        """
        ...
    
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get a user by their ID.
        
        Args:
            user_id: User's unique identifier
            
        Returns:
            User object if found, None otherwise
        """
        ...
    
    async def update_user(self, user_id: str, data: Dict[str, Any]) -> None:
        """Update user data.
        
        Args:
            user_id: User's unique identifier
            data: Dictionary of fields to update
        """
        ...
    
    async def create_user(self, user_data: Dict[str, Any]) -> User:
        """Create a new user.
        
        Args:
            user_data: Dictionary containing user information
            
        Returns:
            Created user object
        """
        ...


class TokenServiceProtocol(Protocol):
    """Protocol for token management operations."""
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash.
        
        Args:
            plain_password: Plain text password
            hashed_password: Hashed password from database
            
        Returns:
            True if password matches, False otherwise
        """
        ...
    
    def hash_password(self, password: str) -> str:
        """Hash a password for storage.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password string
        """
        ...
    
    def create_access_token(self, user_id: str, email: str) -> str:
        """Create an access token for authenticated user.
        
        Args:
            user_id: User's unique identifier
            email: User's email address
            
        Returns:
            JWT access token string
        """
        ...
    
    def create_refresh_token(self, user_id: str, email: str) -> str:
        """Create a refresh token for authenticated user.
        
        Args:
            user_id: User's unique identifier
            email: User's email address
            
        Returns:
            JWT refresh token string
        """
        ...
    
    def create_reset_token(self, user_id: str) -> str:
        """Create a password reset token.
        
        Args:
            user_id: User's unique identifier
            
        Returns:
            Password reset token string
        """
        ...
    
    def decode_token(self, token: str) -> Dict[str, Any]:
        """Decode and validate a JWT token.
        
        Args:
            token: JWT token string
            
        Returns:
            Token payload dictionary
            
        Raises:
            TokenExpiredError: If token has expired
            InvalidTokenError: If token is invalid
        """
        ...


class EmailServiceProtocol(Protocol):
    """Protocol for email operations."""
    
    async def send_reset_email(
        self, 
        email: str, 
        name: str, 
        reset_token: str
    ) -> None:
        """Send a password reset email.
        
        Args:
            email: Recipient's email address
            name: Recipient's name
            reset_token: Password reset token
        """
        ...
    
    async def send_welcome_email(self, email: str, name: str) -> None:
        """Send a welcome email to new user.
        
        Args:
            email: Recipient's email address
            name: Recipient's name
        """
        ...
    
    async def send_verification_email(
        self, 
        email: str, 
        name: str, 
        verification_token: str
    ) -> None:
        """Send an email verification email.
        
        Args:
            email: Recipient's email address
            name: Recipient's name
            verification_token: Email verification token
        """
        ...