from flask import Flask
from flask_caching import Cache


cache = Cache()


def init(app: Flask):
    cache.init_app(app)
