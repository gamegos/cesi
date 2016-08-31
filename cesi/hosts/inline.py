def read(cfg):
    return [name[5:] for name in cfg.sections() if name[:4] == 'node']

def config(cfg, node_name):
    node_name = 'node:%s' % (node_name)
    username = cfg.get(node_name, 'username')
    password = cfg.get(node_name, 'password')
    host = cfg.get(node_name, 'host')
    port = cfg.get(node_name, 'port')
    return (username, password, host, port, )