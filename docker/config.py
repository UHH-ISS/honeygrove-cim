class Config:
    BrokerIP = "0.0.0.0"
    BrokerPort = 34445

    BrokerSSLCAFile = None # Path to CA file
    BrokerSSLCAPath = None # Path to directory with CA files
    BrokerSSLCertificate = None # Own certificate
    BrokerSSLKeyFile = None # Own key

    ElasticIP = "elasticsearch"
    ElasticPort = 9200

    MattermostUrl = ""

    LogPath = "/var/honeygrove/cim/logs.json"
    MalwarePath = "/var/honeygrove/cim/uploads"
