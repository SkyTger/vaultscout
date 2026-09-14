import pytest

from vaultscout.config import ConfigError, load_config


def test_empty_file(tmp_path, monkeypatch):
    monkeypatch.setenv("VAULTSCOUT_DB_PASSWORD", "secret")
    config_file = tmp_path / "config.yaml"
    config_file.write_text("", encoding="utf-8")

    with pytest.raises(ConfigError, match="ожидался набор секций"):
        load_config(str(config_file))


def test_just_text_file(tmp_path, monkeypatch):
    monkeypatch.setenv("VAULTSCOUT_DB_PASSWORD", "secret")
    config_file = tmp_path / "config.yaml"
    config_file.write_text("просто текст", encoding="utf-8")

    with pytest.raises(ConfigError, match="ожидался набор секций"):
        load_config(str(config_file))


def test_broken_file(tmp_path, monkeypatch):
    monkeypatch.setenv("VAULTSCOUT_DB_PASSWORD", "secret")
    config_file = tmp_path / "config.yaml"
    config_file.write_text('vault: "abc', encoding="utf-8")

    with pytest.raises(ConfigError, match="некорректный YAML"):
        load_config(str(config_file))


def test_not_dict_file(tmp_path, monkeypatch):
    monkeypatch.setenv("VAULTSCOUT_DB_PASSWORD", "secret")
    config_file = tmp_path / "config.yaml"
    config_file.write_text("database: postgres", encoding="utf-8")

    with pytest.raises(ConfigError, match="секция database должна быть набором полей"):
        load_config(str(config_file))
