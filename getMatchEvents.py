from html import getHTML
import re


def getMatchEvents(matchID):
    html = getHTML("https://www.hltv.org/matches/%s" % (matchID))
    # Find the type of event (online, LAN, etc)
    eventName = re.findall('\"/events/.*/', html)
    if len(eventName) < 1:
        print("Failed %s" % (matchID))
        return None

    # print eventType
    if len(eventName) > 1:
        eventName[0] = (eventName[0].replace("\"/events/", "")).split("/", 1)[0]
    else:
        eventName.append(0)

    array = []
    array.append(matchID)
    array.append(eventName[0])
    return array
