import json
import time
import urllib.parse
from typing import Dict, Optional, Text

import requests
from pydantic import BaseModel

from cnside.cli.documents import CNSIDERequestDocument
from cnside.objects.encoders import CNSIDEJsonEncoder

__all__ = ["APIClient", "APIClientConfig"]


class APIClientConfig(BaseModel):
    base_url: Text
    headers: Optional[Dict] = {}
    proxies: Optional[Dict] = {}
    max_attempts: Optional[int] = 500


class APIClient:
    def __init__(self, config: APIClientConfig):
        self.config = config
        self.session = self.open()

    def open(self) -> requests.Session:
        s = requests.Session()
        s.headers.update(self.config.headers)
        s.proxies.update(self.config.proxies)
        return s

    def request_packages_from_cnside_system(self, request_document: CNSIDERequestDocument) -> bool:
        analyze_url = urllib.parse.urljoin(self.config.base_url, "analyze")

        rv = False

        response = self.session.post(url=analyze_url, json=json.loads(json.dumps(request_document, cls=CNSIDEJsonEncoder)))

        workflow_id: Text = response.json()['workflow_id']
        attempts = 0
        while attempts < self.config.max_attempts:
            time.sleep(10)
            response = self.session.get(url=f"{analyze_url}/{workflow_id}")
            if response.status_code == 404:
                pass
            else:
                data = response.json()
                if data['STATUS'] == "COMPLETED":
                    rv = data['ACCEPT']
                    return rv
                attempts += 1

        return rv
