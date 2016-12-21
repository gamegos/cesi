__author__ = 'gkawamoto'
__version__ = '1.0'

import importlib

def validate_password(username, password, dbpassword, auth_mode):
    validator = importlib.import_module('.%s' % auth_mode, __package__)
    valid = validator.validate(username, password, dbpassword)
    if not valid and auth_mode != 'basic' and len(dbpassword) > 0:
        valid = validate_password(username, password, dbpassword, 'basic')
    return valid