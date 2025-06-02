import os
import yaml
from pydantic import BaseModel


# --------------------
# Config Models
# --------------------

class Database(BaseModel):
    host: str
    port: int
    database: str


class MainConfig(BaseModel):
    calculation_db: Database


# --------------------
# Config Loader
# --------------------

class ConfigLoader:
    @staticmethod
    def _load_yaml(path: str) -> dict:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Config file {path} not found.")

        with open(path, "r") as file:
            return yaml.safe_load(file)

    @staticmethod
    def load() -> MainConfig:
        """
        Try loading configuration from different sources in order:
        1. Default production path
        2. From environment variable if set
        3. Default development path
        """
        try_paths = [
            "/CONFIG",  # Docker path / Linux path
            "/etc/CONFIG"   # Development / Mac path
        ]

        for path in try_paths:
            if path and os.path.exists(path):
                config_dict = ConfigLoader._load_yaml(path)
                return MainConfig(**config_dict)

        raise FileNotFoundError("No valid configuration found.")
