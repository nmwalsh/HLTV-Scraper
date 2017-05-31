from getMatchIDs import getMatchIDs
import csv


def tabulate(csvFile, array):
    # Files must be in the csv directory inside the project folder
    with open("csv/%s.csv" % (csvFile), 'a', encoding='utf-8') as f:
        print(f)
        writer = csv.writer(f, delimiter=',')
        print(writer)
        for i in range(0, len(array)):
            writer.writerow(array[i])
    return True


# Make an array of existing Match IDs
existingMatchIDS = []
# Read the existing CSV file and add all of the IDs to an array
with open('csv/matchIDs.csv', encoding='utf-8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        existingMatchIDS.append(row[0])

# Get the last ID so we know when to stop looking
newMatchIDs = getMatchIDs(existingMatchIDS[len(existingMatchIDS)-1])
# Tell teh use how many matches we will tabulate
print("%s new matches to tabulate" % (len(newMatchIDs)))
print(newMatchIDs)


# Step 1: add to matches.csv
# tabulate("matchIDs", newMatchIDs)


# To call tabulate
# fields = [["a1", "2b", "3c"], ["4d", "e6", "f5"], ["8g", "9h", "7i"]]
# tabulate("name", fields)
