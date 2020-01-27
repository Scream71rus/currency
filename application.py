
import momoko
import psycopg2.extras
import redis
import tornado.ioloop
import tornado.web
import tornado.httpclient
from tornado.options import options

from models.base_model import BaseModel


class Application(tornado.web.Application):

    @property
    def cache(self):
        return self._cache

    @property
    def httpclient(self):
        return self._httpclient

    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)

        dsn = "dbname={} user={} password={} host={} port={}".format(
            options.db_name,
            options.db_user,
            options.db_password,
            options.db_host,
            options.db_port)

        BaseModel.db = momoko.Pool(
            dsn=dsn,
            size=options.size_db_connection_pool,
            ioloop=tornado.ioloop.IOLoop.current(),
            cursor_factory=psycopg2.extras.RealDictCursor)

        BaseModel.db.connect()

        self._redis_pool = redis.ConnectionPool(
            host=options.cache_host,
            port=options.cache_port,
            db=options.cache_db)

        self._cache = redis.StrictRedis(connection_pool=self._redis_pool)

        self._httpclient = tornado.httpclient.AsyncHTTPClient()

