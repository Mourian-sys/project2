"""
Application routes
"""

from app.routes.main import main_bp
from app.routes.api import api_bp
from app.routes.webhook import webhook_bp

__all__ = ['main_bp', 'api_bp', 'webhook_bp']
