import os

import yaml
from dotenv import load_dotenv
from pydantic import BaseModel, SecretStr


class VaultConfig(BaseModel):
    path: str


class EmbeddingsConfig(BaseModel):
    model: str


class DatabaseConfig(BaseModel):
    host: str
    port: int
    name: str
    user: str
    password: SecretStr


class Config(BaseModel):
    vault: VaultConfig
    embeddings: EmbeddingsConfig
    database: DatabaseConfig


class ConfigError(Exception):
    pass


def load_config(path: str) -> Config:
    load_dotenv()
    password = os.environ.get("VAULTSCOUT_DB_PASSWORD")
    if not password:
        raise ConfigError(
            "не задана переменная VAULTSCOUT_DB_PASSWORD - добавьте её в .env"
        )

    try:
        with open(path, encoding="utf-8") as file:
            data = yaml.safe_load(file)
    except yaml.YAMLError as e:
        raise ConfigError(f"{path} - некорректный YAML: {e}") from e

    if not isinstance(data, dict):
        raise ConfigError(f"{path}: ожидался набор секций vault, embeddings, database")

    database = data.setdefault("database", {})
    if not isinstance(database, dict):
        raise ConfigError(f"{path}: секция database должна быть набором полей")
    database["password"] = password

    return Config.model_validate(data)
