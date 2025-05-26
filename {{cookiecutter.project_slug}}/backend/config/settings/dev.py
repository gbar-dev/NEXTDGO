from config.settings.base import *


ALLOWED_HOSTS = ['frontend',"backend"]


BASE_URL="http://127.0.0.1:8000"
FRONTEND_URL="http://127.0.0.1:3000"

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000", 
    "http://127.0.0.1:3000", 
    "http://frontend:3000", 
    "http://backend:8000",
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'Accept',
    'Accept-Language',
    'Content-Language',
    'Content-Type',
    'Authorization',
    "authorization",
    'X-CSRFToken',
    "Cookie",
]

DEBUG = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = False
SESSION_COOKIE_NAME = 'sessionid' 
SESSION_COOKIE_AGE = 86400  
SESSION_EXPIRE_AT_BROWSER_CLOSE = False 
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_DOMAIN = None

CSRF_COOKIE_NAME = 'csrftoken'
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_SAMESITE = 'Lax'

HTTPONLY=False
SECURE=False 
