"""
    Package pyckaxe

    This can be an sample app using the package
    or the app itself to feed the __main__ and gui
    modules.
"""

import asyncio
import logging
from logging.config import dictConfig

import aiohttp
import requests
from tqdm import tqdm

from pyckaxe import CONFIG_LOG
from pyckaxe import AsyncInspector

dictConfig(CONFIG_LOG)

logger = logging.getLogger('client')
report = logging.getLogger('report')

class WebInspect:
    def __init__(self, session: aiohttp.ClientSession|requests.Session):
        self.session = session

    def run(self, ):
        return self.session

    def close(self,):
        self.session.close()
        del self.session
