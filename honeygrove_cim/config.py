class Config:
    BrokerIP = "127.0.0.1"
    BrokerPort = 34445

    BrokerSSLCAFile = None # Path to CA file
    BrokerSSLCAPath = None # Path to directory with CA files
    BrokerSSLCertificate = None # Own certificate
    BrokerSSLKeyFile = None # Own key

    ElasticIP = "127.0.0.1"
    ElasticPort = 9200

    MattermostUrl = ""

    LogPath = "/var/honeygrove/cim/logs.json"
    MalwarePath = "/var/honeygrove/cim/uploads"
