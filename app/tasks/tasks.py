from app.tasks.celery_ import celery


@celery.task
def make_report():
    pass
