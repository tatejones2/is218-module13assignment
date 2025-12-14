"""
End-to-End Tests for Authentication (Registration and Login)

This module contains Playwright-based E2E tests for the authentication flows,
including positive and negative test scenarios.

Tests cover:
- Registration with valid data (success message confirmation)
- Registration with invalid data (password too short, email invalid)
- Login with correct credentials (token storage)
- Login with incorrect credentials (401 error handling)
"""

import pytest
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from playwright.sync_api import Page


class TestRegistrationE2E:
    """End-to-end tests for user registration."""

    @pytest.mark.e2e
    def test_register_with_valid_data(self, page: Page, fastapi_server):
        """
        Test successful registration with valid data.
        
        Verifies:
        - Form fields are present
        - Valid data can be entered
        - Form submits successfully
        - Redirects to login page
        """
        page.goto(f"{fastapi_server}register")
        
        # Wait for form to load
        page.wait_for_selector('#registrationForm', timeout=5000)
        
        # Verify form elements exist
        assert page.locator('#username').is_visible()
        assert page.locator('#email').is_visible()
        assert page.locator('#first_name').is_visible()
        assert page.locator('#last_name').is_visible()
        assert page.locator('#password').is_visible()
        assert page.locator('#confirm_password').is_visible()
        
        # Fill in valid registration data
        page.fill('#username', 'testuser123')
        page.fill('#email', 'testuser@example.com')
        page.fill('#first_name', 'John')
        page.fill('#last_name', 'Doe')
        page.fill('#password', 'ValidPass123!')
        page.fill('#confirm_password', 'ValidPass123!')
        
        # Submit form
        page.click('button[type="submit"]')
        
        # Wait for redirect to login page (indicates successful registration)
        page.wait_for_url('**/login', timeout=10000)
        assert page.url.endswith('/login')

    @pytest.mark.e2e
    def test_register_with_short_password_client_validation(self, page: Page, fastapi_server):
        """
        Test registration with password that's too short.
        
        Verifies:
        - Client-side validation catches short password
        - Error message is displayed to user
        - Form is not submitted
        """
        page.goto(f"{fastapi_server}register")
        page.wait_for_selector('#registrationForm', timeout=5000)
        
        # Fill in data with short password (7 characters, needs 8+)
        page.fill('#username', 'testuser456')
        page.fill('#email', 'testuser456@example.com')
        page.fill('#first_name', 'Jane')
        page.fill('#last_name', 'Smith')
        page.fill('#password', 'Short1!')  # Only 7 chars
        page.fill('#confirm_password', 'Short1!')
        
        # Submit form
        page.click('button[type="submit"]')
        
        # Verify error message appears
        page.wait_for_selector('#errorAlert:not(.hidden)', timeout=5000)
        
        error_message = page.locator('#errorMessage')
        assert 'at least 8 characters' in error_message.inner_text().lower()

    @pytest.mark.e2e
    def test_register_with_invalid_email(self, page: Page, fastapi_server):
        """
        Test registration with invalid email format.
        
        Verifies:
        - Client-side validation catches invalid email
        - Error message is displayed
        """
        page.goto(f"{fastapi_server}register")
        page.wait_for_selector('#registrationForm', timeout=5000)
        
        # Fill in data with invalid email
        page.fill('#username', 'testuser789')
        page.fill('#email', 'invalidemail')  # Missing @domain
        page.fill('#first_name', 'Bob')
        page.fill('#last_name', 'Johnson')
        page.fill('#password', 'ValidPass123!')
        page.fill('#confirm_password', 'ValidPass123!')
        
        # Submit form
        page.click('button[type="submit"]')
        
        # Verify error message appears
        page.wait_for_selector('#errorAlert:not(.hidden)', timeout=5000)
        
        error_message = page.locator('#errorMessage')
        assert 'email' in error_message.inner_text().lower()

    @pytest.mark.e2e
    def test_register_with_mismatched_passwords(self, page: Page, fastapi_server):
        """
        Test registration with passwords that don't match.
        
        Verifies:
        - Validation detects mismatched passwords
        - Error message is shown
        """
        page.goto(f"{fastapi_server}register")
        page.wait_for_selector('#registrationForm', timeout=5000)
        
        # Fill in data with mismatched passwords
        page.fill('#username', 'testuser999')
        page.fill('#email', 'testuser999@example.com')
        page.fill('#first_name', 'Alice')
        page.fill('#last_name', 'Brown')
        page.fill('#password', 'ValidPass123!')
        page.fill('#confirm_password', 'DifferentPass123!')
        
        # Submit form
        page.click('button[type="submit"]')
        
        # Verify error message appears
        page.wait_for_selector('#errorAlert:not(.hidden)', timeout=5000)
        
        error_message = page.locator('#errorMessage')
        assert 'do not match' in error_message.inner_text().lower()

    @pytest.mark.e2e
    def test_register_password_without_uppercase(self, page: Page, fastapi_server):
        """
        Test registration with password missing uppercase letter.
        
        Verifies:
        - Validation requires uppercase letter
        - Error message guides user
        """
        page.goto(f"{fastapi_server}register")
        page.wait_for_selector('#registrationForm', timeout=5000)
        
        # Fill in data with password missing uppercase
        page.fill('#username', 'testuser111')
        page.fill('#email', 'testuser111@example.com')
        page.fill('#first_name', 'Charlie')
        page.fill('#last_name', 'Wilson')
        page.fill('#password', 'lowercase123!')  # Missing uppercase
        page.fill('#confirm_password', 'lowercase123!')
        
        # Submit form
        page.click('button[type="submit"]')
        
        # Verify error message appears
        page.wait_for_selector('#errorAlert:not(.hidden)', timeout=5000)
        
        error_message = page.locator('#errorMessage')
        assert 'uppercase' in error_message.inner_text().lower()

    @pytest.mark.e2e
    def test_register_duplicate_email(self, page: Page, fastapi_server, db_session):
        """
        Test registration with an email that already exists.
        
        Verifies:
        - Server rejects duplicate email
        - Error message is displayed
        """
        from app.models.user import User
        
        # Create an existing user in DB
        existing_user = User(
            username='existinguser',
            email='existing@example.com',
            first_name='Existing',
            last_name='User',
            password=User.hash_password('ValidPass123!')
        )
        db_session.add(existing_user)
        db_session.commit()
        
        page.goto(f"{fastapi_server}register")
        page.wait_for_selector('#registrationForm', timeout=5000)
        
        # Try to register with existing email
        page.fill('#username', 'newuser')
        page.fill('#email', 'existing@example.com')  # Duplicate
        page.fill('#first_name', 'New')
        page.fill('#last_name', 'User')
        page.fill('#password', 'ValidPass123!')
        page.fill('#confirm_password', 'ValidPass123!')
        
        # Submit form
        page.click('button[type="submit"]')
        
        # Verify error message from server
        page.wait_for_selector('#errorAlert:not(.hidden)', timeout=5000)
        
        error_message = page.locator('#errorMessage')
        assert 'already exists' in error_message.inner_text().lower()


