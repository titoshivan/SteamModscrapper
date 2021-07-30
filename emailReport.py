#TODO give proper format to mail from/to/subject/content
#TODO Make the email fancy with proper HTML and URL tagging

import logging, utils
import smtplib, ssl, json
#
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
#

#
#with open('mailproperties.json') as f:  #Right properties file for release
with open('properties_valid.json') as f: #For dev purposes remove for release
  properties = json.load(f)
#
port = int(properties["port"])  # For SSL
smtp_server = properties["smtp"]
password = properties["password"]
senderName = properties["accountname"]
context = ssl.create_default_context()
sender_email = properties["account"]
subject = "Threads Detected"
context = ssl.create_default_context()
bodyHeader = "The following threads have been detected by the Steam Automod: \n"
#

#Loading server 
def sendReport (receiver, content):
    try: 
        logging.info(utils.getTimestamp() + "SENDING REPORT EMAIL: "+ "From: "+ senderName + ", To: " + receiver + ", Subject: " + subject)
        logging.info(utils.getTimestamp() + 'SENDING REPORT EMAIL: CONTENT: \n')
        logging.info(utils.getTimestamp() + '********************************\n')
        logging.info(utils.getTimestamp() + content)
        logging.info(utils.getTimestamp() + '********************************\n')
        #
        msg = MIMEMultipart()
        msg['From'] = senderName
        msg['To'] = receiver
        msg['Subject'] = subject
        body = bodyHeader + content
        msg.attach(MIMEText(body,'plain'))
        text = msg.as_string()
        #
        #Formatting the mail body:
        server = smtplib.SMTP_SSL(smtp_server, port, context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver, text)
        logging.info(utils.getTimestamp() + ' REPORT EMAIL SENT')
    except Exception as ex:
        logging.error(utils.getTimestamp() +  " REPORT EMAIL SENDMAIL EXCEPTION: "+str(ex))

