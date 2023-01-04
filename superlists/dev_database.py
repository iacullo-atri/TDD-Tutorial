import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
with open(os.path.join(BASE_DIR, 'secrets.json')) as secrets_file:
    secrets = json.load(secrets_file)

def get_secret(key):
    return secrets[key]

def config_database(name):
    return {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': name,
        'USER': 'nicholasiacullo',
        'PASSWORD': get_secret('database_password'),
    }
