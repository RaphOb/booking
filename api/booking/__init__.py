import importlib
import logging

from .database import Base, engine

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

import sys
import os
from os import chdir, listdir, getcwd
from os.path import splitext, isdir

logger = logging.getLogger(__name__)


def create_app():
    """Create application"""

    logger.info("Create APP")
    app = FastAPI()

    logger.info("Add middleware")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    logger.info("Load all route")
    load_router(app)
    logger.info("Create db")
    Base.metadata.create_all(bind=engine)
    return app


def load_router(app):
    """This function will look in all current folders
    of the current folder (booking here), .py files that contains routers and
    append it to the fastApi app."""

    previous_directory = getcwd()
    app_directory = os.path.dirname(os.path.realpath(__file__))
    root = (
        app_directory.split("\\")[-1]
        if sys.platform.startswith("win")
        else app_directory.split("/")[-1]
    )
    chdir(app_directory)
    folders = [f for f in listdir() if isdir(f)]
    chdir(previous_directory)
    for folder in folders:
        path = root + "/" + folder
        files = [splitext(f)[0] for f in listdir(path) if f.lower().endswith(".py")]
        path = path.replace("/", ".")
        for file in files:
            module = importlib.import_module("." + file, path)
            for item in dir(module):
                router = getattr(module, item)
                if isinstance(router, APIRouter):
                    app.include_router(router)
