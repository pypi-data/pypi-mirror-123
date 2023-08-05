import json
import os
from pathlib import Path
from typing import Text, Dict

from cnside.storage import StorageHandlerConfig

__all__ = ["StorageHandler"]


class FileHandler:
    def __init__(self, file_path: Text):
        self.file_path = file_path

    def load(self):
        with open(self.file_path, "r+") as fp:
            data = json.load(fp)
        return data

    def save(self, data: Dict):
        if not os.path.exists(self.file_path):
            Path(self.file_path).parent.mkdir(parents=True, exist_ok=True)

        with open(self.file_path, "w+") as fp:
            json.dump(data, fp)


class StorageHandler:
    def __init__(self, config: StorageHandlerConfig):
        self._config = config

    @property
    def token(self):
        return FileHandler(self._config.token_file_path)
