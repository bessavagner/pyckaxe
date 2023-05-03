"""
    Package "pyckaxe"

    This module provides package's base logic, factories and abstractions
"""
import logging
from pathlib import Path
from urllib.parse import urljoin
from logging.config import dictConfig

from pyckaxe import CONFIG_LOG

dictConfig(CONFIG_LOG)

logger = logging.getLogger("standard")


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
        try:
            return self._soup.find_all(*args, **kwargs)

        except AttributeError:
            if __class__.__name__ == "BaseInspector":
                logger.warning(
                    "Using an instance of %s. Returning None", __class__.__name__
                )

                return None

    def anchors(
        self,
    ):
        return self.find_all("a")

    def absolute_links(self, contains: str = None):
        links = self.anchors()
        absolute_links_ = []

        try:
            for link in links:
                relative_link = link.attrs["href"]

                if contains is not None:
                    if contains not in relative_link:
                        continue

                url = urljoin(self.url, relative_link)
                absolute_links_.append(url)

            return absolute_links_

        except TypeError as err:
            if err == "'NoneType' object is not iterable":
                if links is None:
                    if __class__.__name__ == "BaseInspector":
                        logger.warning(
                            "Using an instance of %s. Returning empty list",
                            __class__.__name__,
                        )

                        return []


class BaseFileManager:
    def __init__(self, folder_path: str):
        self.folder_path = Path(folder_path)
        self.file_state = {}
        try:
            self.folder_path.mkdir(parents=True, exist_ok=True)
        except OSError as err:
            raise ValueError(f"Invalid folder path: {folder_path}") from err

    def _file_path(self, file_name):
        return self.folder_path / file_name

    def _read_file(self, file_name, encoding="utf-8", **kwargs):
        with open(self._file_path(file_name), "r", encoding=encoding, **kwargs) as f:
            return f.read()

    def _write_file(self, file_name, file_contents):
        with open(self._file_path(file_name), "w") as f:
            f.write(file_contents)

    def save_file(self, file_name, file_contents):
        self._write_file(file_name, file_contents)
        self.file_state.setdefault(file_name, []).append("saved")

    def load_file(self, file_name):
        try:
            file_contents = self._read_file(file_name)
            self.file_state.setdefault(file_name, []).append("loaded")
            return file_contents
        except FileNotFoundError:
            logger.error("File not found: %s. Returning None", file_name)
            return None

    def get_file_state(self, file_name):
        return self.file_state.get(file_name, ["unknown"])[-1]

    def list_files(self):
        return [f.name for f in self.folder_path.glob("*") if f.is_file()]

    def delete_file(self, file_name):
        file_path = self._file_path(file_name)
        if file_path.exists():
            file_path.unlink()
            self.file_state.setdefault(file_name, []).append("deleted")
        else:
            raise ValueError(f"File not found: {file_name}")

    def __str__(self):
        files = self.list_files()
        file_info = []
        for file in files:
            file_state = self.get_file_state(file)
            file_info.append(f"{file}: {file_state}")
        return "\n".join(file_info)


class BaseHandleData:
    def __init__(
        self,
    ):
        pass
