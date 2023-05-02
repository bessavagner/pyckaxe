"""
    Package "pyckaxe"

    This module provides package's base logic, factories and abstractions
"""
from urllib.parse import urljoin

class BaseInspector:
    def __init__(self, url: str):
        self.session = None
        self.page = None
        self._soup = None
        if isinstance(url, str):
            self.url = url
        else:
            raise ValueError(f"Url must be string, {type(url)} was given")

    def find_all(self, *args, **kwargs):
        return self._soup.find_all(*args, **kwargs)

    def anchors(self, ):
        return self.find_all('a')

    def absolute_links(self, contains: str=None):
        links = self.anchors()
        absolute_links_ = []
        for link in links:
            relative_link = link.attrs['href']
            if contains is not None:
                if contains not in relative_link:
                    continue
            url = urljoin(self.url, relative_link)
            absolute_links_.append(url)
        return absolute_links_


class BaseHandleData:
    def __init__(self,):
        pass
