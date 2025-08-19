# src\app\utils\hash_utils.py
import hashlib
from typing import Optional


def generate_thread_id(
    module: str,
    thread_type: str,
    parent_thread_id: Optional[str] = None,
    entity_id: Optional[str] = None,
) -> str:
    """
    Generate a unique thread ID based on module, thread_type, and optional parent/entity.
    
    Args:
        module: The module name (e.g., "home", "social")
        thread_type: The thread type (e.g., "module", "company", "product")
        parent_thread_id: Optional parent thread ID for sub-threads
        entity_id: Optional entity ID for company/product threads
        
    Returns:
        A unique thread ID in format: {module}_{thread_type}_{hash}
    """
    key_parts = [module, thread_type]
    
    if parent_thread_id:
        key_parts.append(parent_thread_id)
    
    if entity_id:
        key_parts.append(entity_id)
    
    # Create hash input
    key = "_".join(key_parts)
    
    # Generate short hash (8 characters)
    hash_suffix = hashlib.md5(key.encode()).hexdigest()[:8]
    
    return f"{module}_{thread_type}_{hash_suffix}"