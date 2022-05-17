import os
from dotenv import load_dotenv

load_dotenv()

broker_url = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
result_backend = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
timezone = os.getenv("TZ", "Europe/Paris")
