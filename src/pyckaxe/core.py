"""
    Package "pyckaxe"

    This module provides package's api
"""

import logging
import asyncio
from pathlib import Path

import requests
import aiohttp
import aiofiles
from bs4 import BeautifulSoup

from pyckaxe.base import BaseInspector

from pyckaxe.utils import get_json
from pyckaxe.utils import get_content

logger = logging.getLogger('standard')
report = logging.getLogger('report')


class AsyncInspector(BaseInspector):
    """
    An asynchronous web page inspector.

    Attributes:
    -----------
    async_method : List[str]
        A list of async methods available for the AsyncInspector object.

    Methods:
    --------
    __init__(self, url: str, session: aiohttp.ClientSession, **kwargs):
        Initializes a new AsyncInspector object.

    _content(self, *args, **kwargs):
        Asynchronously retrieves and returns the content of the web page.

    _json(self, *args, **kwargs):
        Asynchronously retrieves and returns the JSON data from requests.

    _save_html(self, *args, directory: str=None, **kwargs):
        Asynchronously saves the HTML of the web page to a file.

    load(self, *args, method='content', **kwargs):
        Asynchronously loads the content or HTML of the web page based on the specified method.
    """
    SUPPORTED_METHODS = {
        'content': '_content',
        'save html': '_save_html',
        'json': '_json'
    }
    def __init__(self, url: str,
                 session: aiohttp.ClientSession,
                 **kwargs):
        super().__init__(url, **kwargs)
        self.session = session

    async def _content(self, *args, **kwargs):
        content = await get_content(self.url, self.session, *args, **kwargs)
        self.page = content
        self._soup = BeautifulSoup(self.page, 'html.parser')
        return content

    async def _json(self, *args, **kwargs):
        data = await get_json(self.url, self.session, *args, **kwargs)
        return data

    async def _save_html(self, *args, directory: str=None, **kwargs):

        filename = self.url.split('/')[-1] + '.html'

        if self.page is None:
            await self._content(*args, **kwargs)

        if directory is not None:
            directory = Path(directory)
            if not directory.is_dir():
                directory.mkdir()
            filename = directory / filename

        async with aiofiles.open(filename, 'w', encoding='utf-8') as afile:
            await afile.write(self._soup.prettify())

    async def load(self, *args, method='content', **kwargs):
        if method not in self.SUPPORTED_METHODS:
            raise ValueError(f"'method' must be one of {list(self.SUPPORTED_METHODS.keys())}")

        method_name = self.SUPPORTED_METHODS[method]
        coroutine = getattr(self, method_name)
        return asyncio.create_task(coroutine(*args, **kwargs))


class Inspector(BaseInspector):
    def __init__(self, url: str=None, **kwargs):
        super().__init__(url)
        self.session = requests.Session(**kwargs)
        self.page = None
        if isinstance(url, str):
            self.url = url
        else:
            raise ValueError(f"Url must be string, {type(url)} was given")

    def get(self, render=False, **kwargs):
        response = self.session.get(self.url, **kwargs)
        if render:
            response.html.render()
        self.page = response.html
        return response
