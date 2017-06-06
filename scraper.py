from html import getHTML
import re
from datetime import datetime
from string import digits


def getEventNames(eventID):
    html = getHTML("https://www.hltv.org/results?offset=0&event=%s" % (eventID))
    if html is None:
        print("Failed for %s" % (eventID))
        return []
    # Find the type of event (online, LAN, etc)
    eventType = re.findall(' <div class=\".*text-ellipsis\">', html)
    if len(eventType) < 1:
        return []
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
    # Make an array for pool.map to process
    result = []
    result.append(eventType[0])
    result.append(eventNames[0])
    result.append(eventEndDate[0])
    result.append(eventID)
    return result


def getMatchEvents(matchID):
    html = getHTML("https://www.hltv.org/matches/%s" % (matchID))
    if html is None:
        print("Failed for %s" % (matchID))
        return []
    # Find the type of event (online, LAN, etc)
    eventName = re.findall('\"/events/.*/', html)
    if len(eventName) < 1:
        print("Failed %s" % (matchID))
        return []

    # print eventType
    if len(eventName) > 1:
        eventName[0] = (eventName[0].replace("\"/events/", "")).split("/", 1)[0]
    else:
        eventName.append(0)

    # Make an array for pool.map to process
    array = []
    array.append(matchID)
    array.append(eventName[0])
    return array


def getTeams(teamID):
    html = getHTML("https://www.hltv.org/team/%s/a" % (teamID))
    if html is None:
        print("Failed for %s" % (teamID))
        return []
    # Find the type of event (online, LAN, etc)
    teamName = re.findall('<div><span class=\"subjectname\">.*</span><br><i', html)
    if len(teamName) < 1:
        return []
    teamCountry = re.findall('fa fa-map-marker\" aria-hidden=\"true\"></i>.*<', html)
    if len(teamCountry) < 1:
        teamCountry = re.findall('fa fa-map-marker\" aria-hidden=\"true\"></i>.*</div>', html)
    if len(teamCountry) < 1:
        return []

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

    # Make an array for pool.map to process
    array = []
    array.append(teamName[0])
    array.append(teamCountry[0])
    array.append(teamID)

    return array


def getMatchInfo(matchID):
    html = getHTML("https://www.hltv.org/matches/%s" % (matchID))
    if html is None:
        print("Failed for %s" % (matchID))
        return []
    # Search variables data-unix="
    date = re.findall('data-unix=\".*\"', html)
    teamIDs = re.findall('src=\"https://static.hltv.org/images/team/logo/.*\" class', html)
    teamNames = re.findall('class=\"logo\" title=\".*\">', html)
    map = re.findall('<div class=\"mapname\">.*</div>', html)
    scores = re.findall('<div class=\"results\"><span class=\".*</span><span>', html)

    # Give up if no team names found
    if len(teamNames) < 1:
        return []

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
        return []

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
            return []

    # Make an array for pool.map to process
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
    if html is None:
        print("Failed for %s" % (matchID))
        return []
    playerIDs = re.findall('<a href=\"/player/.*/', html)

    # Give up if no team names found
    if len(playerIDs) < 1:
        print("%s failed, no players detected" % (matchID))
        return []
    for i in range(0, len(playerIDs)):
        playerIDs[i] = (playerIDs[i].split("/"))[2].split("/")[0]
    # print(playerIDs)c
    # print(playerIDs[0:5] + playerIDs[10:15])

    # Make an array for pool.map to process
    if len(playerIDs) > 15:
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
        return []


def getPlayers(playerID):
    html = getHTML("https://www.hltv.org/player/%s/a" % (playerID))
    if html is None:
        print("Failed for %s" % (playerID))
        return []
    # Find the type of event (online, LAN, etc)
    playerName = re.findall('Complete statistics for.*</a>', html)
    if len(playerName) < 1:
        return []
    playerCountry = re.findall('class=\"flag\" title=\".*\"> ', html)
    if len(playerCountry) < 1:
        return []

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

    # Make an array for pool.map to process
    array = []
    array.append(playerName[0])
    array.append(playerCountry[0])
    array.append(playerID)

    return array


