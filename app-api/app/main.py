#!/usr/bin/env python3

import base64
import os, sys
import hashlib
import urllib
import requests
import re
import pprint

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every
from app.routers import base, user, auth
from app.database import database, engine

app = FastAPI()
app.header = {}


# PROMETHEUS (part 5)
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Gauge

# END PROMETHEUS (part 5)


# Fluent (part 8)
from app.lib.app_logging import setup_logging

setup_logging("api")
import logging

logger = logging.getLogger("api")
logger.info("HELLO LOGGING!")
# End fluent (part 8)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://app.k8s.castlerock.ai",
    "https://www.app.k8s.castlerock.ai",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(base.router)
app.include_router(user.router)
app.include_router(auth.router)

# PREMETHEUS (part 5)
@app.on_event("startup")
def init_instrumentator():
    """Setup prometheus instrumentation for the API"""
    Instrumentator().instrument(app).expose(app)


@app.on_event("startup")
@repeat_every(seconds=30, wait_first=True)
def periodic():
    count = engine.execute("select count(id) from user").scalar()
    Gauge("total_users", "Total Users").set(int(count))


# END PROMETHEUS (part 5)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
