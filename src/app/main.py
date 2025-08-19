# src\app\main.py
from app.app import create_app

app = create_app()  # for uvicorn: `uvicorn app.main:app`

