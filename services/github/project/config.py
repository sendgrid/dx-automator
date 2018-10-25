import os


class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
    GITHUB_ORG = os.environ.get('GITHUB_ORG')
    EXCEPTIONS = []


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True


class TestingConfig(BaseConfig):
    """Testing configuration"""
    DEBUG = False
    TESTING = True
    EXCEPTIONS = [
        'test_exception_user'
    ]
    GITHUB_ORG = os.environ.get('GITHUB_ORG', 'pallets')


class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False
