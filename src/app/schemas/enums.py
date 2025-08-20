# src\app\schemas\enums.py
from enum import Enum


class Module(str, Enum):
    home = "home"
    social = "social"
    analytics = "analytics"


class ThreadType(str, Enum):
    module = "module"
    company = "company"
    product = "product"
