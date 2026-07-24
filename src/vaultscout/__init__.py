import sys

from pydantic import ValidationError

import vaultscout.config as config


def main() -> None:
    try:
        cfg = config.load_config("config.yaml")
        print(cfg)
    except FileNotFoundError:
        print("config.yaml не найден — скопируйте config.example.yaml и заполните")
        sys.exit(1)
    except ValidationError as e:
        print(f"ошибка в config.yaml: {e}")
        sys.exit(1)
    except config.ConfigError as e:
        print(e)
        sys.exit(1)
