"""
Application settings and configuration
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration class"""
    
    # Basic App Config
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    APP_NAME = 'Project2'
    DEBUG = False
    TESTING = False
    
    # Session Config
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Database (optional)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # API Configuration
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = False
    
    # Rate Limiting
    RATELIMIT_ENABLED = True
    RATELIMIT_DEFAULT = '100/hour'
    
    # GitHub Webhook
    GITHUB_WEBHOOK_SECRET = os.getenv('GITHUB_WEBHOOK_SECRET', '')
    
    # Jenkins Configuration
    JENKINS_URL = os.getenv('JENKINS_URL', 'http://localhost:8080')
    JENKINS_USERNAME = os.getenv('JENKINS_USERNAME', '')
    JENKINS_TOKEN = os.getenv('JENKINS_TOKEN', '')


class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    TESTING = False
    LOG_LEVEL = 'DEBUG'
    SESSION_COOKIE_SECURE = False
    SQLALCHEMY_ECHO = True
    RATELIMIT_ENABLED = False


class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    TESTING = False
    LOG_LEVEL = 'WARNING'
    SESSION_COOKIE_SECURE = True
    SQLALCHEMY_ECHO = False
    RATELIMIT_ENABLED = True


class TestingConfig(Config):
    """Testing environment configuration"""
    DEBUG = True
    TESTING = True
    LOG_LEVEL = 'DEBUG'
    WTF_CSRF_ENABLED = False
    RATELIMIT_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


def get_config(env=None):
    """
    Get configuration object based on environment
    
    Args:
        env (str): Environment name (development, production, testing)
        
    Returns:
        Config: Configuration object
    """
    if env is None:
        env = os.getenv('FLASK_ENV', 'development').lower()
    
    config_map = {
        'development': DevelopmentConfig,
        'dev': DevelopmentConfig,
        'production': ProductionConfig,
        'prod': ProductionConfig,
        'testing': TestingConfig,
        'test': TestingConfig,
    }
    
    return config_map.get(env, DevelopmentConfig)
