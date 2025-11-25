"""
Entry point for deployment platforms like Render
"""
from main import app

# Export the app instance for deployment
__all__ = ["app"]