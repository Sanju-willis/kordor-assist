import uvicorn
from app.config.settings import settings

def main():
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="warning",
    )
