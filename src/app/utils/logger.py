# src\app\utils\logger.py
import logging
import sys

# ---- Configure root logging ----
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(filename)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

# Reduce noise from external libraries
logging.getLogger("uvicorn").setLevel(logging.WARNING)
logging.getLogger("fastapi").setLevel(logging.WARNING)

# Export a shared logger
logger = logging.getLogger()  # root logger


# format="%(levelname)s | %(filename)s | %(method)s %(path)s HTTP/%(http_version)s | %(status_code)s
# | %(client_ip)s | %(user_agent)s | %(message)s"
