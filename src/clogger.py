import os
import logging


def setup_custom_logger(name):
#    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(name)
    logger.propagate = False
    hdlr = logging.FileHandler(os.environ.get('LOG_DIR','../../logs') + "/" + os.environ.get('TEST_TYPE','smoke')  + '.log')
    #hdlr = logging.FileHandler( "../../logs/login.log")
    formatter = logging.Formatter(fmt='%(asctime)s[%(levelname)s][%(funcName)s][%(name)s:%(lineno)d)] %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    return logger
