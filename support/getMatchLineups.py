from html import getHTML
import re


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
