from getMatchIDs import getMatchIDs
from scraper import *
from helper import *


# Define number of threads to use
threads = 32
# Set to True to activate tabulation and False to disable it.
tab = True

# Make an array of existing Match IDs
existingMatchIDs = getExistingData("matchIDs", 1)

# Get the last ID so we know when to stop looking
newMatchIDs = getMatchIDs(existingMatchIDs[len(existingMatchIDs)-1])
if len(newMatchIDs) < 1:
    print("No new matches found!")
else:
    # Tell the user how many matches we will tabulate
    print("%s new matches to tabulate" % (len(newMatchIDs)))

    # Step 1: add to matches.csv
    if tab:
        tabulate("matchIDs", newMatchIDs)

    # Step 2: add new matches to the event join table
    events = getExistingData("joinMatchEvent", 0)
    matchesToCheck = removeExistingData(events, unDimension(newMatchIDs, 1))
    newEvents = scrape(matchesToCheck, getMatchEvents, threads)
    if tab:
        tabulate("joinMatchEvent", newEvents)

    # Step 3: Add new events to eventIDs.csv
    eventIDs = getExistingData("eventIDs", 3)
    eventsToCheck = removeExistingData(eventIDs, unDimension(newEvents, 1))
    newEventIDs = scrape(eventsToCheck, getEventNames, threads)
    if len(newEventIDs) < 1:
        print("No new event IDs to add!")
    elif tab:
        tabulate("eventIDs", newEventIDs)

    # Step 4: Update matchResults.csv
    newMatchInfo = scrape(matchesToCheck, getMatchInfo, threads)
    # Sometimes this returns a multi-dimensional array, so we remove it
    newMatchInfo = fixArray(fixArray(fixArray(newMatchInfo, 14), 14), 14)
    if tab:
        tabulate("matchResults", newMatchInfo)

    # Step 5: Update matchLineups.csv
    newMatchLineups = scrape(matchesToCheck, getMatchLineups, threads)
    if tab:
        tabulate("matchLineups", newMatchLineups)

    # Step 6: Update playerStats.csv
    newPlayerStats = scrape(matchesToCheck, getPlayerStats, threads)
    # This returns a single array for each match with all of the player stats, so we un-array it
    newPlayerStats = fixPlayerStats(newPlayerStats)
    if tab:
        tabulate("playerStats", newPlayerStats)

    # Step 7: Update teams.csv
    newTeams = getNewIterableItems("team", findMax("teams", 2))
    newTeams = scrape(newTeams, getTeams, threads)
    if tab:
        tabulate("teams", newTeams)

    # Step 8: Update players.csv
    newPlayers = getNewIterableItems("player", findMax("players", 2))
    newPlayers = scrape(newPlayers, getPlayers, threads)
    if tab:
        tabulate("players", newPlayers)
    print("Completed tabulation for %s new matches, %s new player stats, %s new events, %s new teams, and %s new players." % (len(matchesToCheck), len(newPlayerStats), len(newEventIDs), len(newTeams), len(newPlayers)))
