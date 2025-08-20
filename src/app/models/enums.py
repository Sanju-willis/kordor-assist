# src\app\models\enums.py
from enum import Enum
from typing import Dict

class ModuleEnum(str, Enum):
    HOME = "home"
    SOCIAL = "social"
    ANALYTICS = "analytics"

class ThreadType(str, Enum):
    MODULE = "module"
    COMPANY = "company"
    PRODUCT = "product"

STAGE_MAP: Dict[str, str] = {
    "company:*": "company_ready",
    "product:*": "product_ready",
    "module:home": "onboarding",
    "module:social": "social_ready",
    "module:analytics": "analytics_ready",
}