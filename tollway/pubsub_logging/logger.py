import logging


def get_pubsub_logger(pubsub: bool) -> logging.Logger:
    logger = logging.getLogger("pubsub")
    if pubsub:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            filename="pubsub.log",
            filemode="a",
        )
    else:
        logger.handlers.clear()
        logger.addHandler(logging.NullHandler())
    return logger
