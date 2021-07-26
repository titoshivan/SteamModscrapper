import requests
import json
#with open('slackproperties.json') as f:  #Right properties file for release
with open('slackproperties_valid.json') as f: #For dev purposes remove for release
  slackProperties = json.load(f)
#
#--------------------------
def post_message(text, blocks = None):
    return requests.post('https://slack.com/api/chat.postMessage', {
        'token': slackProperties["slack_token"],
        'channel': slackProperties["slack_channel"],
        'text': text,
        'icon_emoji': slackProperties["slack_icon_emoji"],
        'username': slackProperties["slack_user_name"],
        'as_user': True,
        'blocks': json.dumps(blocks) if blocks else None
    }).json()
#--------------------------
#post_message_to_slack('Prueba \n http://www.google.com')