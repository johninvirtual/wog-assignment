import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

from django.contrib.auth import get_user_model
import json

User = get_user_model()

with open("data.json", 'r') as f:
    data = json.loads(f.read())

print(data)

