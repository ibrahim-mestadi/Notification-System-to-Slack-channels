from time import time
from slack_sdk.webhook import WebhookClient


url = "//"

webhook = WebhookClient(url)

import time

def webhookBotScrap(text) :
    
    time.sleep(1)

    try :
        webhook.send (
        text="notif",
        blocks=[
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": text 
            }

        }

    ]
                )
    except :
        time.sleep(5)
        webhookBotScrap(text) 




