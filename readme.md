# HLTV Scraper

## Getting New Matches

This works by scraping several pieces of data from the HLTV webpages. First, it will paginate through the match [results](https://www.hltv.org/results) page and determine which Match IDs are not yet in the database. If there are new IDs to tabulate, it will append them to the `matchIDs.csv` file. 

### Matching Matches to Events

Once these have been added, it compares `matchIDs.csv` to `joinMatchEvent.csv` file. `getMatchEvents.py` will parse new Match IDs to fond their respective Event IDs and append them to the `joinMatchEvent.csv` file. 

## Getting New Events

From there, `getEventNames.py` compares `eventIDs.csv` to `joinMatchEvent.csv` and scrapes the respective event results page to determine various data about the event. The data is then appended to `eventIDs.csv`. 

## Getting Match Results

Once the new events have been accounted for, the script takes the array of new matches and sends them to `getMatchInfo.py` to scrape the necessary information. Since this returns multidimensional arrays for matches with more than one map, the script calls `fixArray()` twice to remove any extra dimensions. The method turns an array like this:

	[[1, 2, 3], [3, 4, 5], [['a', 'b', 'c'], ['c', 'd', 'e']], [5, 6, 7]]
 
 To an array like this:
 
	[[1, 2, 3], [3, 4, 5], [5, 6, 7], ['a', 'b', 'c'], ['c', 'd', 'e']]
 
 After that, it tabulates the new information to matches.csv