import json
with open('rules.json') as f:
  ruleset = json.load(f)
def runRulesEngine(threadObject):
    ruleFound = False
    threadTitle = threadObject.find(class_='forum_topic_name')
    threadTitleUPPER = str(threadTitle.text.strip())
    threadOP = threadObject.find(class_="forum_topic_op")
    #iteramos las reglas
    for rule in ruleset:
        if (not ruleFound):
            print("Rule Check: " + rule["rulename"])
            #Check if the thread title contains the searched string
            if rule["SubjectString"] != "" and rule["SubjectString"] in threadTitleUPPER.upper():
                ruleFound = True
    return ruleFound