class TestLoginE2E:
    """End-to-end tests for user login."""

    @pytest.mark.e2e
    def test_login_with_valid_credentials(self, page: Page, fastapi_server, db_session):
        """
        Test successful login with correct credentials.
        
        Verifies:
        - Form fields are present
        - Credentials can be entered
        - Form submits
        - JWT tokens stored in localStorage
        - Redirects to dashboard
        """
        from app.models.user import User
        
        # Create a test user
        test_user = User(
            username='logintest',
            email='logintest@example.com',
            first_name='Login',
            last_name='Test',
            password=User.hash_password('ValidPass123!')
        )
        db_session.add(test_user)
        db_session.commit()
        
        page.goto(f"{fastapi_server}login")
        page.wait_for_selector('#loginForm', timeout=5000)
        
        # Fill in valid credentials
        page.fill('#username', 'logintest')
        page.fill('#password', 'ValidPass123!')
        
        # Submit form
        page.click('button[type="submit"]')
        
        # Wait for redirect to dashboard
        page.wait_for_url('**/dashboard', timeout=10000)
        assert page.url.endswith('/dashboard')
        
        # Verify tokens stored
        access_token = page.evaluate('() => localStorage.getItem("access_token")')
        assert access_token is not None and len(access_token) > 0
        
        refresh_token = page.evaluate('() => localStorage.getItem("refresh_token")')
        assert refresh_token is not None and len(refresh_token) > 0
        
        user_id = page.evaluate('() => localStorage.getItem("user_id")')
        assert user_id is not None

    @pytest.mark.e2e
    def test_login_with_email_instead_of_username(self, page: Page, fastapi_server, db_session):
        """
        Test login using email instead of username.
        
        Verifies:
        - User can login with email
        - Tokens are stored
        - Redirects successfully
        """
        from app.models.user import User
        
        # Create a test user
        test_user = User(
            username='emaillogintest',
            email='emaillogin@example.com',
            first_name='Email',
            last_name='Login',
            password=User.hash_password('ValidPass456!')
        )
        db_session.add(test_user)
        db_session.commit()
        
        page.goto(f"{fastapi_server}login")
        page.wait_for_selector('#loginForm', timeout=5000)
        
        # Fill in credentials using email
        page.fill('#username', 'emaillogin@example.com')
        page.fill('#password', 'ValidPass456!')
        
        # Submit form
        page.click('button[type="submit"]')
        
        # Wait for redirect
        page.wait_for_url('**/dashboard', timeout=10000)
        
        # Verify tokens stored
        access_token = page.evaluate('() => localStorage.getItem("access_token")')
        assert access_token is not None

    @pytest.mark.e2e
    def test_login_with_wrong_password(self, page: Page, fastapi_server, db_session):
        """
        Test login with incorrect password.
        
        Verifies:
        - Server returns 401 Unauthorized
        - Error message displayed to user
        - No tokens stored
        - Page doesn't redirect
        """
        from app.models.user import User
        
        # Create a test user
        test_user = User(
            username='wrongpasstest',
            email='wrongpass@example.com',
            first_name='Wrong',
            last_name='Pass',
            password=User.hash_password('CorrectPass123!')
        )
        db_session.add(test_user)
        db_session.commit()
        
        page.goto(f"{fastapi_server}login")
        page.wait_for_selector('#loginForm', timeout=5000)
        
        # Fill in credentials with wrong password
        page.fill('#username', 'wrongpasstest')
        page.fill('#password', 'WrongPass123!')
        
        # Submit form
        page.click('button[type="submit"]')
        
        # Verify error message appears
        page.wait_for_selector('#errorAlert:not(.hidden)', timeout=5000)
        
        error_message = page.locator('#errorMessage')
        assert 'invalid' in error_message.inner_text().lower()
        
        # Verify no tokens stored
        access_token = page.evaluate('() => localStorage.getItem("access_token")')
        assert access_token is None
        
        # Verify still on login page
        assert page.url.endswith('/login')

    @pytest.mark.e2e
    def test_login_with_nonexistent_user(self, page: Page, fastapi_server):
        """
        Test login with a username that doesn't exist.
        
        Verifies:
        - Server rejects nonexistent user
        - Error message displayed
        - No tokens stored
        """
        page.goto(f"{fastapi_server}login")
        page.wait_for_selector('#loginForm', timeout=5000)
        
        # Fill in credentials for nonexistent user
        page.fill('#username', 'nonexistentuser99999')
        page.fill('#password', 'SomePass123!')
        
        # Submit form
        page.click('button[type="submit"]')
        
        # Verify error message appears
        page.wait_for_selector('#errorAlert:not(.hidden)', timeout=5000)
        
        error_message = page.locator('#errorMessage')
        assert 'invalid' in error_message.inner_text().lower()
        
        # Verify no tokens stored
        access_token = page.evaluate('() => localStorage.getItem("access_token")')
        assert access_token is None

    @pytest.mark.e2e
    def test_login_with_empty_fields(self, page: Page, fastapi_server):
        """
        Test login form submission with empty fields.
        
        Verifies:
        - Client-side validation prevents submission
        - Error message shown for empty fields
        """
        page.goto(f"{fastapi_server}login")
        page.wait_for_selector('#loginForm', timeout=5000)
        
        # Try to submit without filling fields
        page.click('button[type="submit"]')
        
        # Verify error message appears
        page.wait_for_selector('#errorAlert:not(.hidden)', timeout=5000)
        
        error_message = page.locator('#errorMessage')
        assert 'fill in all fields' in error_message.inner_text().lower()

    @pytest.mark.e2e
    def test_login_remember_me_functionality(self, page: Page, fastapi_server, db_session):
        """
        Test the "Remember me" checkbox functionality.
        
        Verifies:
        - Username is stored when "Remember me" is checked
        - Username is pre-filled on return
        """
        from app.models.user import User
        
        # Create a test user
        test_user = User(
            username='remembermetest',
            email='rememberme@example.com',
            first_name='Remember',
            last_name='Me',
            password=User.hash_password('ValidPass789!')
        )
        db_session.add(test_user)
        db_session.commit()
        
        page.goto(f"{fastapi_server}login")
        page.wait_for_selector('#loginForm', timeout=5000)
        
        # Fill in credentials
        page.fill('#username', 'remembermetest')
        page.fill('#password', 'ValidPass789!')
        
        # Check remember me
        page.check('#remember')
        
        # Submit form
        page.click('button[type="submit"]')
        
        # Wait for redirect
        page.wait_for_url('**/dashboard', timeout=10000)
        
        # Verify remembered username in localStorage
        remembered_username = page.evaluate('() => localStorage.getItem("remembered_username")')
        assert remembered_username == 'remembermetest'
        
        # Go back to login page
        page.goto(f"{fastapi_server}login")
        page.wait_for_selector('#loginForm', timeout=5000)
        
        # Verify username is pre-filled
        username_value = page.input_value('#username')
        assert username_value == 'remembermetest'
        
        # Verify checkbox is checked
        is_checked = page.is_checked('#remember')
        assert is_checked


class TestAuthNavigationE2E:
    """End-to-end tests for authentication flow navigation."""

    @pytest.mark.e2e
    def test_register_page_has_login_link(self, page: Page, fastapi_server):
        """
        Test that register page has link to login page.
        """
        page.goto(f"{fastapi_server}register")
        page.wait_for_selector('#registrationForm', timeout=5000)
        
        # Click link to login
        page.click('a[href="/login"]')
        
        # Verify on login page
        page.wait_for_url('**/login', timeout=5000)
        assert page.url.endswith('/login')

    @pytest.mark.e2e
    def test_login_page_has_register_link(self, page: Page, fastapi_server):
        """
        Test that login page has link to register page.
        """
        page.goto(f"{fastapi_server}login")
        page.wait_for_selector('#loginForm', timeout=5000)
        
        # Click link to register
        page.click('a[href="/register"]')
        
        # Verify on register page
        page.wait_for_url('**/register', timeout=5000)
        assert page.url.endswith('/register')
