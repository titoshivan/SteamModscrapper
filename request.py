#TODO actually login in Steam
#TODO launch delete/ban on positive.
#TODO create a log file
import requests, time, json
from bs4 import BeautifulSoup
import emailReport, ruleEngine 

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
emailcontent = ''
ScanTimer = properties["rescantimer"] #Delay between requesting pages
#TODO make the number of pages forum dependent moving it to watchlist.json property
pagesToScan = properties["pages"]+1 #Number of pages to scan in each forum
debugMode = properties["debug"] #Activate verbose mode for debug
#-----------------------------------

for URL in pages["URLS"]:
  for pagecount in range(1,pagesToScan):

      page = requests.get(URL+str(pagecount))

      soup = BeautifulSoup(page.content, 'html.parser')

      results = soup.find_all(class_='unread')

      for each in results:
          threadURL = each.find('a', href=True)
          threadTitle = each.find(class_='forum_topic_name')
          threadOP = each.find(class_="forum_topic_op")
          threadTitleUP = str(threadTitle.text.strip())

          if debugMode > 0:
              print("scanning page "+str(pagecount)+" ----> thread "+ threadTitleUP+ " by " +str(threadOP.text.strip()))

          matchFound = ruleEngine.runRulesEngine(each, properties)

          if matchFound :

              if debugMode >0:
                  print('Matching thread')

              #TODO move formating of positives to it's own module
              emailcontent = emailcontent + "Title: \"" + str(threadTitle.text.strip()) + "\"\nBy \"" +str(threadOP.text.strip()) + "\"\n" + str(threadURL['href'] + "\n\n") 
      time.sleep(ScanTimer)
      
if emailcontent != '':
    emailReport.sendReport(receiver_email, emailcontent)