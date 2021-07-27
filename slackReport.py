import requests, logging, datetime
import json
#with open('slackproperties.json') as f:  #Right properties file for release
with open('slackproperties_valid.json') as f: #For dev purposes remove for release
  slackProperties = json.load(f)
#TODO: Move header and footer to properties
reportHeader = '[{"type": "header","text": {"type": "plain_text","text": "WARNING: Actionable Thread(s) detected","emoji": true}}'
reportfooter = ']'
#--------------------------
def post_message(blocks):
    if blocks:
      reportdata= reportHeader + blocks + reportfooter
      logging.info(str(datetime.datetime.utcnow()) + 'PREPARING JSON: ' + reportdata)
      reportblocks = json.loads(reportdata)
      #reportblocks = json.loads(testblocks)
    else:
      blocks = None
    return requests.post('https://slack.com/api/chat.postMessage', {
        'token': slackProperties["slack_token"],
        'channel': slackProperties["slack_channel"],
        #'text': text,
        'icon_emoji': slackProperties["slack_icon_emoji"],
        'username': slackProperties["slack_user_name"],
        'as_user': True,
        'blocks': json.dumps(reportblocks)  #if blocks else None
    }).json()
#--------------------------
#post_message_to_slack('Prueba \n http://www.google.com')
