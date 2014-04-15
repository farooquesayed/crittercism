import os
import logging


def setup_custom_logger(name):
#    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(name)
    logger.propagate = False
    hdlr = logging.FileHandler(os.environ['LOG_DIR'] + "/yopenstackqe_" + os.environ['TEST_TYPE'] + '.log')
    formatter = logging.Formatter(fmt='%(asctime)s[%(levelname)s][%(funcName)s][%(name)s:%(lineno)d)] %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    return logger
