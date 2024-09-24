import logging.config
import os


def singleton(cls):
    instances = {}

    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return get_instance()


current_path = os.path.dirname(os.path.abspath(__file__))


@singleton
class Logger:
    def __init__(self):
        logging.config.fileConfig(current_path + "/logging.conf")
        self.logr = logging.getLogger("root")
