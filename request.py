import requests, time, json
from bs4 import BeautifulSoup
import emailReport, ruleEngine 
#todo actually login in Steam
#todo launch delete/ban on positive.
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
#TODO Make the email fancy with proper HTML and URL tagging
#TODO Pull mail sending to its own module
emailcontent = ''
ScanTimer = properties["rescantimer"] #Delay between requesting pages
#TODO make the number of pages forum dependent moving it to watchlist.json property
pagesToScan = properties["pages"]+1 #Number of pages to scan in each forum
debugMode = properties["debug"] #Activate verbose mode for debug
#-----------------------------------

for URL in pages["URLS"]:
  for pagecount in range(1,pagesToScan):
      #print('Checqueando pagina '+str(pagecount))
      #TODO iterate URLS stored in watchlist.json
      #URL = 'https://steamcommunity.com/discussions/forum/29/?fp='
      #URL = i
      #print(URL)
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
          #TODO Here we should have a proper rules engine.
          # x= item in threadTitleUP.upper()
          matchFound = ruleEngine.runRulesEngine(each, properties)
          #print(ruleEngine.runRulesEngine(each))
          #print('chequeando positivo')
          if matchFound :
              if debugMode >0:
                  print('hilo coincidente')
              #print(threadURL['href'], end=' subject: ')
              #print(threadTitle.text.strip(), end=' By: ')
              #print(threadOP.text.strip())
              #TODO move formating of positives to it's own module
              emailcontent = emailcontent + "Title: \"" + str(threadTitle.text.strip()) + "\"\nBy \"" +str(threadOP.text.strip()) + "\"\n" + str(threadURL['href'] + "\n\n") 
      time.sleep(ScanTimer)
      #
if emailcontent != '':
    emailReport.sendReport(receiver_email, emailcontent)