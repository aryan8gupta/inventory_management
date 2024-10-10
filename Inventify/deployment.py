import os 
import pymongo
from .settings import *
from .settings import BASE_DIR

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['https://inventory-management-app-hnbvgqaag3g2hyde.centralindia-01.azurewebsites.net/']
DEBUG = False
SECRET_KEY = 'django-insecure-$j$mcen!5kw_vxos#q9g)cm!@zflik7k3&nohn@rg_&qx!88hl'
PUBLIC_KEY = 'Aryan971pass'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Inventify'
]

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

from pymongo import MongoClient

connection_string = "mongodb://inventory-management-app-server.mongo.cosmos.azure.com:10255/"

client = MongoClient(connection_string)

DB = client['inventory-management-app-database']



# DB = {
#     'default': {
#         'ENGINE': 'djongo',
#         'NAME': 'inventory-management-app-database',  # Name of your database
#         'CLIENT': {
#             'host': 'mongodb://inventory-management-app-server.mongo.cosmos.azure.com:10255/',  # Replace with your URI
#             'port': 10255,  # Default port for Azure Cosmos DB Mongo API
#             'username': 'inventory-management-app-server',  # Your account name
#             'password': os.getenv('Azure_Cosmos_Pswd'),  # Your primary key
#             'authSource': 'admin',
#             'authMechanism': 'SCRAM-SHA-256',
#             'tls': True,
#         },
#     }
# }

STATIC_ROOT = BASE_DIR/'staticfiles'