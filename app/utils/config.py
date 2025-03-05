import yaml
from typing import Any
from .logger import logger

class ConfigLoader:
    def __init__(self, caminho_arquivo="config.yaml"):
        self.data = {}
        try:
            with open(caminho_arquivo, "r") as arquivo:
                self.data = yaml.safe_load(arquivo)
            logger.info(f"Config {caminho_arquivo} carregado com sucesso.")
        except FileNotFoundError:
            logger.error(f"{caminho_arquivo} Não encontrado.")
            self.data = {}
        except yaml.YAMLError as erro:
            logger.error(f"Erro no YAML: {erro}.")
            raise

    def get_value(self, caminho: str, padrao=None):
        keys = caminho.split(".")
        value = self.data
        for key in keys:
            value = value.get(key, padrao) if value else padrao
        if value is None and padrao is None:
            logger.warning(f"Chave {caminho} não existe no config")
        return value

config = ConfigLoader()