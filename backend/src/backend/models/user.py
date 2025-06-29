"""User model definition."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    """User model representing an authenticated user."""

    id: str
    email: str
    name: str
    hashed_password: str
    is_active: bool
    created_at: datetime
    updated_at: datetime | None = None
    last_login: datetime | None = None

    def to_dict(self) -> dict[str, str | bool | None]:
        """Convert user to dictionary representation."""
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
        }
