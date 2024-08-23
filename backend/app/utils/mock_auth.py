from fastapi import HTTPException
import uuid
from typing import Tuple

class MockAuth:
    def __init__(self):
        # Simulate some stored "user information" for testing purposes
        self.fake_user_data = {
            "email": f"testuser{str(uuid.uuid4())}@example.com",
            "name": f"Test User {str(uuid.uuid4())}",
        }

    def get_authorization_url(self) -> Tuple[str, str]:
        """
        Simulates getting an authorization URL. In a real provider, this would
        be a URL to redirect the user to for authentication.

        Returns:
            :return authorization_url: A mock URL.
            :return state: A unique state parameter to help prevent CSRF attacks.
        """
        authorization_url = "http://example.com/auth?provider=test"
        state = str(uuid.uuid4())  # Generate a unique state token
        return authorization_url, state

    def exchange_authorization_code(self, code: str) -> dict:
        """
        Simulates exchanging an authorization code for user information.

        Parameters:
            :param code: A mock authorization code.

        Returns:
            :return: A dictionary with user information.
        """
        if code != "test-code":  # For testing, we expect a specific "test-code"
            raise ValueError("Invalid authorization code")

        # Return the fake user data as if it was fetched from the provider
        return self.fake_user_data

