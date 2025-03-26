import os
import django
from pathlib import Path
import sys
import ftfy
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","project.settings")
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.all()
from app.models import InvestModel , NewsHeadLines
from app.models import UserCompany
for usr in user:
    user_company = InvestModel.objects.filter(user=usr).values_list('company',flat=True)
    headlines = NewsHeadLines.objects.filter(stock__in = user_company).order_by('-created_at')[:100]
    com = []
    for headline in headlines:
        com.append(ftfy.fix_text(headline.headline))

    for news in com:
        UserCompany.objects.create(user=usr,companies_news = news)
# import html
# com = set(com)
# for text in com:
#     print(text)

