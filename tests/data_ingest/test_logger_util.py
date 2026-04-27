import logging

from data_ingest import logger_util as sut

LOGGER_NAME = "test_logger"


def test_logging_output(caplog):
    """Teste para verificar se as mensagens de log estão sendo capturadas corretamente."""
    caplog.set_level(logging.INFO, logger=LOGGER_NAME)

    sut.configure_logging()

    logger = logging.getLogger(LOGGER_NAME)
    logger.info("Mensagem de teste INFO")
    logger.debug("Mensagem de teste DEBUG")

    assert "Mensagem de teste INFO" in caplog.text, "Deve conter a mensagem INFO"
    assert "Mensagem de teste DEBUG" not in caplog.text, "Não deve conter a mensagem DEBUG"
