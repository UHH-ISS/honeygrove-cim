from cim_broker.es import check_ping, get_instance
from cim_broker.malware import check_file_for_malware

import base64
from datetime import datetime
import json
import os
import select

import broker


class CIMEndpoint:
    config = None
    endpoint = None

    log_queue = None
    file_queue = None

    es_instance = None

    def __init__(self, cfg):
        self.config = cfg
        self.endpoint = broker.Endpoint()
        
        # Status Subscriber
        self.status_queue = self.endpoint.make_status_subscriber(True)
        # Message Subscribers
        self.log_queue = self.endpoint.make_subscriber("logs")
        self.file_queue = self.endpoint.make_subscriber("files")

        self.es_instance = get_instance(self.config.ElasticIP, self.config.ElasticPort)

    def listen(self):
        port = self.endpoint.listen(self.config.BrokerIP, self.config.BrokerPort)
        if port == 0:
            raise RuntimeError("Unable to listen on Broker port {}".format(self.config.BrokerPort))

        print("Listening at {}:{}".format(self.config.BrokerIP, port))
        fds = [self.status_queue.fd()]

        while True:
            # Wait for something to do
            result = select.select(fds, [], [])
            
            # - Status
            if self.status_queue.fd() in result[0]:
                changed = False
                for st in self.status_queue.poll():
                    # Error
                    if type(st) == broker.Error:
                        print("[Broker Error] {}". format(st))
                    # Status
                    elif type(st) == broker.Status:
                        print("[Broker Status] {}". format(st))
                        changed = True
                        # became connected:
                        if st.code() == broker.SC.PeerAdded:
                            if self.log_queue.fd() not in fds:
                                fds.append(self.log_queue.fd())
                            if self.file_queue.fd() not in fds:
                                fds.append(self.file_queue.fd())
                        # became disconnected:
                        else:
                            if self.log_queue in fds:
                                fds.remove(self.log_queue.fd())
                            if self.file_queue in fds:
                                fds.remove(self.file_queue.fd())
                    else:
                        raise RuntimeError("Unknown Broker Status Type")
                # Apply new fds
                if changed: continue
                    
            # - Log
            if self.log_queue.fd()  in result[0]:
                logs = self.log_queue.poll()
                self.process_logs(logs)
            
            # - File
            if self.file_queue.fd() in result[0]:
                files = self.file_queue.poll()
                self.process_files(files)

    def process_files(self, files):
        for (topic, data) in files:
            # Do this to accept both lists and single values
            data = _flatten([data])
            for f in data:
                filename = '{}.file'.format(datetime.utcnow().isoformat())
                path = os.path.join(self.config.MalwarePath, filename)
                with open(path, 'wb') as fp:
                    fp.write(base64.b64decode(str(f)))
                check_file_for_malware(path, self.es_instance)

    def process_logs(self, logs):
        with open(self.config.LogPath, 'a') as fp:
            for (topic, data) in logs:
                # Do this to accept both lists and single values
                data = _flatten([data])
                for entry in data:
                    if check_ping(self.config.ElasticIP, self.config.ElasticPort):
                        try:
                            output_logs = json.loads(str(entry))
                            # send logs into Elasticsearch
                            month = datetime.utcnow().strftime("%Y-%m")
                            indexname = "honeygrove-" + month
                            self.es_instance.index(index=indexname, doc_type="log_event", body=output_logs)

                        except Exception:
                            # XXX: Improve this
                            pass
                    else:
                        # if connection to Elasticsearch is interrupted, cache logs to prevent data loss
                        print("The logs will be saved at {}".format(self.config.LogPath))
                        fp.write(str(entry))
                        fp.write('\n')


def _flatten(items):
    for x in items:
        if hasattr(x, '__iter__') and not isinstance(x, str):
            for y in _flatten(x):
                yield y
        else:
            yield x
