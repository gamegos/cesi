__author__ = 'gkawamoto'
__version__ = '1.0'

import importlib

def __get_reader__ (cfg):
    node_discovery = cfg.get('cesi', 'node_discovery') if cfg.has_option('cesi', 'node_discovery') else 'inline'
    return importlib.import_module('.%s' % node_discovery, __package__)
def read(cfg):
    return __get_reader__(cfg).read(cfg)
def config(cfg, node_name):
    return __get_reader__(cfg).config(cfg, node_name)