import logging
import pymsteams
from spaceone.core.connector import BaseConnector
from cloudforet.notification.conf.ms_teams_conf import MS_TEAMS_CONF


__all__ = ['MSTeamsConnector']
_LOGGER = logging.getLogger(__name__)


class MSTeamsConnector(BaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = pymsteams.connectorcard(hookurl=kwargs.get('hookurl'))
        self.card_section = pymsteams.cardsection()
        self.client.summary('Cloudforet MS Teams Notification')

    def get_card_section(self):
        return self.card_section

    def set_title(self, title):
        self.client.title(title)

    def set_section_title(self, title, link):
        _title = pymsteams.formaturl(title, link)
        self.card_section.activityTitle(_title)

    def set_section_sub_title(self, sub_title):
        self.card_section.activitySubtitle(sub_title)

    def set_description(self, description):
        self.card_section.activityText(description)

    def set_tag(self, tag):
        self.card_section.addFact(tag.get('key'), tag.get('value'))

    def set_button(self, buttontext, buttonurl):
        self.card_section.linkButton(buttontext, buttonurl)

    def set_section_color(self, notification_type):
        self.client.color(MS_TEAMS_CONF['attachment_color_map'][notification_type])

    def set_image(self, image_url):
        self.card_section.addImage(image_url)

    def enable_markdown(self):
        self.card_section.enableMarkdown()

    def send(self):
        self.client.addSection(self.card_section)
        self.client.send()
