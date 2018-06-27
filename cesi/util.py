import logging

from flask import (
    jsonify,
    g
)

from core import (
    Cesi
)

class ActivityLog:
    __instance = None

    def __init__(self,
                log_name="activitiy",
                log_path="activitiy.log",
                log_format="%(asctime)s [%(levelname)s]: %(message)s",
                log_level=logging.INFO):
        if ActivityLog.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.logger = logging.getLogger(log_name)
            self.logger.setLevel(log_level)
            logger_file_handler = logging.FileHandler(log_path)
            logger_file_handler.setLevel(log_level)
            logger_file_handler.setFormatter(logging.Formatter(log_format))
            self.logger.addHandler(logger_file_handler)
            ActivityLog.__instance = self

    @staticmethod
    def getInstance():
        """ Static access method """
        if ActivityLog.__instance == None:
            ActivityLog()
        return ActivityLog.__instance

class JsonValue:

    @staticmethod
    def success(node=None,
                process_name="",
                event_name="",
                status="Success",
                code=80):

        return jsonify(status=status,
                       code=code,
                       message = f"{node.name} {process_name} {event_name} event succesfully",
                       nodename = node.name,
                       data = node.get_process(process_name))

    @staticmethod
    def error(node=None,
            process_name="",
            event_name="",
            status="Error",
            code=0,
            payload=""):

        return jsonify(status=status,
                       code=code,
                       message = f"{node.name} {process_name} {event_name} event unsuccesfully",
                       nodename = node.name,
                       payload=payload)

# Database connection
def get_db():
    cesi = Cesi.getInstance()
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = cesi.get_db_connection()
    return db