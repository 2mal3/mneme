import logging

from mneme.config import CONFIG

_LEVEL = logging.DEBUG if CONFIG.DEBUG else logging.INFO

log = logging.getLogger("somnus")

_formatter = logging.Formatter(
    "[%(asctime)s] [%(module)s/%(process)d/%(levelname)s]: %(message)s", datefmt="%d-%m-%y %H:%M:%S"
)

log.setLevel(_LEVEL)
_console_handler = logging.StreamHandler()
_console_handler.setLevel(_LEVEL)
_console_handler.setFormatter(_formatter)
log.addHandler(_console_handler)
