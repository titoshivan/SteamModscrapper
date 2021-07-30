#Report formatting method
def formatReport( title, op, url, channel):
    if channel == 'Email':

        formattedReport =  "Title: \"" + title + "\"\nBy \"" + op + "\"\n" + url + "\n\n"

    if channel == 'Slack':

        formattedReport = ',{"type": "section","fields": [{"type": "mrkdwn","text": "*SUBJECT:* '+title+\
                          '"}]},{"type": "section","fields": [{"type": "mrkdwn","text": "*URL:* <'+ url +\
                          '|Link>"},{"type": "mrkdwn","text": "*Posted By:* '+ op +'"}]},{"type": "divider"}'
    
    return formattedReport