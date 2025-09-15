import os
from celery import Celery

# ست کردن تنظیمات جنگو
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

# خواندن تنظیمات celery از settings.py (با پیشوند CELERY_)
app.config_from_object("django.conf:settings", namespace="CELERY")

# پیدا کردن tasks.py در اپ‌ها
app.autodiscover_tasks()