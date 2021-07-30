import datetime
import time, datetime
#Returns timestamp in string format (for logs)
def getTimestamp():
    return str(datetime.datetime.utcnow())
#
#TODO Improve sanitation of strings
def sanitizeString(stringToSanitize):
    charsToSanitize = ["\r\n","\t","\"","\\"]
    for i in charsToSanitize:
        stringToSanitize = str(stringToSanitize).replace(i,"")
    return stringToSanitize
