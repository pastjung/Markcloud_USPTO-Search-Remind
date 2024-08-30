# 로그 메시지를 포맷팅하여 출력하며, 로그 레벨에 따라 생상을 다르게 표시하여 시각적으로 구분하도록 하는 기능

import logging

class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - [%(levelname)s]:: %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

syslog = logging.StreamHandler()
syslog.setLevel(logging.DEBUG)
syslog.setFormatter(CustomFormatter())
logger.addHandler(syslog)
