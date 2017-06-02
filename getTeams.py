from html import getHTML
import re


def getTeams(teamID):
    html = getHTML("https://www.hltv.org/team/%s/a" % (teamID))
    # Find the type of event (online, LAN, etc)
    teamName = re.findall('<div><span class=\"subjectname\">.*</span><br><i', html)
    if len(teamName) < 1:
        return True
    teamCountry = re.findall('fa fa-map-marker\" aria-hidden=\"true\"></i>.*<', html)
    if len(teamCountry) < 1:
        teamCountry = re.findall('fa fa-map-marker\" aria-hidden=\"true\"></i>.*</div>', html)
    if len(teamCountry) < 1:
        return True

    # print teamName
    if len(teamName) > 0:
        teamName[0] = (teamName[0].replace("<div><span class=\"subjectname\">", "")).replace("</span><br><i", "")
    else:
        teamName.append(0)

    # print teamCountry
    if len(teamCountry) > 0:
        teamCountry[0] = (teamCountry[0].replace("fa fa-map-marker\" aria-hidden=\"true\"></i> ", "")).split("<", 1)[0]
    else:
        teamCountry.append(0)

    array = []
    array.append(teamName[0])
    array.append(teamCountry[0])
    array.append(teamID)

    return array
