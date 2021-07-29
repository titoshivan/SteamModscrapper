#Report formatting method
def formatReport(content, title, op, url, channel):
    if channel == 'Email':
        formattedReport = content + "Title: \"" + title + "\"\nBy \"" + op + "\"\n" + url + "\n\n"
    if channel == 'Slack':
        formattedReport = content + ',{"type": "section","fields": [{"type": "mrkdwn","text": "*SUBJECT:* '+title+\
                          '"}]},{"type": "section","fields": [{"type": "mrkdwn","text": "*URL:* <'+ url +\
                          '|Link>"},{"type": "mrkdwn","text": "*Posted By:* '+ op +'"}]},{"type": "divider"}'
    #
    return formattedReport