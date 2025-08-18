# src\app\middleware\error_handler.py
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.lib.logger import logger
import time

async def error_handling_middleware(request: Request, call_next):
    start = time.perf_counter()
    request_line = f'{request.method} {request.url.path} HTTP/{request.scope.get("http_version","1.1")}'
    try:
        response = await call_next(request)
        elapsed_ms = int((time.perf_counter() - start) * 1000)
        msg = f'"{request_line}" {response.status_code} {elapsed_ms}ms'
        (logger.error if response.status_code >= 400 else logger.info)(msg)
        return response
    except StarletteHTTPException as e:
        logger.error(f'"{request_line}" {e.status_code} - {e.detail}')
        return JSONResponse(status_code=e.status_code, content={"error": e.detail})
    except Exception as e:
        logger.error(f'"{request_line}" 500 - {e}', exc_info=True)
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})
