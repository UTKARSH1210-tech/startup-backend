from app.tasks import celery_app

celery_app.conf.update(task_routes = {
    'app.tasks.fetch_and_send_alerts': {'queue': 'news_alerts'},
})

if __name__ == "__main__":
    celery_app.worker_main()
