from apps.celery import celery
from apps.celery.celery_util import init_celery
from apps import create_app
from apps.config import config_dict

app = create_app(config_dict['Debug'])
init_celery(app, celery)