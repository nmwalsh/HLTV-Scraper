from html import getHTML
import re
from datetime import datetime


def getMatchInfo(matchID):
    html = getHTML("https://www.hltv.org/matches/%s" % (matchID))
    # Search variables data-unix="
    date = re.findall('data-unix=\".*\"', html)
    teamIDs = re.findall('src=\"https://static.hltv.org/images/team/logo/.*\" class', html)
    teamNames = re.findall('class=\"logo\" title=\".*\">', html)
    map = re.findall('<div class=\"mapname\">.*</div>', html)
    scores = re.findall('<div class=\"results\"><span class=\".*</span><span>', html)

    # Give up if no team names found
    if len(teamNames) < 1:
        return True

    # Find the match date
    if len(date) > 0:
        date[0] = (date[0].replace("data-unix=\"", "")).replace("\"", "")[:-3]
        date[0] = datetime.utcfromtimestamp(int(date[0])).strftime('%Y-%m-%d')
    else:
        date.append(0)

    # Find the Teams respective IDs
    if len(teamIDs) > 0:
        teamIDs[0] = (teamIDs[0].replace("src=\"https://static.hltv.org/images/team/logo/", "")).replace("\" class", "")
        teamIDs[1] = (teamIDs[1].replace("src=\"https://static.hltv.org/images/team/logo/", "")).replace("\" class", "")
    else:
        teamIDs.append(0)

    # Fidn the map(s) that the match was played on
    if len(map) == 1:
        map[0] = (map[0].replace("<div class=\"mapname\">", "")).replace("</div>", "")
    elif len(map) > 1:
        for i in range(0, len(map)):
            map[i] = (map[i].replace("<div class=\"mapname\">", "")).replace("</div>", "")
    else:
        map.append(0)

    # Find the team starding and half sides
    sides = []
    if len(scores) == 1:
        if re.findall('\"t\"|\"ct\"', scores[0])[0] == '\"t\"':
            sides.append("T")
            sides.append("CT")
        else:
            sides.append("CT")
            sides.append("T")
    elif len(scores) > 1:
        for i in range(0, len(scores)):
            if re.findall('\"t\"|\"ct\"', scores[i])[0] == "\"t\"":
                sides.append("T")
                sides.append("CT")
            else:
                sides.append("CT")
                sides.append("T")
    else:
        return True

    # Find the scores if there is only one map
    if len(map) == 1:
        scores[0] = re.findall('\d+', scores[0])
    # Find the scores if there are multiple maps
    elif len(map) > 1:
        for i in range(0, len(scores)):
            scores[i] = re.findall('\d+', scores[i])
    else:
        scores.append(0)

    for i in range(0, len(scores)):
        # If there was no overtime, make the OT value 0
        if len(scores[i]) == 6:
            scores[i].append(0)
            scores[i].append(0)
        elif len(scores[i]) > 6:
            # Do nothing, because OT scores are already calculated
            pass
        else:
            print("HLTV altered score layout for %s" % (matchID))
            return True

    # Add results to arrays so we can access them from the scrape() method
    result = []
    if len(map) > 1:
        for i in range(0, len(scores)):
            # Create a temp array so that each map's stats are each contained in their own array
            tempArray = []
            tempArray.append(date[0])
            tempArray.append(map[i])
            tempArray.append(teamIDs[0])
            tempArray.append(sides[0])
            tempArray.append(scores[i][0])
            tempArray.append(scores[i][2])
            tempArray.append(scores[i][4])
            tempArray.append(scores[i][6])
            tempArray.append(teamIDs[1])
            tempArray.append(sides[1])
            tempArray.append(scores[i][1])
            tempArray.append(scores[i][3])
            tempArray.append(scores[i][5])
            tempArray.append(scores[i][7])
            tempArray.append(matchID)
            result.append(tempArray)
    else:
        result.append(date[0])
        result.append(map[0])
        result.append(teamIDs[0])
        result.append(sides[0])
        result.append(scores[0][0])
        result.append(scores[0][2])
        result.append(scores[0][4])
        result.append(scores[0][6])
        result.append(teamIDs[1])
        result.append(sides[1])
        result.append(scores[0][1])
        result.append(scores[0][3])
        result.append(scores[0][5])
        result.append(scores[0][7])
        result.append(matchID)
    return result
