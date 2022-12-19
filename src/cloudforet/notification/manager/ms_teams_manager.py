from spaceone.core.manager import BaseManager
from cloudforet.notification.connector.ms_teams import MSTeamsConnector


class MSTeamsManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn = None

    def set_connector(self, hookurl):
        self.conn: MSTeamsConnector = self.locator.get_connector('MSTeamsConnector', hookurl=hookurl)

    def make_card_section(self, notification_type, message):
        title = message['title']
        sub_title = message.get('occurred_at', None)
        link = message.get('link', None)
        description = f"{message.get('description', None)}"
        tags = message.get('tags', [])
        callbacks = message.get('callbacks', [])
        content_type = message.get('content_type', None)

        # want to use markdown
        if contents := message.get('contents') and content_type == 'MARKDOWN':
            self.conn.enable_markdown()
            description = contents

        self.conn.set_title(title)
        self.conn.set_section_title(title, link)
        self.conn.set_section_sub_title(sub_title)
        self.conn.set_description(description)
        self._make_add_fact_from_tags(tags)
        self.conn.set_section_color(notification_type)
        self._make_button_from_callbacks(callbacks)

        if image_url := message.get('image_url'):
            self.conn.set_image(image_url)

    def _make_button_from_callbacks(self, callbacks):
        for callback in callbacks:
            buttontext = callback['label']
            buttonurl = callback['url']
            self.conn.set_button(buttontext, buttonurl)

    def _make_add_fact_from_tags(self, tags):
        for tag in tags:
            self.conn.set_tag(tag)

    def send_message(self):
        self.conn.send()
