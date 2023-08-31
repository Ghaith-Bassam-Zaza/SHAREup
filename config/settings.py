import os


class Config:
    """ basic configuration"""
    DEBUG = False
    PORT = os.environ.get('PORT') or 5000
    FLASK_ENV = os.environ.get('FLASK_ENV')
    FLASK_APP = os.environ.get('FLASK_APP')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_TOKEN_LOCATION = os.environ.get('JWT_TOKEN_LOCATION')


class development(Config):
    """development configuration"""
    DEBUG = True


class production(Config):
    """production configuration"""
    PORT = os.environ.get('PORT') or 8080
