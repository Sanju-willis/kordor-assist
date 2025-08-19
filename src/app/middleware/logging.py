# src\app\middleware\logging.py
import time
from fastapi import Request
from app.lib import logger


async def logging_middleware(request: Request, call_next):
    start = time.perf_counter()
    req_line = f"{request.method} {request.url.path} HTTP/{request.scope.get('http_version', '1.1')}"

    try:
        response = await call_next(request)
    except Exception as e:
        # Let the error handler middleware deal with this later
        raise e
    else:
        elapsed = int((time.perf_counter() - start) * 1000)
        msg = f'"{req_line}" {response.status_code} {elapsed}ms'
        (logger.error if response.status_code >= 400 else logger.info)(msg)
        return response
