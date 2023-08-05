from urllib.parse import urljoin

import requests
from requests.utils import requote_uri


PUBLIC_API_BASE = "/public_api/v1"


class CatalogSession(requests.Session):
    def __init__(self, base_url: str, user: str, password: str):
        super().__init__()
        self.url = urljoin(base_url, f"/api/catalog/")
        jwt_token = self._login(base_url, user, password)
        self.headers.update({"Authorization": f"Bearer {jwt_token}"})

    def _login(self, base_url, user, password):
        url = urljoin(base_url, f"{PUBLIC_API_BASE}/auth/login")
        data = {"email": user, "password": password}
        r = requests.post(url, json=data)
        r.raise_for_status()
        return r.json()["access_token"]

    def _full_url(self, rel_url):
        rel_url = rel_url.lstrip("/")
        return requote_uri(urljoin(self.url, rel_url))

    def get(self, rel_url, **kwargs):
        url = self._full_url(rel_url)
        r = super().get(url, **kwargs)
        r.raise_for_status()
        return r

    def post(self, rel_url, **kwargs):
        url = self._full_url(rel_url)
        r = super().post(url, **kwargs)
        r.raise_for_status()
        return r

    def delete(self, rel_url, **kwargs):
        url = self._full_url(rel_url)
        r = super().delete(url, **kwargs)
        r.raise_for_status()
        return r
