from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

import json

User = get_user_model()

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        
        with open("data.json", 'r') as f:
            data = json.loads(f.read())

        print(data)