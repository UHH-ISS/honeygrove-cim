from .config import CIMConfig
from .endpoint import CIMEndpoint

cfg = CIMConfig()
ep = CIMEndpoint(cfg)
ep.listen()
