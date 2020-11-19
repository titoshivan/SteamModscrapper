import smtplib, ssl, json
#
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
#
#with open('mailproperties.json') as f:
with open('properties_valid.json') as f:
  properties = json.load(f)
#
port = int(properties["port"])  # For SSL
smtp_server = properties["smtp"]
password = properties["password"]
context = ssl.create_default_context()
sender_email = properties["account"]
subject = "Hilos detectados"
context = ssl.create_default_context()
bodyHeader = "The following threads have been detected by the Steam Automod: \n"
#

#Loading server 
def sendReport (receiver, content):
    try: 
        print("·······ENVIANDO MAIL············")
        print("De  : "+sender_email)
        print("Para: "+ receiver)
        print("Asunto: " + subject)
        print('Contenido:'+ content)
        #
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver
        msg['Subject'] = 'Threads detected'
        body = bodyHeader + content
        msg.attach(MIMEText(body,'plain'))
        text = msg.as_string()
        #
        #Formateamos el cuerpo del correo:
        #TODO give proper format to mail from/to/subject/content
        server = smtplib.SMTP_SSL(smtp_server, port, context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver, text)
    except Exception as ex:
        print("Exception: "+str(ex))

