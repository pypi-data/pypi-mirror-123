from http import HTTPStatus

from requests import HTTPError


class FramesMetadataExists(Exception):
    pass


class ColumnGroupExists(Exception):
    pass


class CatalogRequestError(Exception):
    def __init__(self, e: HTTPError):
        msg = f"{HTTPStatus(e.response.status_code)} for {e.request.url}. Msg: {e.response.text}"
        super().__init__(msg)
