import logging

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)  # or whatever
handler = logging.FileHandler('main.log', 'w', 'utf-8')  # or whatever
formatter = logging.Formatter('%(asctime)s - %(message)s')  # or whatever
handler.setFormatter(formatter)  # Pass handler as a parameter, not assign
root_logger.addHandler(handler)


def log_inf(string):
    root_logger.info(string)


def log_deb(string):
    root_logger.debug(string)


def log_err(string):
    root_logger.error(string)
