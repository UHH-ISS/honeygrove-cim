from honeygrove_cim.config import Config
from honeygrove_cim.endpoint import Endpoint


def main():
    cfg = Config()
    ep = Endpoint(cfg)
    ep.ensure_elastic()
    ep.listen()


if __name__ == '__main__':
    main()
