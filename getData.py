from getMatchIDs import getMatchIDs
import csv


# Handle an error where data is not added ta the end of the CSV file.
def addNewLine(file):
    with open(file, "r+") as f:
        f.seek(0, 2)
        if(f.read() != '\n'):
            f.seek(0, 2)
            f.write('\n')


def tabulate(csvFile, array):
    # Files must be in the csv directory inside the project folder
    with open("csv/%s.csv" % (csvFile), 'a', encoding='utf-8') as f:
        print(f)
        writer = csv.writer(f, delimiter=',')
        addNewLine("csv/%s.csv" % (csvFile))
        for i in range(0, len(array)):
            writer.writerow(array[i])
        print("Succesfully wrote %s rows" % (len(array)))
    return True


def getExistingData(csvFile):
    array = []
    with open("csv/%s.csv" % (csvFile), encoding='utf-8') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            array.append(row[1])
    return array


# Make an array of existing Match IDs
existingMatchIDs = getExistingData("matchIDs")

# Get the last ID so we know when to stop looking
newMatchIDs = getMatchIDs(existingMatchIDs[len(existingMatchIDs)-1])
newMatchIDs = newMatchIDs[::-1]
if len(newMatchIDs) < 1:
    print("No new matches found.")
else:
    # Tell teh use how many matches we will tabulate
    print("%s new matches to tabulate" % (len(newMatchIDs)))

    # Step 1: add to matches.csv
    tabulate("matchIDs", newMatchIDs)

    # Step 2: add new matches to the event join tabulate
    newEvents = []
    # tabulate("joinMatchEvent", newEvents)


# To call tabulate
# fields = [["a1", "2b", "3c"], ["4d", "e6", "f5"], ["8g", "9h", "7i"]]
# tabulate("name", fields)
