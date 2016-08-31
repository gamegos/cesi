__author__ = 'gkawamoto'
__version__ = '1.0'

def validate_password(username, password, dbpassword, auth_mode):
    if auth_mode == 'basic':
        return password == dbpassword
    
    raise Exception('Invalid auth method \'%s\'' % auth_mode)