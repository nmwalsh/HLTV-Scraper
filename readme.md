# HLTV Scraper

## Getting New Matches

This works by scraping several pieces of data from the HLTV webpages. First, it will paginate through the match [results](https://www.hltv.org/results) page and determine which Match IDs are not yet in the database. If there are new IDs to tabulate, it will append them to the `matchIDs.csv` file. 

### Matching Matches to Events

Once these have been added, it compares `matchIDs.csv` to `joinMatchEvent.csv` file. `getMatchEvents.py` will parse new Match IDs to fond their respective Event IDs and append them to the `joinMatchEvent.csv` file. 

## Getting New Events

From there, `getEventNames.py` compares `eventIDs.csv` to `joinMatchEvent.csv` and scrapes the respective event results page to determine various data about the event. The data is then appended to `eventIDs.csv`. 