import requests
import httpx
from typing import AnyStr, Optional, Union

from .uilog import logger
from .uitry import retry


class sync_uiclient:
    def __init__(
        self,
        proxy: Optional[dict] = None,
        timeout: Optional[Union[tuple, int]] = None,
        request_headers: Optional[dict] = None,
        other_headers: Optional[str] = None,
        request_json: Optional[AnyStr] = None,
        request_params: Optional[dict] = None,
        request_data: Optional[dict] = None,
    ) -> None:
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh-HK;q=0.9,zh;q=0.8,en;q=0.7",
            "cache-control": "max-age=0",
            "sec-ch-ua": """Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99""",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "cross-site",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        }
        if request_headers:
            self.headers = request_headers
        if other_headers:
            for x, y in other_headers.items():
                self.headers[x] = y
        self.proxy = proxy
        self.timeout = timeout
        self.params = request_params
        self.data = request_data
        self.json = request_json

    def __enter__(self) -> None:
        pass

    def __exit__(self) -> None:
        pass

    @retry(logger=logger)
    def uiget(self, url: str):
        logger.debug(
            f"开始连接至:{url},方法:GET,代理:{self.proxy},参数:{self.params},数据:{self.data}"
        )
        res = requests.get(
            url,
            proxies=self.proxy,
            timeout=self.timeout,
            json=self.json,
            headers=self.headers,
            params=self.params,
            data=self.data,
        )
        logger.debug(f"成功连接,状态码:{res.status_code}")
        return res

    @retry(logger=logger)
    def uipost(self, url: str):
        logger.debug(
            f"开始连接至:{url},方法:POST,代理:{self.proxy},参数:{self.params},数据:{self.data}"
        )
        res = requests.post(
            url,
            proxies=self.proxy,
            timeout=self.timeout,
            headers=self.headers,
            json=self.json,
            params=self.params,
            data=self.data,
        )
        logger.debug(f"成功连接,状态码:{res.status_code}")
        return res


class async_uiclient:
    def __enter__(
        self,
        proxy: Optional[dict] = None,
        timeout: Optional[Union[tuple, int]] = None,
        request_headers: Optional[dict] = None,
        other_headers: Optional[dict] = None,
        request_json: Optional[AnyStr] = None,
        request_params: Optional[dict] = None,
        request_data: Optional[dict] = None,
    ) -> None:
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh-HK;q=0.9,zh;q=0.8,en;q=0.7",
            "cache-control": "max-age=0",
            "sec-ch-ua": """Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99""",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "cross-site",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        }
        if request_headers:
            self.headers = request_headers
        if other_headers:
            for x, y in other_headers.items():
                self.headers[x] = y
        self.proxy = proxy
        self.timeout = timeout
        self.json = request_json
        self.params = request_params
        self.data = request_data

    def __exit__(self) -> None:
        pass

    @retry(logger=logger)
    async def uiget(self, url: str):
        logger.debug(
            f"开始连接至:{url},方法:GET,代理:{self.proxy},参数:{self.params},数据:{self.data}"
        )
        with httpx.AsyncClient(
            proxies=self.proxy,
            timeout=self.timeout,
            headers=self.headers,
            params=self.params,
        ) as client:
            res = await client.get(
                url,
            )
        logger.debug(f"成功连接,状态码:{res.status_code}")
        return res

    @retry(logger=logger)
    async def uipost(self, url: str):
        logger.debug(
            f"开始连接至:{url},方法:POST,代理:{self.proxy},参数:{self.params},数据:{self.data}"
        )
        with httpx.AsyncClient(
            proxies=self.proxy,
            timeout=self.timeout,
            headers=self.headers,
            params=self.params,
        ) as client:
            res = await client.post(url, data=self.data, json=self.json)
        logger.debug(f"成功连接,状态码:{res.status_code}")
        return res
