from spaceone.core.manager import BaseManager

from cloudforet.notification.connector.ms_teams import MSTeamsConnector


class MSTeamsManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn = None

    def set_connector(self, hookurl):
        self.conn: MSTeamsConnector = self.locator.get_connector('MSTeamsConnector', hookurl=hookurl)

    def make_adaptive_card(self, notification_type, message):
        title = message['title']
        sub_title = message.get('occurred_at', None)
        link = message.get('link', None)
        description = f"{message.get('description', None)}"
        tags = message.get('tags', [])
        callbacks = message.get('callbacks', [])
        content_type = message.get('content_type', None)

        if content_type == "MARKDOWN" and (contents := message.get("contents")):
            description = contents

        formatted_title = self._format_title_with_link(title, link)
        actions = self._make_actions_from_callbacks(callbacks)
        facts = self._make_facts_from_tags(tags)

        body = [
            {
                "type": "TextBlock",
                "size": "Large",
                "weight": "Bolder",
                "text": formatted_title,
                "wrap": True,
            },
            {
                "type": "TextBlock",
                "isSubtle": True,
                "spacing": "None",
                "text": sub_title,
                "wrap": True,
            },
            {
                "type": "TextBlock",
                "text": description,
                "wrap": True,
            },
            {
                "type": "FactSet",
                "facts": facts,
            },
        ]

        if image_url := message.get("image_url"):
            body.append(
                {
                    "type": "Image",
                    "url": image_url,
                    "size": "Auto",
                    "altText": "Image",
                }
            )

        adaptive_card = {
            "type": "message",
            "attachments": [
                {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "contentUrl": None,
                    "content": {
                        "$schema": "https://adaptivecards.io/schemas/adaptive-card.json",
                        "type": "AdaptiveCard",
                        "version": "1.5",
                        "body": body,
                        "actions": actions,
                    },
                }
            ],
        }

        return adaptive_card

    @staticmethod
    def _format_title_with_link(title: str, link: str = None) -> str:
        if link:
            return f"[{title}]({link})"
        return title

    @staticmethod
    def _make_actions_from_callbacks(callbacks):
        actions = []

        for callback in callbacks:
            actions.append(
                {
                    "type": "Action.OpenUrl",
                    "title": callback["label"],
                    "url": callback["url"],
                }
            )

        return actions

    @staticmethod
    def _make_facts_from_tags(tags):
        facts = []

        for tag in tags:
            facts.append({"title": tag.get("key", ""), "value": tag.get("value", "")})

        return facts

    def send_message(self, adaptive_card):
        self.conn.send(adaptive_card)
