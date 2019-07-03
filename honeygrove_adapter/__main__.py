from honeygrove_adapter.config import Config
from honeygrove_adapter.endpoint import Endpoint


def main():
    cfg = Config()
    ep = Endpoint(cfg)
    ep.ensure_elastic()
    ep.listen()


if __name__ == '__main__':
    main()
