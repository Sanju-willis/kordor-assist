# src\app\core\deps.py
from app.core.thread_manager import thread_manager

def get_thread_manager():
    return thread_manager

def get_chat_service():
    from app.services.chat_service import ChatService
    return ChatService
