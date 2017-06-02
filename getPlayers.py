from html import getHTML
import re


def getPlayers(playerID):
    html = getHTML("https://www.hltv.org/player/%s/a" % (playerID))
    # Find the type of event (online, LAN, etc)
    playerName = re.findall('Complete statistics for.*</a>', html)
    if len(playerName) < 1:
        return True
    playerCountry = re.findall('class=\"flag\" title=\".*\"> ', html)
    if len(playerCountry) < 1:
        return True

    # print teamName
    if len(playerName) > 0:
        playerName[0] = (playerName[0].replace("Complete statistics for ", "")).replace("</a>", "")
    else:
        playerName.append(0)

    # print teamCountry
    if len(playerCountry) > 0:
        playerCountry[0] = (playerCountry[0].replace("class=\"flag\" title=\"", "")).replace("\"> ", "")
    else:
        playerCountry.append(0)

    array = []
    array.append(playerName[0])
    array.append(playerCountry[0])
    array.append(playerID)

    return array
