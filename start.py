from getMatchIDs import getMatchIDs
from scraper import *
from helper import *


# Define number of threads to use
threads = 32

# Make an array of existing Match IDs
existingMatchIDs = getExistingData("matchIDs", 1)

# Get the last ID so we know when to stop looking
newMatchIDs = getMatchIDs(existingMatchIDs[len(existingMatchIDs)-1])
if len(newMatchIDs) < 1:
    print("No new matches found.")
else:
    # Tell teh use how many matches we will tabulate
    print("%s new matches to tabulate" % (len(newMatchIDs)))

    # Step 1: add to matches.csv
    # TODO tabulate("matchIDs", newMatchIDs)

    # Step 2: add new matches to the event join table
    events = getExistingData("joinMatchEvent", 0)
    matchesToCheck = removeExistingData(events, unDimension(newMatchIDs, 1))
    newEvents = scrape(matchesToCheck, getMatchEvents, threads)
    # TODO tabulate("joinMatchEvent", newEvents)

    # Step 3: Add new events to eventIDs.csv
    eventIDs = getExistingData("eventIDs", 3)
    eventsToCheck = removeExistingData(eventIDs, unDimension(newEvents, 1))
    newEventIDs = scrape(eventsToCheck, getEventNames, threads)
    if len(newEventIDs) < 1:
        print("No new event IDs to add!")
    else:
        # TODO tabulate("eventIDs", newEventIDs)
        pass

    # Step 4: Update matchResults.csv
    newMatchInfo = scrape(matchesToCheck, getMatchInfo, threads)
    # Sometimes this returns a multi-dimensional array, so we remove it
    newMatchInfo = fixArray(fixArray(newMatchInfo, 14), 14)
    # TODO tabulate("matchResults", newMatchInfo)

    # Step 5: Update matchLineups.csv
    newMatchLineups = scrape(matchesToCheck, getMatchLineups, threads)
    # TODO: tabulate("matchLineups", newMatchLineups)

    # Step 6: Update teams.csv
    newTeams = getNewIterableItems("team", findMax("teams", 2))
    newTeams = scrape(newTeams, getTeams, threads)
    # TODO tabulate("teams", newTeams)
    # Step 7: Update players.csv
    newPlayers = getNewIterableItems("player", findMax("players", 2))
    newPlayers = scrape(newPlayers, getPlayers, threads)
    # TODO tabulate("players", newPlayers)
    print("Completed tabulation for %s new matches, %s new teams, and %s new players." % (len(matchesToCheck), len(newTeams), len(newPlayers)))
