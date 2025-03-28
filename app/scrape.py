import os
import django
import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","project.settings")
django.setup()
import requests
from bs4 import BeautifulSoup
import csv
from app.models import NewsHeadLines, Stock
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
}
# stocks = Stock.objects.all()
# for stock in stocks:
#     query = stock.name
#     print(f"Searching news for {query}")
#     URL = f"https://news.google.com/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"
#     try:
#         r = requests.get(URL, headers=headers)
#         soup = BeautifulSoup(r.content, "html5lib")
#         for link in soup.find_all("a", class_="JtKRv"):
#             headline_text = link.text.strip()  
#             if headline_text and not NewsHeadLines.objects.filter(headline = headline_text).exists():
#                 NewsHeadLines.objects.create(headline = headline_text,stock = stock)


#     except Exception as e:
#         print(f"Error: {e}")



from celery import shared_task
import requests
from bs4 import BeautifulSoup
from .models import NewsHeadLines, Stock

@shared_task
def scrape_news_headlines():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
    }
    stocks = Stock.objects.all()
    for stock in stocks:
        query = stock.name
        print(f"Searching news for {query}")
        URL = f"https://news.google.com/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"
        try:
            r = requests.get(URL, headers=headers)
            soup = BeautifulSoup(r.content, "html5lib")
            for link in soup.find_all("a", class_="JtKRv"):
                headline_text = link.text.strip()
                if headline_text and not NewsHeadLines.objects.filter(headline=headline_text).exists():
                    NewsHeadLines.objects.create(headline=headline_text, stock=stock)
        except Exception as e:
            print(f"Error: {e}")