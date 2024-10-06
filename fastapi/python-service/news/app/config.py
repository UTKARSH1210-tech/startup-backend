import os

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://username:password@localhost/news_alert")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY", "your_newsapi_key")
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.example.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
    SMTP_USER = os.getenv("SMTP_USER", "your_email@example.com")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "your_email_password")
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

settings = Settings()
