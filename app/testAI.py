import os
import django
from pathlib import Path 
import sys
from google import genai
import re

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","project.settings")
django.setup()
from app.models import NewsHeadLines , UserCompany , ResponseModel
headline = NewsHeadLines.objects.all()
from django.contrib.auth import get_user_model
API_KEY = f"AIzaSyBdNNLAMqq95zJ5sj8bAGyDl1sApcVqrzs"
client = genai.Client(api_key = API_KEY)
import time
User = get_user_model()
users = User.objects.all()
print(f"Total Users: {users.count()}")
def extract_sentiment(text):
     match = re.search(r"\b(Positive|Negative|Neutral|Mixed)\b",text,re.IGNORECASE)
     if match:
          return match.group(1).capitalize()
     return "Unknown"


for user in users:
    print("Starting sentiment analysis script...")
    print(f"\n Checking user: {user.username}")
    user_news = UserCompany.objects.filter(user=user)
    print(f"News items found: {user_news.count()}")
    news_list = [title.companies_news for title in user_news]
    if not news_list:
         print("No news to analyze for this user!")
         continue
    prompt ="Analyze the sentiment (positive, negative, or neutral) for each of the following statements:\n\n"
    for id,statement in enumerate(news_list,1):
        prompt += f"{id}. {statement}\n"
    prompt += "\nGive the answer in the format : \n1.Positive\n2.negative\n..."
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        lines = response.text.strip().split("\n")
        for line in lines:
            cleaned = extract_sentiment(line)
            ResponseModel.objects.create(user = user,response_Text = cleaned)
            print(f"{user.username} - {cleaned}")
        time.sleep(1)
    except Exception as e:
            print(f"Error occured: {e}")



# for title in headline:
    # prompt = f"""Analyze the sentiment of the following statement. print positive,negative or neutrl according to the sentiment score.the 
    #             statement is : {title}"""

#     op = client.models.generate_content(
#         model = "gemini-2.0-flash",
#         contents = prompt
#     )
#     print(op.text)
#     time.sleep(1.5)


