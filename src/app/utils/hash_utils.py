# src\app\utils\hash_utils.py
import hashlib
from typing import Optional


def generate_thread_id(
    user_id: str,
    company_id: str,
    module: str,
    thread_type: str,
    parent_thread_id: Optional[str] = None,
    entity_id: Optional[str] = None,
) -> str:
    key_parts = [user_id, company_id, module, thread_type]

    if parent_thread_id:
        key_parts.append(parent_thread_id)

    if entity_id:
        key_parts.append(entity_id)

    # Create hash input
    key = "_".join(key_parts)

    # Generate short hash (8 characters)
    hash_suffix = hashlib.md5(key.encode()).hexdigest()[:8]

    return f"{module}_{thread_type}_{hash_suffix}"
