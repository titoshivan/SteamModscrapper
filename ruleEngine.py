import json
with open('rules.json') as f:
  ruleset = json.load(f)
#
def checkTitleRule(ruleString, titleString):
  titleRuleFound = False
  if ruleString != "":
    if ruleString in titleString:
      titleRuleFound = True
    print ("         ------- IS " + ruleString + " in " + titleString + "? = " + str(titleRuleFound))
  return titleRuleFound
#
def checkThreadOP(nameString, OPString):
  threadOPFound = False
  if nameString != "":
    if nameString in OPString:
      threadOPFound = True
    print ("         ------- IS" + nameString + " in " + OPString + "? = " + str(threadOPFound))
  return threadOPFound
#
def runRulesEngine(threadObject):
    ruleFound = False
    threadTitle = threadObject.find(class_='forum_topic_name')
    threadTitleUPPER = str(threadTitle.text.strip())
    threadOP = threadObject.find(class_="forum_topic_op")
    threadoOPUpper = str(threadOP.text.strip())
    #iteramos las reglas
    for rule in ruleset:
        if (not ruleFound):
            print("         ###### Rule Check: " + rule["rulename"])
            #Check if the thread title contains the searched string
            #if rule["SubjectString"] != "" and rule["SubjectString"] in threadTitleUPPER.upper():
            #    ruleFound = True
            # TODO proper engine rule: 
            # IF rule 1 applies (rule not null) AND rule 2 applies (rule not null) THEN Return rule 1 found AND rule2found
            # ELSE (only 1 rule applies) THEN return (rule 1 applies AND rule 1 found) OR (rule 2 applies and rule 2 found)
            # For now only one of the matches in the rule needs to apply
            # If checkTitleRule turns TRUE we are NOT even evaluating checkThreadOP now
            ruleFound = checkTitleRule(rule["SubjectString"], threadTitleUPPER.upper()) or checkThreadOP(rule["username"], threadoOPUpper.upper())
    return ruleFound