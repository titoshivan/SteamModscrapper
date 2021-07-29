#TODO actually login in Steam
#TODO launch delete/ban on positive.
import requests, time, json, datetime
from bs4 import BeautifulSoup
import emailReport, ruleEngine, logging, slackReport

#---Load properties from file----
with open('properties.json') as f:
  properties = json.load(f)
#-- rules now go in the rules.json file
with open('filters.json') as f:
  filters = json.load(f)
#---Load pages to scan----
with open('watchlist.json') as f:
  pages = json.load(f)
#-------------------------

#---Setting up the email---------------
receiver_email = properties["receiver"]
reportContent = ''
ScanTimer = properties["rescantimer"] #Delay between requesting pages
#TODO make the number of pages forum dependent moving it to watchlist.json property
pagesToScan = properties["pages"]+1 #Number of pages to scan in each forum
debugMode = properties["debug"] #Activate verbose mode for debug
#-----------------------------------

#------------setting up logging-----------
logging.basicConfig(filename="steam_mod_log.log", level=logging.INFO)
#-----------------------------------
for URL in pages["URLS"]:
  for pagecount in range(1,pagesToScan):

      page = requests.get(URL+str(pagecount))

      soup = BeautifulSoup(page.content, 'html.parser')

      results = soup.find_all(class_='unread')

      for each in results:
          #TODO Sanitize data entry to avoid screwing JSON formatting
          threadURL = each.find('a', href=True)
          threadTitle = each.find(class_='forum_topic_name')
          threadOP = each.find(class_="forum_topic_op")
          threadTitleUP = str(threadTitle.text.strip()).replace("\r\n"," ").replace("\t","").replace("\"","")

          logging.info(str(datetime.datetime.utcnow()) + " scanning page "+str(pagecount)+" ----> thread "+ threadTitleUP+ " by " +str(threadOP.text.strip()))

          matchFound = ruleEngine.runRulesEngine(each, properties)

          if matchFound :

              logging.info(str(datetime.datetime.utcnow()) + ' MATCHING THREAD FOUND !!! ---->' + threadTitleUP)

              #TODO move formating of positives to it's own module
              #reportContent = reportContent + "Title: \"" + str(threadTitle.text.strip()) + "\"\nBy \"" +str(threadOP.text.strip()) + "\"\n" + str(threadURL['href'] + "\n\n") 
              #
              if properties["Report_Channel"] == 'Email':
                reportContent = reportContent + "Title: \"" + threadTitleUP + "\"\nBy \"" +str(threadOP.text.strip()) + "\"\n" + str(threadURL['href'] + "\n\n") 
              if properties["Report_Channel"] == 'Slack':
                reportContent = reportContent + ',{"type": "section","fields": [{"type": "mrkdwn","text": "*SUBJECT:* '+threadTitleUP+'"}]},{"type": "section","fields": [{"type": "mrkdwn","text": "*URL:* <'+str(threadURL['href'])+'|Link>"},{"type": "mrkdwn","text": "*Posted By:* '+str(threadOP.text.strip())+'"}]},{"type": "divider"}'
      time.sleep(ScanTimer)
      
if reportContent != '':
    #TODO make sending report its own method
    if properties["Report_Channel"] == 'Email':
      emailReport.sendReport(receiver_email, reportContent)
    if properties["Report_Channel"] == 'Slack':
      slackReport.post_message(reportContent)
      #print(slackReport.post_message(reportContent))