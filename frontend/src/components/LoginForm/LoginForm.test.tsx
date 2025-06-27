import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import { LoginForm } from './LoginForm';

// Mock submit handler
const mockOnSubmit = vi.fn();

describe('LoginForm - User Authentication Behavior', () => {
  let user: ReturnType<typeof userEvent.setup>;

  beforeEach(() => {
    user = userEvent.setup();
    mockOnSubmit.mockClear();
  });

  describe('when user attempts to login with valid credentials', () => {
    it('should show success message on successful submission', async () => {
      // Given: A user on the login page
      mockOnSubmit.mockResolvedValue(undefined);
      render(<LoginForm onSubmit={mockOnSubmit} />);

      // When: The user enters valid credentials
      await user.type(screen.getByLabelText(/email/i), 'john@example.com');
      await user.type(screen.getByLabelText(/password/i), 'ValidPassword123!');
      await user.click(screen.getByRole('button', { name: /sign in/i }));

      // Then: The success message should be displayed
      expect(await screen.findByText('Welcome back!')).toBeInTheDocument();

      // And: The submit handler should be called with correct arguments
      expect(mockOnSubmit).toHaveBeenCalledWith('john@example.com', 'ValidPassword123!');
    });
  });

  describe('when user submits empty form', () => {
    it('should show validation errors for both fields', async () => {
      // Given: A user on the login page
      render(<LoginForm onSubmit={mockOnSubmit} />);

      // When: The user submits without filling fields
      await user.click(screen.getByRole('button', { name: /sign in/i }));

      // Then: Validation errors should be displayed
      expect(await screen.findByText(/email is required/i)).toBeInTheDocument();
      expect(await screen.findByText(/password is required/i)).toBeInTheDocument();

      // And: The submit handler should not be called
      expect(mockOnSubmit).not.toHaveBeenCalled();
    });
  });

  describe('when user attempts to login with invalid credentials', () => {
    it('should display an error message when submission fails', async () => {
      // Given: Mock that will throw an error
      mockOnSubmit.mockRejectedValue(new Error('Invalid credentials'));
      render(<LoginForm onSubmit={mockOnSubmit} />);

      // When: The user enters credentials
      await user.type(screen.getByLabelText(/email/i), 'wrong@example.com');
      await user.type(screen.getByLabelText(/password/i), 'WrongPassword');
      await user.click(screen.getByRole('button', { name: /sign in/i }));

      // Then: An error message should be displayed
      expect(await screen.findByText(/invalid email or password/i)).toBeInTheDocument();

      // And: The success message should not be shown
      expect(screen.queryByText('Welcome back!')).not.toBeInTheDocument();
    });
  });

  describe('when user enters an invalid email format', () => {
    it('should show email validation error', async () => {
      // Given: A user on the login page
      render(<LoginForm onSubmit={mockOnSubmit} />);

      // When: The user enters an invalid email and tries to submit
      const emailInput = screen.getByLabelText(/email/i);
      const passwordInput = screen.getByLabelText(/password/i);
      const submitButton = screen.getByRole('button', { name: /sign in/i });

      await user.type(emailInput, 'notanemail');
      await user.type(passwordInput, 'ValidPassword123!');
      await user.click(submitButton);

      // Then: An email validation error should be displayed
      // Wait for the error message to appear
      await waitFor(() => {
        // The input field should be marked as invalid
        expect(emailInput).toHaveAttribute('aria-invalid', 'true');

        // And: The error message should be visible
        const errorMessage = screen.getByText('Invalid email format');
        expect(errorMessage).toBeInTheDocument();
      });

      // And: The submit handler should not be called
      expect(mockOnSubmit).not.toHaveBeenCalled();
    });
  });

  describe('when user enters a short password', () => {
    it('should show password validation error', async () => {
      // Given: A user on the login page
      render(<LoginForm onSubmit={mockOnSubmit} />);

      // When: The user enters a password that is too short
      await user.type(screen.getByLabelText(/email/i), 'user@example.com');
      await user.type(screen.getByLabelText(/password/i), 'short');
      await user.click(screen.getByRole('button', { name: /sign in/i }));

      // Then: A password validation error should be displayed
      expect(
        await screen.findByText(/password must be at least 8 characters/i),
      ).toBeInTheDocument();

      // And: The submit handler should not be called
      expect(mockOnSubmit).not.toHaveBeenCalled();
    });
  });

  describe('when the login request is in progress', () => {
    it('should disable the form and show loading state', async () => {
      // Given: A slow authentication service
      mockOnSubmit.mockImplementation(() => new Promise((resolve) => setTimeout(resolve, 1000)));

      render(<LoginForm onSubmit={mockOnSubmit} />);

      // When: The user submits valid credentials
      await user.type(screen.getByLabelText(/email/i), 'john@example.com');
      await user.type(screen.getByLabelText(/password/i), 'ValidPassword123!');
      await user.click(screen.getByRole('button', { name: /sign in/i }));

      // Then: The form should be disabled
      expect(screen.getByLabelText(/email/i)).toBeDisabled();
      expect(screen.getByLabelText(/password/i)).toBeDisabled();

      // And: The button should show loading state
      expect(screen.getByRole('button', { name: /signing in/i })).toBeDisabled();
    });
  });

  describe('accessibility features', () => {
    it('should be fully keyboard navigable', async () => {
      // Given: A user relying on keyboard navigation
      render(<LoginForm onSubmit={mockOnSubmit} />);

      // When: The user navigates using Tab key
      await user.tab(); // Focus on email
      expect(screen.getByLabelText(/email/i)).toHaveFocus();

      await user.tab(); // Focus on password
      expect(screen.getByLabelText(/password/i)).toHaveFocus();

      await user.tab(); // Focus on submit button
      expect(screen.getByRole('button', { name: /sign in/i })).toHaveFocus();
    });

    it('should have proper ARIA attributes for form validation', () => {
      // Given: A form with validation
      render(<LoginForm onSubmit={mockOnSubmit} />);

      // When: Checking ARIA attributes
      const emailInput = screen.getByLabelText(/email/i);
      const passwordInput = screen.getByLabelText(/password/i);

      // Then: Inputs should have proper ARIA attributes
      expect(emailInput).toHaveAttribute('aria-label', 'Email');
      expect(passwordInput).toHaveAttribute('aria-label', 'Password');
    });

    it('should announce errors to screen readers', async () => {
      // Given: A user with a screen reader
      render(<LoginForm onSubmit={mockOnSubmit} />);

      // When: Validation errors occur
      await user.click(screen.getByRole('button', { name: /sign in/i }));

      // Then: Error messages should have role="alert"
      const errorMessages = await screen.findAllByRole('alert');
      expect(errorMessages).toHaveLength(2); // Email and password errors
    });
  });

  describe('form state management', () => {
    it('should clear error messages when user corrects input', async () => {
      // Given: A form with validation errors
      render(<LoginForm onSubmit={mockOnSubmit} />);
      await user.click(screen.getByRole('button', { name: /sign in/i }));

      // Verify errors are shown
      expect(await screen.findByText(/email is required/i)).toBeInTheDocument();

      // When: User enters valid email
      await user.type(screen.getByLabelText(/email/i), 'user@example.com');
      await user.type(screen.getByLabelText(/password/i), 'ValidPass123');
      await user.click(screen.getByRole('button', { name: /sign in/i }));

      // Then: Email error should be cleared
      expect(screen.queryByText(/email is required/i)).not.toBeInTheDocument();
    });

    it('should maintain form values after failed submission', async () => {
      // Given: A form that will fail submission
      mockOnSubmit.mockRejectedValue(new Error('Server error'));
      render(<LoginForm onSubmit={mockOnSubmit} />);

      // When: User submits form and it fails
      const email = 'user@example.com';
      const password = 'ValidPassword123!';
      await user.type(screen.getByLabelText(/email/i), email);
      await user.type(screen.getByLabelText(/password/i), password);
      await user.click(screen.getByRole('button', { name: /sign in/i }));

      // Then: Form values should be maintained
      await waitFor(() => {
        expect(screen.getByLabelText(/email/i)).toHaveValue(email);
        expect(screen.getByLabelText(/password/i)).toHaveValue(password);
      });
    });
  });
});
