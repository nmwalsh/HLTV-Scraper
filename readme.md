# HLTV Scraper

This is a Python scraper designed to pull data from HLTV.org and tabulate it into a series of CSV files. It is written in pure Python, so it should run on any system that can run Python 3. It is not compatible with Python 2, so you may need to install the latest Python release from [here](https://www.python.org/downloads/).

{{TOC}}

## Installation

Since this is written in pure Python, there are no dependencies to install. Simply clone the repository or download the zip file, then `cd` to the directory and run `python3 start.py`. There is demonstration [here](https://twitter.com/rxcs/status/870564131715162112).

![](https://i.imgur.com/g5Wk3eS.png)

## Getting New Matches

This works by scraping several pieces of data from the HLTV webpages. First, it will paginate through the match [results](https://www.hltv.org/results) page and determine which Match IDs are not yet in the database. If there are new IDs to tabulate, it will append them to the `matchIDs.csv` file. These new matches are stored in an array called `matchesToCheck`.

### Matching Matches to Events

Once these have been added, it compares `matchIDs.csv` to `joinMatchEvent.csv` file. `getMatchEvents.py` will parse `matchesToCheck` to find their respective Event IDs and append them to the `joinMatchEvent.csv` file. 

## Getting New Events

From there, `getEventNames.py` compares `eventIDs.csv` to `joinMatchEvent.csv` and scrapes the respective event results page to determine various data about the event. The data is then appended to `eventIDs.csv`. 

## Getting Match Results

Once the new events have been accounted for, the script takes `matchesToCheck` and sends them to `getMatchInfo.py` to scrape the necessary information.

### Handling Multiple Maps

Since this returns multidimensional arrays for matches with more than one map, the script calls `fixArray()` twice to remove any extra dimensions. The method turns an array like this:

	[[1, 2, 3], [3, 4, 5], [['a', 'b', 'c'], ['c', 'd', 'e']], [5, 6, 7]]
 
 To an array like this:
 
	[[1, 2, 3], [3, 4, 5], [5, 6, 7], ['a', 'b', 'c'], ['c', 'd', 'e']]
 
 After that, it tabulates the new information to `matchResults.csv`.
 
## Getting Match Lineups 

Next, the script parses the same new matches stored in `MatchesToCheck` and find the respective team lineups and tabulates the new information to `matchLineups.csv`.

## Updating Players and Teams

Each player and team on HLTV has a unique identification number that increases as new players are added to the database. To find new players and teams, we get the maximum identifier value form the respective `.csv` file and iterate over it using `getIterableItems`. From there the relevant pages are scraped and tabulated to `players.csv` and `teams.csv`.