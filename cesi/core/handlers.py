import functools
import xmlrpc.client


def xmlrpc_exceptions(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except xmlrpc.client.Fault as err:
            return False, err.faultString
        except xmlrpc.client.ProtocolError as err:
            return False, err.errmsg
        except Exception as err:
            return False, str(err)

    return wrapped
