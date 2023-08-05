import logging
import sys

logger = logging.getLogger()
logger.setLevel(logging.INFO)

log_format = logging.Formatter('[%(asctime)s] [%(levelname)s] - %(message)s')

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
handler.setFormatter(log_format)
logger.addHandler(handler)


def info(msg):
    logger.info(msg)