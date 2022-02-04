import logging

from starlette.config import Config

config = Config(".env")

ENV = config("ENV", default="local")
DEBUG = config("DEBUG", default=True)
LOG_LEVEL = config("LOG_LEVEL", default=logging.DEBUG)
logging.basicConfig(
    format="%(asctime)s,%(msecs)d %(levelname)-8s [%(pathname)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d:%H:%M:%S",
    filename="all.log",
    level=LOG_LEVEL,
)

SQL_DB_URI = config("SQL_DB_URI", default="sqlite:///./sql_app.db")
