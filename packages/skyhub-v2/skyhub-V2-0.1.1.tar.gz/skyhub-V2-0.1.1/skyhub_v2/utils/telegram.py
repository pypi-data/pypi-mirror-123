"""Envia uma menssagem para o chat do telegram quando ocorre um erro no sistema."""
import logging

import requests

from config import settings
from skyhub_v2.logging_config import *

logger = logging.getLogger(__name__)
logger.addHandler(f_handler)


def send_message(message):
    token = settings.secrets.telegram.token
    url = f"{settings.settings.telegram.url}{token}/sendMessage"
    params = {
        "chat_id": "325105532",
        "text": f'<code class="language-python">{message}</code>',
        "parse_mode": "html",
    }

    response = requests.get(url, params=params)

    status = response.status_code

    if status == 200:
        logger.info("Menssagem de erro enviada.")

    else:
        logger.error("A menssagem não foi enviada")
