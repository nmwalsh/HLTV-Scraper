from helper import scrape, tabulate, getExistingData, removeExistingData, unDimension, fixArray
from getMatchIDs import getMatchIDs
from getMatchEvents import getMatchEvents
from getEventNames import getEventNames
from getMatchInfo import getMatchInfo
from getMatchLineups import getMatchLineups


# Define number of CPU threads to use
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
    newMatchInfo = fixArray(fixArray(newMatchInfo, 14), 14)
    # tabulate("matchResults", newMatchInfo)

    # Step 5: Update matchLineups.csv
    newMatchLineups = scrape(matchesToCheck, getMatchLineups, threads)
    tabulate("matchLineups", newMatchLineups)

    # TODO Step 6: Update teams.csv; rework process(); move to html.py
    # TODO Step 7: Update players.csv; rework process(); move to html.py


# To call tabulate
# fields = [["a1", "2b", "3c"], ["4d", "e6", "f5"], ["8g", "9h", "7i"]]
# tabulate("name", fields)
# 22032
