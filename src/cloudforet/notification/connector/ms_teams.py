import json
import logging

import requests
from spaceone.core.connector import BaseConnector

__all__ = ['MSTeamsConnector']
_LOGGER = logging.getLogger(__name__)


class MSTeamsConnector(BaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hookurl = kwargs.get('hookurl')
        self.headers = {'Content-Type': 'application/json'}

    def send(self, adaptive_card):
        try:
            res = requests.post(
                self.hookurl,
                data=json.dumps(adaptive_card),
                headers=self.headers,
                timeout=60
            )

            if 200 <= res.status_code < 300:
                return True

            _LOGGER.error(f"Failed to send Teams webhook: {res.status_code} {res.text}")
            res.raise_for_status()

        except requests.exceptions.RequestException as e:
            _LOGGER.error(f"Exception when sending Teams webhook: {e}")
            raise

        return False