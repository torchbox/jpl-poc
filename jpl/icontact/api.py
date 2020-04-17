import requests

from django.conf import settings


class IContactAPI:
    def __init__(self, icontact_settings=None):
        if not icontact_settings:
            icontact_settings = settings.ICONTACT_SETTINGS

        self.url = icontact_settings["url"]
        self.version = icontact_settings["version"]
        self.app_id = icontact_settings["app_id"]
        self.username = icontact_settings["username"]
        self.password = icontact_settings["password"]
        self.campaign_id = icontact_settings["campaign_id"]

    def get_headers(self):
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Api-Version": self.version,
            "Api-AppId": self.app_id,
            "Api-Username": self.username,
            "Api-Password": self.password,
        }

    def create_message(self, message_name, subject, html_body, text_body):
        return requests.post(
            self.url + "messages/",
            headers=self.get_headers(),
            json=[{
                "campaignId": self.campaign_id,
                "messageType": "normal",
                "messageName": message_name,
                "subject": subject,
                "htmlBody": html_body,
                "textBody": text_body,
            }],
        )
