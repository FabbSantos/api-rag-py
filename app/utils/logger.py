import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app_log.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("appRag")

if __name__ == "__main__":
    logger.info("Testando o logger")
    logger.warning("Teste aviso")
    logger.error("Teste erro")
    
__all__ = ["logger"]