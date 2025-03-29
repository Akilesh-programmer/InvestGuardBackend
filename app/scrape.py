import os
from datetime import datetime
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
from app.models import NewsHeadLines, Stock, ScrapingStatus
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
# from .models import NewsHeadLines, Stock

def get_last_scraped_time():
    status = ScrapingStatus.objects.first()
    return status.last_scraped_at if status else None

def save_scrape_time():
    status, created = ScrapingStatus.objects.get_or_create(id=1)
    status.last_scraped_at = datetime.now()
    status.save()

@shared_task
def scrape_news_headlines():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
    }
    last_scraped_time = get_last_scraped_time()
    
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

                # Extract article time
                time_tag = link.find_next("time")
                if time_tag and "datetime" in time_tag.attrs:
                    article_time = datetime.fromisoformat(time_tag["datetime"])

                    # Skip if the article is older than last scraped time
                    if last_scraped_time and article_time <= last_scraped_time:
                        continue

                if headline_text and not NewsHeadLines.objects.filter(headline=headline_text).exists():
                    NewsHeadLines.objects.create(headline=headline_text, stock=stock)

        except Exception as e:
            print(f"Error: {e}")
            continue

    save_scrape_time()



# your function remains unchanged

if __name__ == "__main__":
    print("Starting the scraper...")
    scrape_news_headlines()
