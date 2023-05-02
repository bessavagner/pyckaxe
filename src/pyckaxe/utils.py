"""
    Package "pyckaxe"

    This module provides helpful objects
"""
import aiohttp
from pyckaxe import USER_AGENT


async def get_json(url: str, session: aiohttp.ClientSession, headers: dict=None):
    session.headers['User-Agent'] = USER_AGENT
    async with session.get(url, headers=headers) as response:
        data = await response.json()
        return data

async def get_content(url: str, session: aiohttp.ClientSession, headers: dict=None):
    session.headers['User-Agent'] = USER_AGENT
    async with session.get(url, headers=headers) as response:
        content = await response.content.read()
        return content
