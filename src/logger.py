import os
import logging


def setup_custom_logger(name):
#    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(name)
    logger.propagate = False
    #hdlr = logging.FileHandler(os.environ['LOG_DIR'] or "./" + "/login" + os.environ['TEST_TYPE'] or "sample" + '.log')
    hdlr = logging.FileHandler( "../../logs/login.log")
    formatter = logging.Formatter(fmt='%(asctime)s[%(levelname)s][%(funcName)s][%(name)s:%(lineno)d)] %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    return logger
