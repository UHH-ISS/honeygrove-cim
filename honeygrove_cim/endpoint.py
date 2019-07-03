from honeygrove_cim.es import check_ping, get_instance
from honeygrove_cim.malware import check_file_for_malware

import base64
from datetime import datetime
import json
import os
import select
from time import sleep
from sys import stdout

import broker


class Endpoint:
    config = None
    endpoint = None

    log_queue = None
    file_queue = None

    elastic = None

    def __init__(self, cfg):
        self.config = cfg

        # Broker Configuration
        bcfg = broker.Configuration()
        # (Optional) SSL Configuration
        if cfg.BrokerSSLCAFile:
            bcfg.openssl_cafile = cfg.BrokerSSLCAFile  # Path to CA file
        if cfg.BrokerSSLCAPath:
            bcfg.openssl_capath = cfg.BrokerSSLCAPath  # Path to directory with CA files
        if cfg.BrokerSSLCertificate:
            bcfg.openssl_certificate = cfg.BrokerSSLCertificate  # Own certificate
        if cfg.BrokerSSLKeyFile:
            bcfg.openssl_key = cfg.BrokerSSLKeyFile  # Own key

        self.endpoint = broker.Endpoint(bcfg)

        # Status Subscriber
        self.status_queue = self.endpoint.make_status_subscriber(True)
        # Message Subscribers
        self.log_queue = self.endpoint.make_subscriber("logs")
        self.file_queue = self.endpoint.make_subscriber("files")

        self.elastic = get_instance(self.config.ElasticIP, self.config.ElasticPort)

    def ensure_elastic(self):
        ip = self.config.ElasticIP
        port = self.config.ElasticPort
        print("[Endpoint] Waiting for Elasticsearch to come online at {}:{}..".format(ip, port), flush=True)
        while not check_ping(self.config.ElasticIP, self.config.ElasticPort, print_status=False):
            sleep(1)
        print("[Endpoint] Elasticseach found at {}:{}".format(ip, port), flush=True)

    def listen(self):
        port = self.endpoint.listen(self.config.BrokerIP, self.config.BrokerPort)
        if port == 0:
            raise RuntimeError("Unable to listen on Broker port {}".format(self.config.BrokerPort))

        print("[Endpoint] Listening on {}:{}".format(self.config.BrokerIP, port))
        fds = [self.status_queue.fd()]

        while True:
            stdout.flush()

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
                if changed:
                    continue

            # - Log
            if self.log_queue.fd() in result[0]:
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
                check_file_for_malware(path, self.elastic)

    def process_logs(self, logs):
        # Loop through broker messages
        for (topic, data) in logs:
            # Loop through message dictionary
            for index, jdocument in data:
                if check_ping(self.config.ElasticIP, self.config.ElasticPort):
                    try:
                        # Decode json document and push it to elasticsearch
                        doc = json.loads(jdocument)
                        self.elastic.index(index=index, body=doc)

                    except Exception as ex:
                        # XXX: Improve this
                        print("Exception encountered while adding log to elasticsearch: ", ex, flush=True)
                else:
                    with open(self.config.LogPath, 'a') as fp:
                        # if connection to Elasticsearch is interrupted, cache logs to prevent data loss
                        print("[Endpoint] The logs will be saved at {}".format(self.config.LogPath))
                        fp.write(jdocument + '\n')


def _flatten(items):
    for x in items:
        if hasattr(x, '__iter__') and not isinstance(x, str):
            for y in _flatten(x):
                yield y
        else:
            yield x
