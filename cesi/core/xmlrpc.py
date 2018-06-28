import xmlrpc.client

class XmlRpc:
    @staticmethod
    def connection(host, port, username, password):
        if username == "" and password == "":
            address = f"http://{host}:{port}/RPC2"
        else:
            address = f"http://{username}:{password}@{host}:{port}/RPC2"

        try:
            return xmlrpc.client.ServerProxy(address)
        except Exception as e:
            print(e)
            return None