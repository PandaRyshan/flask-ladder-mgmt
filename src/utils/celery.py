from celery import Celery, Task
from flask import Flask


celery = Celery()


def init_celery(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(self, *args, **kwargs)
    # celery = Celery(app.name, task_cls=FlaskTask)
    celery.conf.update(
        main=app.name,
        task_cls=FlaskTask,
    )
    celery.config_from_object(app.config["CELERY"])
    celery.set_default()
    # celery.autodiscover_tasks(["src.tasks"])
    app.extensions["celery"] = celery
    return celery
