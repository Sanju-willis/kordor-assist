# src\app\middleware\error_handler.py
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.exceptions import BaseError
from app.lib.logger import logger
from jose import JWTError, ExpiredSignatureError
from langgraph.errors import GraphRecursionError


async def error_handling_middleware(request: Request, call_next):
    try:
        return await call_next(request)

    except RequestValidationError as e:
        logger.error(f"{request.method} {request.url.path} 422 - validation error: {e}")
        return JSONResponse(
            status_code=422,
            content={"error": "Validation failed", "details": e.errors()},
        )

    except StarletteHTTPException as e:
        logger.error(
            f"{request.method} {request.url.path} {e.status_code} - {e.detail}"
        )
        return JSONResponse(status_code=e.status_code, content={"error": e.detail})
    except ExpiredSignatureError as e:
        logger.error(f"{request.method} {request.url.path} 401 - token expired{e}")
        return JSONResponse(status_code=401, content={"error": "Token expired"})

    except JWTError as e:
        logger.error(f"{request.method} {request.url.path} 401 - invalid token: {e}")
        return JSONResponse(status_code=401, content={"error": "Invalid token"})

    except BaseError as e:
        logger.error(
            f"{request.method} {request.url.path} {e.status_code} - {e.message}"
        )
        return JSONResponse(status_code=e.status_code, content={"error": e.message})

    except ValueError as e:
        logger.error(f"{request.method} {request.url.path} 400 - {e}")
        return JSONResponse(status_code=400, content={"error": str(e)})
    
    except AttributeError as e:
        logger.error(f"{request.method} {request.url.path} 500 - attribute error: {e}")
        return JSONResponse(
            status_code=500, content={"error": "Attribute error", "details": str(e)}
        )
    except GraphRecursionError as e:
        logger.error(f"{request.method} {request.url.path} 500 - graph recursion error: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "AI graph recursion error",
                "detail": str(e),
                "hint": "Your AI workflow got stuck in a loop. Fix your branching logic or add an END state."
            }
        )


    except Exception as e:
        logger.error(f"{request.method} {request.url.path} 500 - {e}", exc_info=True)
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})
