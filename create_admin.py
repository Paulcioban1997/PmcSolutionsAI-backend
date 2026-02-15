import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pmc_core.settings')
django.setup()

User = get_user_model()
username = 'admin'
email = 'admin@pmcsolutionsai.com'
password = 'admin'

if not User.objects.filter(username=username).exists():
    print(f"Creating superuser {username}...")
    User.objects.create_superuser(username, email, password)
    print("Superuser created.")
else:
    print("Superuser already exists.")
