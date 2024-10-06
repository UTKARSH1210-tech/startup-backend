from celery import Celery
from fastapi import FastAPI
from sqlalchemy.orm import Session
from .models import User, SessionLocal
from .utils import fetch_news, filter_news, send_email
from .config import settings

app = FastAPI()

celery_app = Celery(
    'worker',
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

@celery_app.task
def fetch_and_send_alerts():
    db = SessionLocal()
    news_data = fetch_news()
    articles = news_data.get('articles', [])
    users = db.query(User).all()
    
    for user in users:
        filtered_news = filter_news(articles, user.keyword)
        if filtered_news:
            subject = f"News Alert: {user.keyword}"
            body = "\n\n".join([article['title'] + "\n" + article['url'] for article in filtered_news])
            send_email(subject, body, user.email)

    db.close()
