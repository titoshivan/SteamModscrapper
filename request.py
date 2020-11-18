import requests, time, json
from bs4 import BeautifulSoup
#import smtplib, ssl #Moved to emailReport.py
import emailReport, ruleEngine 
#todo actually login in Steam
#todo launch delete/ban on positive.
#
#---Load properties from file----
with open('properties.json') as f:
  properties = json.load(f)
#---Load filter chains DEPRECATED
#-- rules now go in the rules.json file
with open('filters.json') as f:
  filters = json.load(f)
#-------------------------

#---Setting up the email---------------
port = int(properties["port"])  # For SSL
smtp_server = properties["smtp"]
password = properties["password"]
#context = ssl.create_default_context()
sender_email = properties["account"]
receiver_email = properties["receiver"]
#TODO Make the email fancy with proper HTML and URL tagging
#TODO Pull mail sending to its own module
message = '''\\
     ... From: titodronedev@gmail.com
     ... Subject: Actionable thread detected in Scan'...
     ... '''
emailcontent = ''
ScanTimer = properties["rescantimer"] #Delay between requesting pages
#-----------------------------------

for pagecount in range(1,3):
    #print('Checqueando pagina '+str(pagecount))
    #TODO iterate URLS stored in watchlist.json
    URL = 'https://steamcommunity.com/discussions/forum/29/?fp='
    page = requests.get(URL+str(pagecount))

    soup = BeautifulSoup(page.content, 'html.parser')

    results = soup.find_all(class_='unread')

    for each in results:
        threadURL = each.find('a', href=True)
        threadTitle = each.find(class_='forum_topic_name')
        threadOP = each.find(class_="forum_topic_op")
        threadTitleUP = str(threadTitle.text.strip())
        print("scanning page "+str(pagecount)+" thread "+ threadTitleUP+ " by " +str(threadOP.text.strip()))
        #TODO Here we should have a proper rules engine.
        # x= item in threadTitleUP.upper()
        x = ruleEngine.runRulesEngine(each)
        #print(ruleEngine.runRulesEngine(each))
        #print('chequeando positivo')
        if x :
            print('hilo coincidente')
            #print(threadURL['href'], end=' subject: ')
            #print(threadTitle.text.strip(), end=' By: ')
            #print(threadOP.text.strip())
            emailcontent = emailcontent + str(threadURL['href']) + " " + str(threadTitle.text.strip()) + " by " +str(threadOP.text.strip()) + "\n"
    time.sleep(ScanTimer)
    #
if emailcontent != '':
    emailReport.sendReport(receiver_email, emailcontent)