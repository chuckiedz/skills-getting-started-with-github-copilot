"""
Pytest configuration and fixtures for the FastAPI application tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """
    Fixture that provides a TestClient instance for testing the FastAPI app.
    Each test gets a fresh instance of the test client.
    """
    return TestClient(app)
