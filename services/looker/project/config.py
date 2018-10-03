import os


class BaseConfig:
    """Base configuration"""
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "my_precious"
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    TRANSFORMATIONS = "project/db_creation/column_transformations.json"
    LOOKS = {
        # "Alias": "look_id"
        "MAIL_SENDS": {
            "look_id": "4404",
            "table": "mail_sends_by_library_language",
            "model": "SendsByLibrary"
        },
        "INVOICING": {
            "look_id": "4405",
            "table": "invoicing_by_library_language",
            "model": "InvoicingByLibrary"
        },
    }


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    DEBUG_TB_ENABLED = True


class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')


class ProductionConfig(BaseConfig):
    """Production configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
