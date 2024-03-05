import logging

from logging.handlers import RotatingFileHandler
from flask import has_request_context, request


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
            record.method = request.method
        else:
            record.url = None
            record.remote_addr = None
            record.method = None
        return super().format(record)


class LoggerConfigurator:
    
    @staticmethod
    def setup_app_logger(app):
        if not app.debug:
            log_level = logging.INFO
            log_path = app.config['FLASK_LOG_PATH']

            file_handler = RotatingFileHandler(log_path, maxBytes=10240, backupCount=10)
            formatter = RequestFormatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d] [%(remote_addr)s] [%(method)s] [%(url)s]'
                # '%(asctime)s %(levelname)s: %(message)s [in %(module)s:%(lineno)d]'
            )
            file_handler.setFormatter(formatter)
            file_handler.setLevel(log_level)

            app.logger.addHandler(file_handler)
            app.logger.setLevel(log_level)

            logging.getLogger('werkzeug').setLevel(log_level)
            logging.getLogger('werkzeug').addHandler(file_handler)
            logging.getLogger('passlib').setLevel(logging.ERROR)
