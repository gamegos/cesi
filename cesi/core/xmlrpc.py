from urllib.parse import urlparse, urlunparse
import xmlrpc.client


class XmlRpc:
    @staticmethod
    def connection(host, port, username, password):
        if not (host.startswith("http://") or host.startswith("https://")):
            host = "http://" + host
        scheme, netloc, path, params, query, fragment = urlparse(host)
        path = path.rstrip("/")
        server = "{}:{}".format(netloc, port)
        if not (username == "" and password == ""):
            server = "{username}:{password}@{server}".format(
                username=username, password=password, server=server
            )

        uri = urlunparse((scheme, server, path + "/RPC2", params, query, fragment))

        print(uri)
        return xmlrpc.client.ServerProxy(uri)
