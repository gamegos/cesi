# -*- coding: utf-8 -*-
import json
import socket
import time
import uhttplib

current_milliseconds = lambda: int(round(time.time() * 1000))

class DockerUnixSockConfig:
    instance = None
    @staticmethod
    def get_instance():
        if DockerUnixSockConfig.instance is None:
            DockerUnixSockConfig.instance = DockerUnixSockConfig()
        return DockerUnixSockConfig.instance
    def __init__(self):
        pass
    def __get_ip_address__(self, container):
        if 'NetworkSettings' not in container:
            return None
        network_settings = container['NetworkSettings']
        if 'Networks' not in network_settings:
            return None
        networks = network_settings['Networks']
        if 'bridge' not in networks:
            return None
        bridge = networks['bridge']
        if 'IPAddress' not in bridge:
            return None
        return bridge['IPAddress']
    def __get_name__(self, container):
        names = [name[1:] for name in container['Names'] if '/' not in name[1:]]
        return '/'.join(names)

    def __test_port__(self, ip_address, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            sock.connect((ip_address, port))
            sock.close()
        except:
            return False
        return True

    def __get_container_data__(self, cfg):
        conn = uhttplib.UnixHTTPConnection(cfg.get('cesi', 'node_file'))
        conn.request('GET', '/containers/json')
        resp = conn.getresponse()
        return resp.read()

    def __build_conf__(self, cfg):
        data = self.__get_container_data__(cfg)
        containers = json.loads(data)
        result = dict()
        for container in containers:
            ip_address = self.__get_ip_address__(container)
            if ip_address is None:
                continue
            port = 9001
            name = self.__get_name__(container)
            if not self.__test_port__(ip_address, port):
                continue
            result[name] = {'hostname':ip_address, 'port':port, 'username':'', 'password':''}
        return result

    __config__ = None
    __config_last_update__ = 0

    def get_config(self, cfg):
        if current_milliseconds() - self.__config_last_update__ > 30 * 1000:
            self.__config__ = self.__build_conf__(cfg)
            self.__config_last_update__ = current_milliseconds()
        return self.__config__

read = lambda cfg: [name for name in DockerUnixSockConfig.get_instance().get_config(cfg)]
def config(cfg, node_name):
    cfg = DockerUnixSockConfig.get_instance().get_config(cfg)[node_name]
    username = cfg['username']
    password = cfg['password']
    host = cfg['host']
    port = cfg['port']
    return (username, password, host, port, )