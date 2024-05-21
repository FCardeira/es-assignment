import asyncio
import httpx
from json import loads, dumps
from logging import getLogger
from time import time

from .exceptions import Error
from .settings import settings

log = getLogger(__name__)


HTTP_POOL = httpx.AsyncClient(
    verify=False, limits=httpx.Limits(max_keepalive_connections=25, max_connections=100)
)
DEFAULT_TIMEOUT = 30.0
BACKOFF_ON_ERROR = 0.5
MAX_RETRIES = 1


class HTTPCall:
    stat_key = None
    timeout = DEFAULT_TIMEOUT

    @classmethod
    def parse_error(cls, url, status_code, content, context=None):
        if isinstance(content, bytes):
            content = content.decode("utf-8")
            try:
                content = loads(content)
            except Exception:
                pass

            return content

        log.warning(f"Unhandled error from {url} -> {status_code}")
        return Error(code=status_code, detail=content)

    @classmethod
    async def send(
        cls,
        method,
        url,
        timeout=None,
        max_retries=MAX_RETRIES,
        context=None,
        with_retry=True,
        return_content=False,
        **kwargs,
    ):
        headers = kwargs.get("headers") or {}
        if not any(i.lower() == "accept-encoding" for i in headers.keys()):
            # httpx auto decodes brotli and gzip
            headers["Accept-Encoding"] = "br, gzip"

        retry = 0
        timeout = cls.timeout if timeout is None else timeout
        while True:
            response = None

            try:
                if settings.DEBUG:
                    log.debug(f"Send request to {url} -> {kwargs}")

                start = time()
                response = await method(url, timeout=timeout, **kwargs)
                response_time = (time() - start) * 1000
                
                if settings.DEBUG:
                    log.debug(f"""Request info
                        url: {url} 
                        response time: {response_time:.2f}ms
                        status_code: {response.status_code}
                        response: {response.content}"""
                    )

                if response.status_code != 200:
                    raise cls.parse_error(
                        url,
                        response.status_code,
                        response.content,
                        context=context,
                    )
                elif return_content:
                    return response.content
                else:
                    return loads(response.content)

            except Exception as error:
                if isinstance(error, httpx.ConnectError):
                    raise

                if not with_retry or retry >= max_retries:
                    raise

                is_timeout = isinstance(error, httpx.ReadTimeout)
                log_message = "Error calling"
                if is_timeout:
                    log_message += " (timeout)"
                log_message += f" retry:{retry}:{url}"
                if response:
                    log_message += f" response:{response.status_code}:{response.content}"

                if is_timeout:
                    log.critical(log_message)
                else:
                    log.exception(log_message)

                await asyncio.sleep(BACKOFF_ON_ERROR)
                retry += 1

    @classmethod
    def get(cls, *args, **kwargs):
        return cls.send(HTTP_POOL.get, *args, **kwargs)

    @classmethod
    def post_core(cls, *args, **kwargs):
        return cls.send(HTTP_POOL.post, *args, **kwargs)

    @classmethod
    def post(cls, *args, json, **kwargs):
        kwargs["data"] = dumps(json)
        return cls.post_core(*args, **kwargs)

    @classmethod
    def delete(cls, *args, **kwargs):
        return cls.send(HTTP_POOL.delete, *args, **kwargs)
