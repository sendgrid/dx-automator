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
    LOCALHOST = 'http://{}'.format(os.environ.get('DX_IP'))
    ERROR_DB_WRITE_FAILURE = 'There was an error writing to the DB, this commit has been rolled back. Please check your DB logs.'
    REPOS = [
        {
            'name': 'twilio-node',
            'programming_language': 'nodejs',
            'org': 'twilio'
        },
        {
            'name': 'twilio-csharp',
            'programming_language': 'csharp',
            'org': 'twilio'
        },
        {
            'name': 'twilio-php',
            'programming_language': 'php',
            'org': 'twilio'
        },
        {
            'name': 'twilio-python',
            'programming_language': 'python',
            'org': 'twilio'
        },
        {
            'name': 'twilio-java',
            'programming_language': 'java',
            'org': 'twilio'
        },
        {
            'name': 'twilio-ruby',
            'programming_language': 'ruby',
            'org': 'twilio'
        },
        {
            'name': 'twilio-cli',
            'programming_language': 'nodejs',
            'org': 'twilio'
        },
        { 
            'name': 'twilio-cli-core', 
            'programming_language': 'nodejs',
            'org': 'twilio'
        },
        { 
            'name': 'sendgrid-nodejs', 
            'programming_language': 'nodejs',
            'org': 'sendgrid'
        },
        {
            'name': 'sendgrid-csharp', 
            'programming_language': 'csharp',
            'org': 'sendgrid'
        },
        {
            'name': 'sendgrid-php',
            'programming_language': 'php',
            'org': 'sendgrid'
        },
        {
            'name': 'sendgrid-python',
            'programming_language': 'python',
            'org': 'sendgrid'
        },
        {
            'name': 'sendgrid-java',
            'programming_language': 'java',
            'org': 'sendgrid'
        },
        {
            'name': 'sendgrid-go',
            'programming_language': 'go',
            'org': 'sendgrid'
        },
        {
            'name': 'sendgrid-ruby',
            'programming_language': 'ruby',
            'org': 'sendgrid'
        },
        {
            'name': 'smtpapi-nodejs',
            'programming_language': 'nodejs',
            'org': 'sendgrid'
        },
        {
            'name': 'smtpapi-go',
            'programming_language': 'go',
            'org': 'sendgrid'
        },
        {
            'name': 'smtpapi-python',
            'programming_language': 'python',
            'org': 'sendgrid'
        },
        {
            'name': 'smtpapi-php',
            'programming_language': 'php',
            'org': 'sendgrid'
        },
        {
            'name': 'smtpapi-csharp',
            'programming_language': 'csharp',
            'org': 'sendgrid'
        },
        {
            'name': 'smtpapi-java',
            'programming_language': 'java',
            'org': 'sendgrid'
        },
        {
            'name': 'smtpapi-ruby',
            'programming_language': 'ruby',
            'org': 'sendgrid'
        },
        {
            'name': 'sendgrid-oai',
            'programming_language': 'openapi',
            'org': 'sendgrid'
        },
        {
            'name': 'open-source-library-data-collector',
            'programming_language': 'python',
            'org': 'sendgrid'
        },
        {
            'name': 'python-http-client',
            'programming_language': 'python',
            'org': 'sendgrid'
        },
        {
            'name': 'php-http-client',
            'programming_language': 'php',
            'org': 'sendgrid'
        },
        {
            'name': 'csharp-http-client',
            'programming_language': 'csharp',
            'org': 'sendgrid'
        },
        {
            'name': 'java-http-client',
            'programming_language': 'java',
            'org': 'sendgrid'
        },
        {
            'name': 'ruby-http-client',
            'programming_language': 'ruby',
            'org': 'sendgrid'
        },
        {
            'name': 'rest',
            'programming_language': 'go',
            'org': 'sendgrid'
        },
        {
            'name': 'nodejs-http-client',
            'programming_language': 'nodejs',
            'org': 'sendgrid'
        },
        {
            'name': 'dx-automator',
            'programming_language': 'python',
            'org': 'sendgrid'
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
