from honeygrove_adapter.config import Config
from honeygrove_adapter.es_watcher import ESWatcher

import socket

from elasticsearch import Elasticsearch


# Check if Elasticsearch on port 9200 is reachable
def check_ping(ip, port, print_status=True):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((ip, port))
    if result == 0:
        pingstatus = True
    else:
        pingstatus = False
        if print_status:
            print('\033[91m' + "The connection to Elasticsearch is interrupted..." + '\033[0m')
    return pingstatus


def get_instance(ip, port):
    return Elasticsearch([{'host': ip, 'port': port}])
