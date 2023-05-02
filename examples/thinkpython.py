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
from tqdm import tqdm

from pyckaxe import CONFIG_LOG
from pyckaxe import AsyncInspector

dictConfig(CONFIG_LOG)

logger = logging.getLogger('client')
report = logging.getLogger('report')

THINK_PYTHON_BASE_URL = 'https://greenteapress.com/thinkpython2/html/'

async def scrape_all_sections():
    async with aiohttp.ClientSession() as session:

        thinkpy = AsyncInspector(THINK_PYTHON_BASE_URL, session)
        task = thinkpy.load()
        await asyncio.gather(task)
        links = thinkpy.absolute_links(contains='thinkpython2')

        thinkpy_sections = [AsyncInspector(link, session) for link in links]
        tasks_save = []
        
        for section in thinkpy_sections:
            tasks_save.append(section.load(method='save html', directory='think_python'))

        with tqdm(total=len(tasks_save)) as pbar:
            for task_save in asyncio.as_completed(tasks_save):
                await task_save
                pbar.update(1)

if __name__ == '__main__':
    asyncio.run(scrape_all_sections())

