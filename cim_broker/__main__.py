from cim_broker.config import CIMConfig
from cim_broker.endpoint import CIMEndpoint

cfg = CIMConfig()
ep = CIMEndpoint(cfg)
ep.listen()
