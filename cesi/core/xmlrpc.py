import xmlrpc.client

class XmlRpc:
    @staticmethod
    def connection(host, port, username, password):
        server = "{}:{}".format(host, port)
        credentials = "{}:{}".format(username, password)
        if username == "" and password == "":
            uri = "http://{server}/RPC2".format(server=server)
        else:
            uri = "http://{credentials}@{server}/RPC2".format(
                credentials=credentials, server=server
            )

        print(uri)
        return xmlrpc.client.ServerProxy(uri)
