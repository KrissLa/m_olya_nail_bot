from loguru import logger


logger.add(sink=f"logs/info.log",
           format="{time:D-M-YYYY dddd HH:mm Z} || {level} || {message} || line: {line}, {function} |||",
           level='INFO',
           encoding="utf8")
