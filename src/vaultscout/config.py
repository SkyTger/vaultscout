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
            "не задана переменная VAULTSCOUT_DB_PASSWORD — добавьте её в .env"
        )
    with open(path) as file:
        data = yaml.safe_load(file)
        data.setdefault("database", {})["password"] = password
        return Config.model_validate(data)
