import requests
from fastapi import Depends
from .config import settings

def fetch_news():
    api_key = settings.NEWS_API_KEY
    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def filter_news(articles, keyword):
    return [article for article in articles if keyword.lower() in article['title'].lower()]

def send_email(subject, body, to_email):
    smtp_server = settings.SMTP_SERVER
    smtp_port = settings.SMTP_PORT
    smtp_user = settings.SMTP_USER
    smtp_password = settings.SMTP_PASSWORD
    
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    import smtplib
    
    from_email = smtp_user
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(from_email, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())
