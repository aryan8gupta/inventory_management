import os 
import pymongo
from .settings import *
from .settings import BASE_DIR

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['https://inventory-management-app-hnbvgqaag3g2hyde.centralindia-01.azurewebsites.net/']
DEBUG = False
SECRET_KEY = 'django-insecure-$j$mcen!5kw_vxos#q9g)cm!@zflik7k3&nohn@rg_&qx!88hl'
PUBLIC_KEY = 'Aryan971pass'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    'https://inventory-management-app-hnbvgqaag3g2hyde.centralindia-01.azurewebsites.net/' 
]


STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# CONNECTION = pymongo.MongoClient('mongodb://localhost:27017')
# DB = CONNECTION.Inventory_Management

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'inventory-management-app-database',  # Name of your database
        'CLIENT': {
            'host': 'https://inventory-management-app-server.mongo.cosmos.azure.com:443/',  # Replace with your URI
            'port': 10255,  # Default port for Azure Cosmos DB Mongo API
            'username': 'inventory-management-app-server',  # Your account name
            'password': os.environ.AZURE_COSMOS_CONNECTIONSTRING,  # Your primary key
            'authSource': 'admin',
            'authMechanism': 'SCRAM-SHA-1',
        },
    }
}

STATIC_ROOT = BASE_DIR/'staticfiles'