import xmlrpc.client


class XmlRpc:
    @staticmethod
    def connection(host, port, username, password):
        server = "{host}:{port}/RPC2".format(host=host, port=port)
        if username == "" and password == "":
            address = "http://{server}/RPC2".format(server=server)
        else:
            address = "http://{username}:{password}@{server}/RPC2".format(
                username=username, password=password, server=server
            )

        print(server)
        return xmlrpc.client.ServerProxy(address)
