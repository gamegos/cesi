from urllib.parse import urlparse, urlunparse
import xmlrpc.client

class XmlRpc:
    @staticmethod
    def connection(host, port, username, password):
        if not host.startswith('http://') or host.startswith('https://'):
            host = 'http://' + host
        scheme, netloc, path, params, query, fragment = urlparse(host)
        path = path.rstrip('/')
        server = "{}:{}".format(netloc, port)
        credentials = "{}:{}".format(username, password)
        if username == "" and password == "":
            uri = urlunparse((scheme, server, path + '/RPC2', params, query, fragment))
        else:
            uri = urlunparse((scheme, '{credentials}@{server}'.format(credentials=credentials, server=server), path + '/RPC2', params, query, fragment))

        print(uri)
        return xmlrpc.client.ServerProxy(uri)
