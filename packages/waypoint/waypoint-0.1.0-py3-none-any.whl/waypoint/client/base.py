import functools
from typing import Callable, Union, TypeVar, Type, List
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseURLSession(requests.Session):
    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url

    def request(self, method: str, url: Union[str, bytes], *args, **kwargs):
        return super().request(method, urljoin(self.base_url, url), *args, **kwargs)


class APIClient:
    retry_strategy: Retry = Retry(
        total=10,
        backoff_factor=1,
    )

    def __init__(self, base_url: str):
        adapter = HTTPAdapter(max_retries=self.retry_strategy)
        self.session = BaseURLSession(base_url)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)


def http_method(model: Type[T] = None):
    def decorator_http_method(
        func: Callable[..., requests.Response]
    ) -> Callable[..., Union[T, List[T], object]]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Union[T, List[T], object]:
            resp = func(*args, **kwargs)
            resp.raise_for_status()
            data = resp.json()
            if model:
                if isinstance(data, list):
                    return [model(**i) for i in data]
                return model(**data)
            return data

        return wrapper

    return decorator_http_method
