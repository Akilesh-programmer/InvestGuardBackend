import os
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

# Load .env file from root of the project
load_dotenv('/app/.env')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

application = get_wsgi_application()
