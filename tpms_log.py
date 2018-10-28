# -*- coding: utf-8 -*-

# # # # # # # # # # # # #
# tpms_log.py           #
# MarooElectronics Inc. #
# # # # # # # # # # # # #

# Import Standard Modules
import os, logging.handlers

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

fileMaxByte = 10 * 1024 * 1024  # 10MB
file_handler = logging.handlers.TimedRotatingFileHandler(os.getcwd()+'/logs/system.log', when='midnight', interval=1, encoding='utf-8')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


# Import Standard Modules
def debug(value):
    logger.debug(value)


def info(value):
    logger.info(value)


def warning(value):
    logger.warning(value)


def error(value):
    logger.error(value)


def critical(value):
    logger.critical(value)
