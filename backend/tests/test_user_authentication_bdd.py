"""
Behavior-Driven Testing (BDD) Example for Python - 2025 Best Practices

This module demonstrates BDD approach focusing on user behavior
rather than implementation details.
"""

from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, Mock

import pytest

pytestmark = pytest.mark.asyncio

from backend.exceptions import (
    InvalidCredentialsError,
    TokenExpiredError,
    ValidationError,
)
from backend.models.user import User
from backend.services.auth_service import AuthService


class TestUserAuthenticationBehavior:
    """Test user authentication behavior using BDD approach."""

    @pytest.fixture
    def auth_service(self) -> AuthService:
        """Create auth service with mocked dependencies."""
        mock_db = Mock()
        mock_token_service = Mock()
        mock_email_service = Mock()

        return AuthService(
            database=mock_db,
            token_service=mock_token_service,
            email_service=mock_email_service,
        )

    @pytest.fixture
    def valid_user(self) -> User:
        """Create a valid user fixture."""
        return User(
            id="user123",
            email="john.doe@example.com",
            name="John Doe",
            hashed_password="$2b$12$hashed_password_here",
            is_active=True,
            created_at=datetime.now(UTC),
        )

    class TestWhenUserAttemptsToLoginWithValidCredentials:
        """Behavior: User logs in with valid credentials."""

        async def test_should_successfully_authenticate_and_return_tokens(
            self,
            auth_service: AuthService,
            valid_user: User,
        ) -> None:
            """
            Given: A registered user with valid credentials
            When: The user attempts to login with correct email and password
            Then: The system should return access and refresh tokens
            """
            # Given
            auth_service.database.get_user_by_email = AsyncMock(return_value=valid_user)
            auth_service.database.update_user = AsyncMock()
            auth_service.token_service.verify_password = Mock(return_value=True)
            auth_service.token_service.create_access_token = Mock(
                return_value="access_token_123",
            )
            auth_service.token_service.create_refresh_token = Mock(
                return_value="refresh_token_123",
            )

            # When
            result = await auth_service.login(
                email="john.doe@example.com",
                password="ValidPassword123!",
            )

            # Then
            assert result.success is True
            assert result.access_token == "access_token_123"
            assert result.refresh_token == "refresh_token_123"
            assert result.user.email == "john.doe@example.com"

            # Verify interactions
            auth_service.database.get_user_by_email.assert_called_once_with(
                "john.doe@example.com",
            )
            auth_service.token_service.verify_password.assert_called_once()

        async def test_should_update_last_login_timestamp(
            self,
            auth_service: AuthService,
            valid_user: User,
        ) -> None:
            """
            Given: A user logging in successfully
            When: Authentication is completed
            Then: The system should update the user's last login timestamp
            """
            # Given
            auth_service.database.get_user_by_email = AsyncMock(return_value=valid_user)
            auth_service.database.update_user = AsyncMock()
            auth_service.token_service.verify_password = Mock(return_value=True)

            # When
            await auth_service.login(
                email="john.doe@example.com",
                password="ValidPassword123!",
            )

            # Then
            auth_service.database.update_user.assert_called_once()
            update_call_args = auth_service.database.update_user.call_args[0]
            assert update_call_args[0] == "user123"  # user_id
            assert "last_login" in update_call_args[1]  # update_data
            assert isinstance(update_call_args[1]["last_login"], datetime)

    class TestWhenUserAttemptsToLoginWithInvalidCredentials:
        """Behavior: User attempts login with invalid credentials."""

        async def test_should_reject_login_with_wrong_password(
            self,
            auth_service: AuthService,
            valid_user: User,
        ) -> None:
            """
            Given: A registered user
            When: The user attempts to login with incorrect password
            Then: The system should reject the login attempt
            """
            # Given
            auth_service.database.get_user_by_email = AsyncMock(return_value=valid_user)
            auth_service.token_service.verify_password = Mock(return_value=False)

            # When & Then
            with pytest.raises(InvalidCredentialsError) as exc_info:
                await auth_service.login(
                    email="john.doe@example.com",
                    password="WrongPassword123!",
                )

            assert "Invalid email or password" in str(exc_info.value)

        async def test_should_reject_login_for_non_existent_user(
            self,
            auth_service: AuthService,
        ) -> None:
            """
            Given: An email that is not registered
            When: Someone attempts to login with this email
            Then: The system should reject the login without revealing user existence
            """
            # Given
            auth_service.database.get_user_by_email = AsyncMock(return_value=None)

            # When & Then
            with pytest.raises(InvalidCredentialsError) as exc_info:
                await auth_service.login(
                    email="nonexistent@example.com",
                    password="AnyPassword123!",
                )

            # Should not reveal that user doesn't exist
            assert "Invalid email or password" in str(exc_info.value)
            assert "not found" not in str(exc_info.value).lower()

    class TestWhenUserAccountIsDeactivated:
        """Behavior: Deactivated user attempts to login."""

        async def test_should_prevent_deactivated_user_from_logging_in(
            self,
            auth_service: AuthService,
            valid_user: User,
        ) -> None:
            """
            Given: A user account that has been deactivated
            When: The user attempts to login with valid credentials
            Then: The system should reject the login with appropriate message
            """
            # Given
            valid_user.is_active = False
            auth_service.database.get_user_by_email = AsyncMock(return_value=valid_user)
            auth_service.token_service.verify_password = Mock(return_value=True)

            # When & Then
            with pytest.raises(InvalidCredentialsError) as exc_info:
                await auth_service.login(
                    email="john.doe@example.com",
                    password="ValidPassword123!",
                )

            assert "account has been deactivated" in str(exc_info.value).lower()

    class TestWhenUserRequestsPasswordReset:
        """Behavior: User requests password reset."""

        async def test_should_send_reset_email_for_existing_user(
            self,
            auth_service: AuthService,
            valid_user: User,
        ) -> None:
            """
            Given: A registered user who forgot their password
            When: The user requests a password reset
            Then: The system should send a reset email with token
            """
            # Given
            auth_service.database.get_user_by_email = AsyncMock(return_value=valid_user)
            auth_service.token_service.create_reset_token = Mock(
                return_value="reset_token_123",
            )
            auth_service.email_service.send_reset_email = AsyncMock()

            # When
            result = await auth_service.request_password_reset(
                email="john.doe@example.com",
            )

            # Then
            assert result.success is True
            assert result.message == "Password reset email sent"

            auth_service.email_service.send_reset_email.assert_called_once_with(
                email="john.doe@example.com",
                name="John Doe",
                reset_token="reset_token_123",
            )

        async def test_should_not_reveal_user_existence_for_unknown_email(
            self,
            auth_service: AuthService,
        ) -> None:
            """
            Given: An email that is not registered
            When: Someone requests password reset for this email
            Then: The system should return success without revealing user doesn't exist
            """
            # Given
            auth_service.database.get_user_by_email = AsyncMock(return_value=None)

            # When
            result = await auth_service.request_password_reset(
                email="nonexistent@example.com",
            )

            # Then
            assert result.success is True
            assert result.message == "Password reset email sent"
            # Email service should not be called
            auth_service.email_service.send_reset_email.assert_not_called()

    class TestWhenUserValidatesAuthToken:
        """Behavior: System validates authentication tokens."""

        async def test_should_accept_valid_unexpired_token(
            self,
            auth_service: AuthService,
            valid_user: User,
        ) -> None:
            """
            Given: A valid authentication token
            When: The system validates the token
            Then: The validation should succeed and return user info
            """
            # Given
            token_payload = {
                "sub": "user123",
                "email": "john.doe@example.com",
                "exp": datetime.now(UTC) + timedelta(hours=1),
            }
            auth_service.token_service.decode_token = Mock(return_value=token_payload)
            auth_service.database.get_user_by_id = AsyncMock(return_value=valid_user)

            # When
            result = await auth_service.validate_token("valid_token_123")

            # Then
            assert result.is_valid is True
            assert result.user.id == "user123"
            assert result.user.email == "john.doe@example.com"

        async def test_should_reject_expired_token(
            self,
            auth_service: AuthService,
        ) -> None:
            """
            Given: An expired authentication token
            When: The system validates the token
            Then: The validation should fail with appropriate error
            """
            # Given
            auth_service.token_service.decode_token = Mock(
                side_effect=TokenExpiredError("Token has expired"),
            )

            # When & Then
            with pytest.raises(TokenExpiredError) as exc_info:
                await auth_service.validate_token("expired_token_123")

            assert "Token has expired" in str(exc_info.value)

    @pytest.mark.parametrize(
        ("email", "expected_error"),
        [
            ("", "Email is required"),
            ("invalid-email", "Invalid email format"),
            ("@example.com", "Invalid email format"),
            ("user@", "Invalid email format"),
            ("user name@example.com", "Invalid email format"),
        ],
    )
    async def test_should_validate_email_format(
        self,
        auth_service: AuthService,
        email: str,
        expected_error: str,
    ) -> None:
        """
        Given: Various invalid email formats
        When: User attempts to login
        Then: System should reject with validation error
        """
        # When & Then
        with pytest.raises(ValidationError) as exc_info:
            await auth_service.login(email=email, password="ValidPassword123!")

        assert expected_error in str(exc_info.value)

    @pytest.mark.parametrize(
        ("password", "expected_error"),
        [
            ("", "Password is required"),
            ("short", "Password must be at least 8 characters"),
            ("12345678", "Password must contain letters"),
            ("password", "Password must contain numbers"),
            ("PASSWORD123", "Password must contain uppercase and lowercase letters"),
        ],
    )
    async def test_should_validate_password_requirements(
        self,
        auth_service: AuthService,
        password: str,
        expected_error: str,
    ) -> None:
        """
        Given: Various invalid password formats
        When: User attempts to set password
        Then: System should reject with validation error
        """
        # When & Then
        with pytest.raises(ValidationError) as exc_info:
            await auth_service.validate_password_strength(password)

        assert expected_error in str(exc_info.value)
