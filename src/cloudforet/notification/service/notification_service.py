import time
import logging

from spaceone.core import utils
from spaceone.core.service import *
from cloudforet.notification.manager.notification_manager import NotificationManager

_LOGGER = logging.getLogger(__name__)


@authentication_handler
class NotificationService(BaseService):

    def __init__(self, metadata):
        super().__init__(metadata)

    @transaction
    @check_required(['options', 'message', 'notification_type'])
    def dispatch(self, params):
        """
        Args:
            params:
                - options
                - message:
                - notification_type : INFO || ERROR || SUCCESS || WARNING
                - secret_data
        """
        channel_data = params.get('channel_data', {})
        notification_type = params['notification_type']
        message = params['message']
        kwargs = {}

        hookurl = channel_data.get('hookurl')

        noti_mgr: NotificationManager = self.locator.get_manager('NotificationManager')

        noti_mgr.dispatch(hookurl, notification_type, message, **kwargs)
