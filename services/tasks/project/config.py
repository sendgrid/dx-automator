# tasks/project/config.py


import os


class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'my_precious'
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    REPOS = [
        { 
            'name': 'sendgrid-nodejs', 
            'programming_language': 'nodejs'
        },
        {
            'name': 'sendgrid-csharp', 
            'programming_language': 'csharp'
        },
        {
            'name': 'sendgrid-php',
            'programming_language': 'php'
        },
        {
            'name': 'sendgrid-python',
            'programming_language': 'python'
        },
        {
            'name': 'sendgrid-java',
            'programming_language': 'java'
        },
        {
            'name': 'sendgrid-go',
            'programming_language': 'go'
        },
        {
            'name': 'sendgrid-ruby',
            'programming_language': 'ruby'
        },
        {
            'name': 'smtpapi-nodejs',
            'programming_language': 'nodejs'
        },
        {
            'name': 'smtpapi-go',
            'programming_language': 'go'
        },
        {
            'name': 'smtpapi-python',
            'programming_language': 'python'
        },
        {
            'name': 'smtpapi-php',
            'programming_language': 'php'
        },
        {
            'name': 'smtpapi-csharp',
            'programming_language': 'csharp'
        },
        {
            'name': 'smtpapi-java',
            'programming_language': 'java'
        },
        {
            'name': 'smtpapi-ruby',
            'programming_language': 'ruby'
        },
        {
            'name': 'sendgrid-oai',
            'programming_language': 'openapi'
        },
        {
            'name': 'open-source-library-data-collector',
            'programming_language': 'python'
        },
        {
            'name': 'python-http-client',
            'programming_language': 'python'
        },
        {
            'name': 'php-http-client',
            'programming_language': 'php'
        },
        {
            'name': 'csharp-http-client',
            'programming_language': 'csharp'
        },
        {
            'name': 'java-http-client',
            'programming_language': 'java'
        },
        {
            'name': 'ruby-http-client',
            'programming_language': 'ruby'
        },
        {
            'name': 'rest',
            'programming_language': 'go'
        },
        {
            'name': 'nodejs-http-client',
            'programming_language': 'nodejs'
        },
        {
            'name': 'dx-automator',
            'programming_language': 'python'
        }
    ]


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True
    DEBUG_TB_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class TestingConfig(BaseConfig):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')


class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
