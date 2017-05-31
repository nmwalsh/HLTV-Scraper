from urllib.request import Request, urlopen
from html import getHTML
import re
import csv
from datetime import datetime
import multiprocessing
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Process, Queue


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

    if len(date) > 0:
        date[0] = (date[0].replace("data-unix=\"", "")).replace("\"", "")[:-3]
        date[0] = datetime.utcfromtimestamp(int(date[0])).strftime('%Y-%m-%d')
    else:
        date.append(0)

    # print teamID
    if len(teamIDs) > 0:
        teamIDs[0] = (teamIDs[0].replace("src=\"https://static.hltv.org/images/team/logo/", "")).replace("\" class", "")
        teamIDs[1] = (teamIDs[1].replace("src=\"https://static.hltv.org/images/team/logo/", "")).replace("\" class", "")
        # print(teamIDs[0] + teamIDs[1])
    else:
        teamIDs.append(0)

    # print map
    if len(map) == 1:
        map[0] = (map[0].replace("<div class=\"mapname\">", "")).replace("</div>", "")
    elif len(map) > 1:
        for i in range(0, len(map)):
            map[i] = (map[i].replace("<div class=\"mapname\">", "")).replace("</div>", "")
    else:
        map.append(0)

    # print scores
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

    if len(map) == 1:
        scores[0] = re.findall('\d+', scores[0])
    elif len(map) > 1:
        for i in range(0, len(scores)):
            scores[i] = re.findall('\d+', scores[i])
    else:
        scores.append(0)

    for i in range(0, len(scores)):
        if len(scores[i]) == 6:
            scores[i].append(0)
            scores[i].append(0)
        elif len(scores[i]) > 6:
            pass
        else:
            return True

    # Handle printing
    result = []
    if len(map) > 1:
        for i in range(0, len(scores)):
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
