import logging

from spaceone.core.manager import BaseManager

from cloudforet.notification.manager.ms_teams_manager import MSTeamsManager

_LOGGER = logging.getLogger(__name__)


class NotificationManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def dispatch(self, hookurl, notification_type, message, **kwargs):
        ms_teams_mgr: MSTeamsManager = self.locator.get_manager('MSTeamsManager')
        ms_teams_mgr.set_connector(hookurl)
        adaptive_card = ms_teams_mgr.make_adaptive_card(notification_type, message)
        ms_teams_mgr.send_message(adaptive_card)
