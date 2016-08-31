__author__ = 'gkawamoto'
__version__ = '1.0'

import importlib

def validate_password(username, password, dbpassword, auth_mode):
    validator = importlib.import_module('.%s' % auth_mode, __package__)
    return validator.validate(username, password, dbpassword)