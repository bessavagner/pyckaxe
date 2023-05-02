"""
    This modules provide a class to manage the CLI
    The package's entry point is pyckaxe.

    To understand more how to implement this module
    check:
     - 
"""
import logging

import click
import aiohttp
import requests

from pyckaxe import HEADER
from app import WebInspect

logger_client = logging.getLogger('client')


class CLI:
    def __init__(self,):
        self.app = None

    def start(self, arg=None):
        click.echo(HEADER)
        self.app = WebInspect(arg)
        self.app.run()

    def finish(self,):
        self.app.close()

@click.command()
@click.option('--arg',
              default=None,
              required=False,
              help='Argument to WebInspect')
def start_program(arg: str=None):
    program = CLI()
    if arg is None:
        session = aiohttp.ClientSession()
    else:
        session = requests.Session()
    program.start(session)
    program.finish()
