import logging

class ActivityLog:
    logger = None

    @staticmethod
    def set_logger(log_name="activitiy",
                    log_path="activitiy.log",
                    log_format="%(asctime)s [%(levelname)s]: %(message)s",
                    log_level=logging.INFO):

        logger = logging.getLogger(log_name)
        logger.setLevel(log_level)
        logger_file_handler = logging.FileHandler(log_path)
        logger_file_handler.setLevel(log_level)
        logger_file_handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(logger_file_handler)
        ActivityLog.logger = logger
