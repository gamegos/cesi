import logging

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