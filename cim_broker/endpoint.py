from .es import check_ping, get_instance
from .malware import check_file_for_malware

import base64
from datetime import datetime
import json

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

        self.log_queue = self.endpoint.make_subscriber("logs")
        self.file_queue = self.endpoint.make_subscriber("files")

        self.es_instance = get_instance(self.config.ElasticIP, self.config.ElasticPort)


    def listen(self):
        self.endpoint.listen(self.config.BrokerIP, self.config.BrokerPort)

        print("listening at {}:{}".format(self.config.BrokerIP, self.config.BrokerPort))
        while True:
            logs = self.log_queue.poll()
            files = self.file_queue.poll()

            self.process_logs(logs)
            self.process_files(files)


    def process_files(self, files):
        """
        receives malwarefiles over the "filesQueue" messagetopic
        and saves them with consecutive timestamps

        :param: files
        """
        timestamp = datetime.utcnow().isoformat()
        for msg in files:
            for m in msg:
                with open('./ressources/%s.file' % timestamp, 'wb') as afile:
                    afile.write(base64.b64decode(str(m))) 
            check_file_for_malware(m)


    def process_logs(self, logs):
        """
        receives logfiles over the "logsQueue" messagetopic
        and saves them in a JSON-file

        :param logs:
        """

        for (topic, data) in logs:
            for entry in [data]:
                print("Log: ", entry)

                # if connection to Elasticsearch is interrupted, cache logs into logs.json to prevent data loss.
                if not check_ping(self.config.ElasticIP, self.config.ElasticPort):
                    print('\033[91m' + "The logs will be saved in the logs.json under "
                                       "/incidentmonitoring/ressources." + '\033[0m')
                    with open('./incidentmonitoring/ressources/logs.json', 'a') as outfile:
                        outfile.write(str(entry))
                        outfile.write('\n')

                else:
                    try:
                        output_logs = json.loads(str(entry))
                        # send logs into Elasticsearch
                        month = datetime.utcnow().strftime("%Y-%m")
                        indexname = "honeygrove-" + month
                        self.es_instance.index(index=indexname, doc_type="log_event", body=output_logs)

                    except Exception:
                        pass
