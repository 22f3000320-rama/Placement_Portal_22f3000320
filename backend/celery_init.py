from celery import Celery
from celery.schedules import crontab

celery_app = Celery('tasks', broker='redis://localhost:6379/1', backend='redis://localhost:6379/2', include=['tasks'])

celery_app.conf.timezone = 'Asia/Kolkata'

celery_app.conf.beat_schedule = {
    'monthly-admin-report':{
        'task': 'tasks.send_monthly_report',
        'schedule': crontab(hour=22, minute=52, day_of_month = 14),
    },
    'daily-reminder':{
        'task': 'tasks.send_daily_reminder',
        'schedule': crontab(hour=22, minute=52),
    },
    'monthly-company-report':{
        'task':'tasks.company_monthly_report',
        'schedule': crontab(hour=22, minute=52, day_of_month=14),
    }
}