from .config import CIMConfig

from elasticsearch.client.xpack.watcher import WatcherClient


class ESWatcher():

    watcher = None
    mattermost_url = None

    def __init__(self, es, url):
        self.watcher = WatcherClient(es)
        self.mattermost_url = url

    # Watcher alerts
    def put_watch(self):
        # HTTP brute force alert
        self.watcher.put_watch(
            id='brute_force_http',
            body={
                # Run the watch every 10 seconds
                'trigger': {'schedule': {'interval': '10s'}},

                # The search request to execute
                'input': {
                    'search': {
                        'request': {
                            'indices': ['honeygrove'],
                            'body': {
                                'query': {
                                    'bool': {
                                        'must': [
                                            {'match': {'service': "HTTP"}},
                                            {'match': {'successful': "false"}}],
                                        'filter': {
                                            'range': {
                                                '@timestamp': {
                                                    'from': 'now-10s',
                                                    'to': 'now'}}}}}}}}},

                # Search for at least 100 logs matching the condition
                'condition': {
                          'compare': {
                            'ctx.payload.hits.total': {
                              'gt': 100}}},

                # The actions to perform
                'actions': {
                    'mattermost_webhook': {
                        'webhook': {
                            'method': 'POST',
                            'url': self.mattermost_url,
                            'headers': {
                                'Content-Type': 'application/json'},
                            'body': {
                                'inline': {
                                    'text': ':heavy_exclamation_mark: **HTTP Brute Force Alert:** \n '
                                            '**{{ctx.payload.hits.total}}** **failed login attempts** was/were registered in the last 10 seconds. \n'
                                            'For an overview you can use the visualisations in **Kibana**.'}}}}}})

        # FTP brute force alert
        self.watcher.put_watch(
            id='brute_force_ftp',
            body={
                # Run the watch every 10 seconds
                'trigger': {'schedule': {'interval': '10s'}},

                # The search request to execute
                'input': {
                    'search': {
                        'request': {
                            'indices': ['honeygrove'],
                            'body': {
                                'query': {
                                    'bool': {
                                        'must': [
                                            {'match': {'service': "FTP"}},
                                            {'match': {'successful': "false"}}],
                                        'filter': {
                                            'range': {
                                                '@timestamp': {
                                                    'from': 'now-10s',
                                                    'to': 'now'}}}}}}}}},

                # Search for at least 100 logs matching the condition
                'condition': {
                          'compare': {
                            'ctx.payload.hits.total': {
                              'gt': 100}}},

                # The actions to perform
                'actions': {
                    'mattermost_webhook': {
                        'webhook': {
                            'method': 'POST',
                            'url': self.mattermost_url,
                            'headers': {
                                'Content-Type': 'application/json'},
                            'body': {
                                'inline': {
                                    'text': ':heavy_exclamation_mark: **FTP Brute Force Alert:** \n '
                                            '**{{ctx.payload.hits.total}}** **failed login attempts** was/were registered in the last 10 seconds. \n'
                                            'For an overview you can use the visualisations in **Kibana**.'}}}}}})

        # SSH brute force alert
        self.watcher.put_watch(
            id='brute_force_ssh',
            body={
                # Run the watch every 10 seconds
                'trigger': {'schedule': {'interval': '10s'}},

                # The search request to execute
                'input': {
                    'search': {
                        'request': {
                            'indices': ['honeygrove'],
                            'body': {
                                'query': {
                                    'bool': {
                                        'must': [
                                            {'match': {'service': "SSH"}},
                                            {'match': {'successful': "false"}}],
                                        'filter': {
                                            'range': {
                                                '@timestamp': {
                                                    'from': 'now-10s',
                                                    'to': 'now'}}}}}}}}},

                # Search for at least 100 logs matching the condition
                'condition': {
                          'compare': {
                            'ctx.payload.hits.total': {
                              'gt': 100}}},

                # The actions to perform
                'actions': {
                    'mattermost_webhook': {
                        'webhook': {
                            'method': 'POST',
                            'url': self.mattermost_url,
                            'headers': {
                                'Content-Type': 'application/json'},
                            'body': {
                                'inline': {
                                    'text': ':heavy_exclamation_mark: **SSH Brute Force Alert:** \n '
                                            '**{{ctx.payload.hits.total}}** **failed login attempts** was/were registered in the last 10 seconds. \n'
                                            'For an overview you can use the visualisations in **Kibana**.'}}}}}})

        # Malware alert
        self.watcher.put_watch(
            id='malware_alerts',
            body={
                # Run the watch every 10 seconds
                'trigger': {'schedule': {'interval': '10s'}},

                # The search request to execute
                'input': {
                    'search': {
                        'request': {
                            'indices': ['honeygrove'],
                            'body': {
                                'query': {
                                    'bool': {
                                        'filter': {
                                            'range': {
                                                '@timestamp': {
                                                    'from': 'now-10s',
                                                    'to': 'now'}}},
                                        'must': [{
                                            'range': {
                                                'percent': {
                                                    'gte': 30,
                                                    'lte': 100}}}]}}}}}},


                # Search for every log matching the condition
                'condition': {
                          'compare': {
                            'ctx.payload.hits.total': {
                              'gt': 0}}},

                # The actions to perform
                'actions': {
                    'mattermost_webhook': {
                        'webhook': {
                            'method': 'POST',
                            'url': self.mattermost_url,
                            'headers': {
                                'Content-Type': 'application/json'},
                            'body': {
                                'inline': {
                                    'text': ':heavy_exclamation_mark: **Malware Alert:** \n'
                                            '**{{ctx.payload.hits.total}}** new **malware file(s)** was/were discovered in the last 10 seconds. \n'
                                            'For an overview you can use the visualisations in **Kibana**.'}}}}}})

        # honeytoken alert
        self.watcher.put_watch(
            id='honeytoken_alerts',
            body={
                # Run the watch every 10 seconds
                'trigger': {'schedule': {'interval': '10s'}},

                # The search request to execute
                'input': {
                    'search': {
                        'request': {
                            'indices': ['honeygrove'],
                            'body': {
                                'query': {
                                    'bool': {
                                        'must': [
                                            {'match': {'successful': "true"}}],
                                        'filter': {
                                            'range': {
                                                '@timestamp': {
                                                    'from': 'now-10s',
                                                    'to': 'now'}}}}}}}}},

                # Search for every log matching the condition
                'condition': {
                          'compare': {
                            'ctx.payload.hits.total': {
                              'gt': 0}}},

                # The actions to perform
                'actions': {
                    'mattermost_webhook': {
                        'webhook': {
                            'method': 'POST',
                            'url': self.mattermost_url,
                            'headers': {
                                'Content-Type': 'application/json'},
                            'body': {
                                'inline': {
                                    'text': ':heavy_exclamation_mark: **Honeytoken Alert:** \n'
                                            '**{{ctx.payload.hits.total}}** **honeytokens** was/were used in the last 10 seconds. \n'
                                            'For an overview you can use the visualisations in **Kibana**.'}}}}}})

        self.watcher.start()
        print('\033[94m'+'Watcher Alerts Complete.'+'\033[0m')
