from multiprocessing.dummy import Pool as ThreadPool
from html import getHTML
import re
import csv
import sys


def scrape(array, function, threads):
        # Define the number of threads
        pool = ThreadPool(threads)

        # Tell the user what is happening
        print("Scraping %s items using %s on %s threads." % (len(array), function, threads))

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


def getExistingData(csvFile, colNum):
    # Add the values in colNum in csvFile to an array
    array = []
    print("Reading data from %s.csv." % (csvFile))
    with open("csv/%s.csv" % (csvFile), encoding='utf-8') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            array.append(row[colNum])
    return array


def findMax(csvFile, colNum):
    array = []
    print("Reading data from %s.csv." % (csvFile))
    with open("csv/%s.csv" % (csvFile), encoding='utf-8') as csvfile:
        next(csvfile)
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            array.append(int(row[colNum]))
    return max(array)


def removeExistingData(existing, new):
    # Remove data we alredy have from the list of new data to parse
    for i in new[:]:
        if i in existing:
            new.remove(i)
    # Convert new values to a set to remove dupelicates, then back to a list
    new = list(set(new))
    print("%s new items to add." % (len(new)))
    return new


def unDimension(array, item):
    # Pulls specific items from an multi-dimensional array and returns them to one array
    result = []
    for i in range(0, len(array)):
        result.append(array[i][item])
    return result


def fixArray(array, value):
    # Used to clean match info results for matches with more than one map
    for i in range(0, len(array)):
        if len(array[i]) < value:
            for b in range(0, len(array[i])):
                array.append(array[i][b])
            array.remove(array[i])
    return array


def getNewIterableItems(page, startID):
    # Iterate through unique IDs until we get the last one, then return them to a list
    print("Checking for new %ss. This may take awhile." % (page))
    check = True
    array = []
    while check:
        startID += 1
        html = getHTML("https://www.hltv.org/%s/%s/a" % (page, startID))
        if len(re.findall('error-desc', html)) > 0:
            check = False
        else:
            print("New %s found: %s" % (page, startID))
            array.append(startID)
    sys.stdout.write('\r'+"Found %s new %ss." % (len(array), page))
    sys.stdout.flush()
    return array
