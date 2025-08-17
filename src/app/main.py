# src\app\main.py
import logging
import sys
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from app.api.chat import router

# Simple readable logging format
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s | %(name)s | %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Reduce noise from external libraries
logging.getLogger("uvicorn").setLevel(logging.WARNING)
logging.getLogger("fastapi").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

app = FastAPI(title="Kordor Assist")

# Cleaner global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    error_msg = f"ERROR on {request.method} {request.url.path}: {str(exc)}"
    logger.error(error_msg)
    return JSONResponse(
        status_code=500,
        content={"error": str(exc)}
    )

# Simpler request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    if response.status_code >= 400:
        logger.error(f"Failed: {response.status_code}")
    else:
        logger.info(f"Success: {response.status_code}")
    return response

app.include_router(router)

@app.get("/")
async def root():
    return {"status": "Kordor Assist is running"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Kordor Assist...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="warning")
