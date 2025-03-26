import pandas as pd
import django
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","project.settings")
django.setup()
from app.models import Stock
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
table = pd.read_html(url)[0]
for _, row in table.iterrows():
    Stock.objects.get_or_create(symbol = row['Symbol'], name=row['Security'])
print("Stocks Saved Securely")
