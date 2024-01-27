from redis import Redis
from flask import Flask


def init(app: Flask) -> Redis:
    return Redis.from_url(app.config['REDIS_URI'])
