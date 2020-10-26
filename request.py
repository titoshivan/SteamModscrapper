import requests, time, json
from bs4 import BeautifulSoup
import smtplib, ssl
#todo add dictionary of keywords
#todo actually login in Steam
#todo launch delete/ban on positive.
#
#---Load properties from file----
with open('properties.json') as f:
  properties = json.load(f)
#-------------------------
#Setting up the email---------------
port = int(properties["port"])  # For SSL
smtp_server = properties["smtp"]
password = properties["password"]
context = ssl.create_default_context()
sender_email = properties["account"]
receiver_email = properties["receiver"]
message = '''\\
     ... From: titodronedev@gmail.com
     ... Subject: Actionable thread detected in Scan'...
     ... '''
emailcontent = ''
ScanTimer = properties["rescantimer"] #Delay between requesting pages
#-----------------------------------

for pagecount in range(1,2):
    #print('Checqueando pagina '+str(pagecount))
    URL = 'https://steamcommunity.com/discussions/forum/29/?fp='
    page = requests.get(URL+str(pagecount))

    soup = BeautifulSoup(page.content, 'html.parser')

    results = soup.find_all(class_='unread')

    for each in results:
        threadURL = each.find('a', href=True)
        threadTitle = each.find(class_='forum_topic_name')
        threadOP = each.find(class_="forum_topic_op")
        threadTitleUP = str(threadTitle.text.strip())
        x= "CSGO" in threadTitleUP.upper()
        #print('chequeando positivo')
        if x :
            print('hilo coincidente')
            print(threadURL['href'], end=' subject: ')
            print(threadTitle.text.strip(), end=' By: ')
            print(threadOP.text.strip())
            if emailcontent == '':
                 emailcontent = message + str(threadURL['href']) + " " + str(threadTitle.text.strip()) + " by " +str(threadOP.text.strip()) + "\n"
            else:
                emailcontent = emailcontent + str(threadURL['href']) + " " + str(threadTitle.text.strip()) + " by " +str(threadOP.text.strip()) + "\n"
    time.sleep(ScanTimer)
    #
if emailcontent != '':
    try: 
        #print('Enviando mail')
        #print('Contenido:'+emailcontent)
        server = smtplib.SMTP_SSL(smtp_server, port, context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, emailcontent.encode('utf-8'))
    except Exception as ex:
        print("Exception: "+str(ex))