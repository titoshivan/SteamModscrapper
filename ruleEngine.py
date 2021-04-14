import json
with open('rules.json') as f:
  ruleset = json.load(f)
#
def checkTitleRule(ruleString, titleString):
  titleRuleFound = False
  if ruleString != "":
    if ruleString in titleString:
      titleRuleFound = True
  return titleRuleFound
#
def checkThreadOP(nameString, OPString):
  threadOPFound = False
  if nameString != "":
    if nameString in OPString:
      threadOPFound = True
  return threadOPFound
#
def runRulesEngine(threadObject, properties):
    ruleFound = False
    debugMode = properties["debug"]
    threadTitle = threadObject.find(class_='forum_topic_name')
    threadTitleUPPER = str(threadTitle.text.strip())
    threadOP = threadObject.find(class_="forum_topic_op")
    threadoOPUpper = str(threadOP.text.strip())
    #we iterate the rules over the forum thread
    #TODO make subject and poster match iterable (Positive if 'string1' or 'string2' or 'string3' in thread title )
    for rule in ruleset:
        if (not ruleFound):

            if debugMode > 0:
              print("         ###### Rule Check: " + rule["rulename"])

            # IF rule 1 applies (rule not null) AND rule 2 applies (rule not null) THEN Return rule 1 found AND rule2found
            # ELSE (only 1 rule applies) THEN return (rule 1 applies AND rule 1 found) OR (rule 2 applies and rule 2 found)
            if  rule["SubjectString"] != "" and rule["username"] != "": #If both rules need to apply
              if  checkTitleRule(rule["SubjectString"], threadTitleUPPER.upper()) and checkThreadOP(rule["username"], threadoOPUpper.upper()):
                ruleFound = True

                if debugMode > 0:
                  print ("Se cumplen ambas reglas" + str(ruleFound))

            else:
              if rule["SubjectString"] != "": #Else If the subject needs to be checked
                ruleFound = checkTitleRule(rule["SubjectString"], threadTitleUPPER.upper())

                if debugMode > 0:
                  print ("Titulo coincide: " + str(ruleFound))

              else:
                if rule["username"] != "": #Or the username
                  ruleFound = checkThreadOP(rule["username"], threadoOPUpper.upper())

                  if debugMode > 0:
                    print ("OP coincide: " + str(ruleFound))
                    
              #if we had a null rule we'd return false
    return ruleFound