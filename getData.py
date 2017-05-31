from getMatchIDs import getMatchIDs
from getMatchEvents import getMatchEvents
from multiprocessing.dummy import Pool as ThreadPool
import csv


# Define number of CPU threads to use
threads = 32


def scrape(array, function, threads):
        # Define the number of threads
        pool = ThreadPool(threads)

        # Calls get() and adds the filesize returned each call to an array called filesizes
        result = pool.map(function, array)
        pool.close()
        pool.join()
        return result


# Handle an error where data is not added ta the end of the CSV file.
def addNewLine(file):
    # Add a newline to the end of the file if there is not one
    with open(file, "r+") as f:
        f.seek(0, 2)
        if(f.read() != '\n'):
            f.seek(0, 2)
            f.write('\n')


def tabulate(csvFile, array):
    # Files must be in the csv directory inside the project folder
    # Opens the CSV file
    with open("csv/%s.csv" % (csvFile), 'a', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        # Adds a new line if there is not one present
        addNewLine("csv/%s.csv" % (csvFile))
        # Add the array passed in to the CSV file
        for i in range(0, len(array)):
            writer.writerow(array[i])
        print("Succesfully tabulated %s rows to %s.csv." % (len(array), csvFile))
    return True


def getExistingData(csvFile, rowNum):
    # Add the values in rowNum in csvFile to an array
    array = []
    print("Reading data from %s.csv." % (csvFile))
    with open("csv/%s.csv" % (csvFile), encoding='utf-8') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            array.append(row[rowNum])
    return array


def removeExistingData(existing, new):
    # Remove data we alredy have from the list of new data to parse
    for i in range(1, len(new)):
        if new[i] in existing:
            new.remove(new[i])
    print("%s to add." % (len(new)))
    return new


def unDimension(array, item):
    # Pulls specific items from an multi-dimensional array and returns them to one array
    result = []
    for i in range(0, len(array)):
        result.append(array[i][item])
    return result


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
    tabulate("matchIDs", newMatchIDs)

    # Step 2: add new matches to the event join tabulate
    events = getExistingData("joinMatchEvent", 0)
    matchesToCheck = removeExistingData(events, unDimension(newMatchIDs, 1))
    newEvents = scrape(matchesToCheck, getMatchEvents, threads)
    tabulate("joinMatchEvent", newEvents)

    # TODO Step 3: Add new events to eventIDs.csv
    # TODO Step 4: Update matches.csv
    # TODO Step 5: Update matchLineups.csv
    # TODO Step 6: Update teams.csv
    # TODO Step 7: Update players.csv


# To call tabulate
# fields = [["a1", "2b", "3c"], ["4d", "e6", "f5"], ["8g", "9h", "7i"]]
# tabulate("name", fields)
# 22032
