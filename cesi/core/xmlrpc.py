import xmlrpc.client


class XmlRpc:
    @staticmethod
    def connection(host, port, username, password):
        if username == "" and password == "":
            address = "http://{0}:{1}/RPC2".format(host, port)
        else:
            address = "http://{0}:{1}@{2}:{3}/RPC2".format(
                username, password, host, port
            )

        try:
            return xmlrpc.client.ServerProxy(address)
        except Exception as e:
            print(e)
            return None
