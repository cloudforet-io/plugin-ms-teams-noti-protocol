import logging
from spaceone.core.service import *

_LOGGER = logging.getLogger(__name__)


@authentication_handler
class ProtocolService(BaseService):

    def __init__(self, metadata):
        super().__init__(metadata)

    @check_required(['options'])
    def init(self, params):
        """ init plugin by options
        """
        return {'metadata': {
            'data_type': 'SECRET',
            'data': {
                'schema': {
                    'properties': {
                        'token': {
                            'description': 'Incoming Webhook URL created by your channel',
                            'minLength': 4,
                            'title': 'Incoming Webhook',
                            'type': 'string',
                            'examples': ['https://...']
                        }
                    },
                    'required': [
                        'hookurl'
                    ],
                    'type': 'object'
                }
            }
        }}

    @transaction
    @check_required(['options'])
    def verify(self, params):
        """
        Args:
              params:
                - options
                - secret_data
        """
        options = params['options']
        secret_data = params.get('secret_data', {})

        return {}