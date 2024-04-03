"""Configuration for the backend application."""
import os

BACKEND_ENDPOINT = os.environ.get("BACKEND_ENDPOINT", "")
CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "")
DATABASE_URL = os.environ.get("DATABASE_URL", "")
ENVIRONMENT = os.environ.get("ENVIRONMENT", "")
FRONTEND_ENDPOINT = os.environ.get("FRONTEND_ENDPOINT", "")
LOGLEVEL = os.environ.get("LOGLEVEL", "")
UVICORN_RELOAD = os.environ.get("UVICORN_RELOAD", "")
SQLALCHEMY_WARN_20 = os.environ.get("SQLALCHEMY_WARN_20", "")
