import pytest
from flask import Flask
from app import create_app

@pytest.fixture
def app():
    return create_app()

@pytest.fixture
def client(app: Flask):
    return app.test_client()