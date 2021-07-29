#TODO actually login in Steam
#TODO launch delete/ban on positive.
import requests, time, json, datetime
from bs4 import BeautifulSoup
import emailReport, ruleEngine, logging, slackReport, formatter

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
          #TODO properly Sanitize data entry to avoid screwing JSON formatting
          threadURL = str(each.find('a', href=True)['href'])
          threadOP = str(each.find(class_="forum_topic_op").text.strip())
          threadTitle = str(each.find(class_='forum_topic_name').text.strip()).replace("\r\n"," ").replace("\t","").replace("\"","")

          logging.info(str(datetime.datetime.utcnow()) + " scanning page "+str(pagecount)+" ----> thread "+ threadTitle+ " by " +threadOP)

          matchFound = ruleEngine.runRulesEngine(each, properties)

          if matchFound :

              logging.info(str(datetime.datetime.utcnow()) + ' MATCHING THREAD FOUND !!! ---->' + threadTitle)
              #formatting the report
              reportContent = formatter.formatReport(reportContent, threadTitle, threadOP, threadURL, properties["Report_Channel"] )

      time.sleep(ScanTimer)
      
if reportContent != '':
    #TODO make sending report its own method
    if properties["Report_Channel"] == 'Email':
      emailReport.sendReport(receiver_email, reportContent)
    if properties["Report_Channel"] == 'Slack':
      logging.info(str(datetime.datetime.utcnow()) + "Posting message result" + str(slackReport.post_message(reportContent)))
      #print(slackReport.post_message(reportContent))