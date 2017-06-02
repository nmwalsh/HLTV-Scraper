from html import getHTML
import re
import sys
from datetime import datetime


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


def getMatchLineups(matchID):
    # Set some vars for later
    html = getHTML("https://www.hltv.org/matches/%s" % (matchID))
    playerIDs = re.findall('<a href=\"/player/.*/', html)

    # Give up if no team names found
    if len(playerIDs) < 1:
        print("%s failed, no players detected" % (matchID))
        return True
    for i in range(0, len(playerIDs)):
        playerIDs[i] = (playerIDs[i].split("/"))[2].split("/")[0]
    # print(playerIDs)c
    # print(playerIDs[0:5] + playerIDs[10:15])

    # Handle printing
    if len(playerIDs) > 15:
        # print(matchID)
        players = []
        players.append(playerIDs[0])
        players.append(playerIDs[1])
        players.append(playerIDs[2])
        players.append(playerIDs[3])
        players.append(playerIDs[4])
        players.append(playerIDs[5])
        players.append(playerIDs[6])
        players.append(playerIDs[7])
        players.append(playerIDs[8])
        players.append(playerIDs[9])
        players.append(matchID)
        return players
    else:
        print("HLTV altered lineup layout for %s" % (matchID))
        return None


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
