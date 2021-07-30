import requests, logging, utils
import json
#with open('slackproperties.json') as f:  #Right properties file for release
with open('slackproperties_valid.json') as f: #For dev purposes remove for release
  Properties = json.load(f)
#TODO: Move header and footer to properties
reportHeader = '[{"type": "header","text": {"type": "plain_text","text": "WARNING: Actionable Thread(s) detected","emoji": true}},{"type": "divider"}'
reportfooter = ',{"type": "section","text": {"type": "mrkdwn","text": "*Report Date:* ' + utils.getTimestamp() +' (UTC)"}},{"type": "divider"}]'
#--------------------------
def post_message(blocks):
    reportdata= reportHeader + blocks + reportfooter
    logging.info(utils.getTimestamp() + 'PREPARING JSON: ' + reportdata)
    reportBody = json.loads(reportdata)
    notificationText = Properties["slack_notification_message"]
    #reportBody = json.loads(testblocks)
    return requests.post('https://slack.com/api/chat.postMessage', {
        'token': Properties["slack_token"],
        'channel': Properties["slack_channel"],
        'text' : notificationText,
        'username': Properties["slack_user_name"],
        'as_user': True,
        'unfurl_links': False,
        'blocks': json.dumps(reportBody)
    }).json()
#--------------------------

