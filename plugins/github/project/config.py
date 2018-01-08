import os

class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
    GITHUB_ORG = os.environ['GITHUB_ORG']
    EXCEPTIONS = [
        'test_exception_user'
    ]

class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True

class TestingConfig(BaseConfig):
    """Testing configuration"""
    DEBUG = False
    TESTING = True

class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False
