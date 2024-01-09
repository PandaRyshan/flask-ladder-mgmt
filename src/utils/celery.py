from celery import Celery, Task
from flask import Flask


celery = Celery()


def init_celery(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.conf.update(
        main=app.name,
        task_cls=FlaskTask,
    )
    celery.config_from_object(app.config["CELERY"])
    celery.set_default()
    app.extensions["celery"] = celery
    celery.Task = FlaskTask
    return celery
