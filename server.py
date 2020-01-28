
import sys
import os

sys.path.append(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), '.'))

import asyncio
import logging
import tornado.ioloop
import tornado.platform.asyncio
import tornado.log
from tornado.options import define, options, parse_config_file

from application import Application
import urls


define("port", type=int)

define("db_name", type=str)
define("db_user", type=str)
define("db_password", type=str)
define("db_host", type=str)
define("db_port", type=str)
define("size_db_connection_pool", type=int)

define("cache_host", type=str)
define("cache_port", type=int)
define("cache_db", type=int)

define("debug", type=str)

parse_config_file("application.conf")
tornado.options.parse_command_line()


if __name__ == '__main__':
    tornado.log.enable_pretty_logging()

    if options.debug == "yes":
        tornado.log.app_log.setLevel(logging.DEBUG)
    elif options.debug == "no":
        tornado.log.app_log.setLevel(logging.INFO)

    tornado.platform.asyncio.AsyncIOMainLoop().install()

    application = Application(
        urls.urls,
        cookie_secret='11111111',
        debug=(True))

    application.listen(options.port)

    asyncio.get_event_loop().run_forever()