def getPlayerStats(matchID):
    html = getHTML("https://www.hltv.org/matches/%s" % (matchID))
    if html is None:
        print("Failed for %s" % (matchID))
        return []

    # Get maps
    maps = re.findall('<div class=\"stats-content\" id=\".*-content\">', html)
    if len(maps) > 0:
        for i in range(0, len(maps)):
            maps[i] = (maps[i].replace("<div class=\"stats-content\" id=\"", "")).replace("-content\">", "").translate({ord(k): None for k in digits})
        maps.remove(maps[0])
    else:
        print("No player stats for %s" % (matchID))
        return []

    # Get Player IDs
    players = re.findall('href=\"/player/.*/', html)
    if len(players) > 0:
        for i in range(0, len(players)):
            players[i] = (players[i].replace("href=\"/player/", "")).replace("/", "")
    else:
        print("No player IDs for %s" % (matchID))
        return []

    # Find player KDs
    kd = re.findall('<td class=\"kd text-center\">.*</td>', html)
    kills = []
    deaths = []
    if len(kd) > 0:
        for i in range(0, len(kd)):
            kd[i] = (kd[i].replace("<td class=\"kd text-center\">", "")).replace("</td>", "")
            # Clean up the hyphenated numbers
            kills.append(kd[i][0:kd[i].find('-')])
            deaths.append(kd[i][kd[i].find('-')+1:len(kd[i])])
    else:
        print("No player K/D for %s" % (matchID))
        return []
    # Remove unnecessary instances of D
    deaths[:] = [x for x in deaths if x != 'D']
    # Remove unnecessary instances of K
    kills[:] = [x for x in kills if x != 'K']

    # Find player ADR
    adr = re.findall('<td class=\"adr text-center \">.*</td>', html)
    if len(adr) > 0:
        for i in range(0, len(adr)):
            adr[i] = (adr[i].replace("<td class=\"adr text-center \">", "")).replace("</td>", "")
    else:
        print("No player ADR for %s" % (matchID))
        adr = [""] * 70

    # Find player KAST%
    kast = re.findall('<td class=\"kast text-center\">.*</td>', html)
    if len(kast) > 0:
        for i in range(0, len(kast)):
            kast[i] = (kast[i].replace("<td class=\"kast text-center\">", "")).replace("%</td>", "")
    else:
        print("No player KAST ratio for %s" % (matchID))
        kast = [""] * 70

    # Find player rating
    rating = re.findall('<td class=\"rating text-center\">.*</td>', html)
    if len(rating) > 0:
        for i in range(0, len(rating)):
            rating[i] = (rating[i].replace("<td class=\"rating text-center\">", "")).replace("</td>", "")
    else:
        print("No player Rating for %s" % (matchID))
        return []

    # Remove unnecessary instances of 'Rating'
    rating[:] = [x for x in rating if x != 'Rating']

    # Handle array building
    masterArray = []
    for i in range(0, len(maps)):
        # Arrays have data for multiple matches, so this offsets us by the amount to get each map separately
        offset = 10 * (i+1)
        for b in range(0, 5):
            playerArray = []
            playerArray.append(maps[i])
            playerArray.append(players[b+offset])
            playerArray.append(kills[b+offset])
            playerArray.append(deaths[b+offset])
            playerArray.append(adr[b+offset])
            playerArray.append(kast[b+offset])
            playerArray.append(rating[b+offset])
            playerArray.append(matchID)
            masterArray.append(playerArray)
        for b in range(5, 10):
            playerArray = []
            playerArray.append(maps[i])
            playerArray.append(players[b+offset])
            playerArray.append(kills[b+offset])
            playerArray.append(deaths[b+offset])
            playerArray.append(adr[b+offset])
            playerArray.append(kast[b+offset])
            playerArray.append(rating[b+offset])
            playerArray.append(matchID)
            masterArray.append(playerArray)
    return masterArray
