import structlog
import logging

# Configuración básica
logging.basicConfig(
    format="%(message)s",
    level=logging.INFO
)

# Configuración de structlog
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer()
    ]
)

logger = structlog.get_logger()