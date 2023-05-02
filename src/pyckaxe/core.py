"""
    Package "pyckaxe"

    This module provides package's api
"""

import logging
import asyncio
from pathlib import Path

import aiohttp
import aiofiles
from bs4 import BeautifulSoup

from pyckaxe.base import BaseInspector

from pyckaxe.utils import get_json
from pyckaxe.utils import get_content

logger = logging.getLogger('standard')
report = logging.getLogger('report')


class AsyncInspector(BaseInspector):
    async_method = [
        'content',
        'save html',
    ]
    def __init__(self, url: str,
                 session: aiohttp.ClientSession,
                 **kwargs):
        super().__init__(url, **kwargs)
        self.session = session
        self.page = None
        self._soup = None

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

    def load(self, *args, method='content', **kwargs):
        if method == self.async_method[0]:
            return asyncio.create_task(self._content(*args, **kwargs))
        elif method == self.async_method[1]:
            return asyncio.create_task(self._save_html(*args, **kwargs))
        else:
            raise ValueError(f"'method' must be one of {self.async_method}")


class Inspector(BaseInspector):
    def __init__(self, url: str=None, **kwargs):
        super().__init__(url)
        self.session = requests_html.HTMLSession(**kwargs)
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
