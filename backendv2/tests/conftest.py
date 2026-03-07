"""Test fixtures for pytest-django."""

import pytest
from rest_framework.test import APIClient


@pytest.fixture
def client():
    """Return a DRF APIClient for making test requests."""
    return APIClient()


@pytest.fixture
def sample_user(client):
    """Register a test user and return the response data."""
    resp = client.post(
        "/api/auth/register",
        {"email": "test@example.com", "password": "test123", "full_name": "Test User"},
        format="json",
    )
    return resp.json()


@pytest.fixture
def auth_token(sample_user):
    """Return the access token from sample_user registration."""
    return sample_user["access_token"]
