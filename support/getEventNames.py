from html import getHTML
import re


def getEventNames(eventID):
    html = getHTML("https://www.hltv.org/results?offset=0&event=%s" % (eventID))
    # Find the type of event (online, LAN, etc)
    eventType = re.findall(' <div class=\".*text-ellipsis\">', html)
    if len(eventType) < 1:
        return True
    eventNames = re.findall('text-ellipsis\">.*<', html)
    eventEndDate = re.findall('class="standard-headline">.*<', html)

    # print eventType
    if len(eventType) > 0:
        eventType[0] = (eventType[0].replace(" <div class=\"", "")).replace(" text-ellipsis\">", "")
    else:
        eventType.append(0)

    # print eventNames
    if len(eventNames) > 0:
        eventNames[0] = (eventNames[0].replace("text-ellipsis\">", "")).replace("<", "")
    else:
        eventNames.append(0)

    # print eventEndDate
    if len(eventEndDate) > 0:
        eventEndDate[0] = (eventEndDate[0].replace("class=\"standard-headline\">", "")).replace("<", "")
    else:
        eventEndDate.append(0)
    result = []
    result.append(eventType[0])
    result.append(eventNames[0])
    result.append(eventEndDate[0])
    result.append(eventID)
    return result
