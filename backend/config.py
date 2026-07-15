import os
from datetime import timedelta

# Configuration for development
SECRET_KEY = os.environ.get('SECRET_KEY') or 'placament-portal-secret-key'
SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
CACHE_TYPE = 'RedisCache'
CACHE_REDIS_URL = 'redis://localhost:6379/0'

# JWT Configuration
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'placament-portal-secret-key'
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

# Debug mode
DEBUG = True