from .config import CIMConfig

import json
import socket

from elasticsearch import Elasticsearch

# Check if Elasticsearch on port 9200 is reachable
def check_ping(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((ip, port))
    if result == 0:
        pingstatus = True
    else:
        pingstatus = False
        print('\033[91m' + "The connection to Elasticsearch is interrupted..." + '\033[0m')
    return pingstatus

def get_instance(ip, port):
    return Elasticsearch([{'host': ip, 'port': port}])

# Define the mapping and load it into the Elasticsearch index
def loadMapping(es_instance):
    mapping = '''{
        "index_patterns": "honeygrove-*",
        "mappings": {
            "log_event": {
                "properties": {
                    "event_type": {"type": "keyword"},
                    "@timestamp": {"type": "date", "format": "yyyy-MM-dd'T'HH:mm:ss.SSSSSS"},
                    "actual": {"type": "keyword"},
                    "filename": {"type": "keyword"},
                    "found_date": {"type": "date", "format": "yyyy-MM-dd'T'HH:mm:ss.SSSSSS"},
                    "hash": {"type": "keyword"},
                    "honeypotID": {"type": "keyword"},
                    "infolink": {"type": "keyword"},
                    "ip": {"type": "ip"},
                    "key": {"type": "keyword"},
                    "percent": {"type": "integer"},
                    "port": {"type": "keyword"},
                    "request": {"type": "keyword"},
                    "request_type": {"type": "keyword"},
                    "response": {"type": "keyword"},
                    "service": {"type": "keyword"},
                    "successful": {"type": "keyword"},
                    "user": {"type": "keyword"},
                    "coordinates": {"type": "geo_point"}
                }
            }
        }
    }'''

    # Create a template with the mapping that is applied to all indices starting with "honeygrove-"
    es_instance.indices.put_template(name='log_event', body=json.loads(mapping))


# Start with mapping if Elasticsearch is reachable and cluster status is ready ("yellow")
def readyToMap(ip, port, es_instance):
    try:
        if check_ping(ip, port):
            health = es_instance.cluster.health()
            if 'status' in health:
                h = (health['status'])
                if h == 'yellow' or h == 'green':
                    loadMapping(es_instance)
                    print('\033[94m' + 'Mapping Complete.' + '\033[0m')

                    # Execute Watcher alerts script
                    print('\033[94m' + "Start Watcher Alerts..." + '\033[0m')
                    WatcherAlerts.putWatch()

                else:
                    print('\033[91m' + "es-master cluster state is red, trying again in 10s..." + '\033[0m')
                    # Wait 10 seconds and retry checking cluster state
                    time.sleep(10)
                    readyToMap(ip, port, es_instance)
        else:
            # Retry connection attempt every 10 seconds
            time.sleep(10)
            readyToMap(ip, port, es_instance)

    except:
        print('\033[91m' + "an error occurred, please try again later..." + '\033[0m')
        print('\033[91m' + "aborting..." + '\033[0m')


if __name__ == '__main__':
    cfg = CIMConfig()
    es = Elasticsearch([{'host': cfg.ElasticIP, 'port': cfg.ElasticPort}])

    # Start the mapping process
    print('\033[94m'+"Start Mapping..."+'\033[0m')
    readyToMap(cfg.ElasticIP, cfg.ElasticPort, es)
