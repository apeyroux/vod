import os

from flask import Flask
from celery import Celery
from elasticsearch import Elasticsearch

app = Flask(__name__)

app.config['ELASTICSEARCH_URL'] = os.environ.get('ELASTICSEARCH_URL')
app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
                    if app.config['ELASTICSEARCH_URL'] else None

app.config.update(
    CELERY_BROKER_URL='redis://127.0.0.1:6379',
    CELERY_RESULT_BACKEND='redis://127.0.0.1:6379'
)

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(app)

from . import views
