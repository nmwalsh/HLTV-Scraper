from urllib.request import Request, urlopen
import re
import multiprocessing


print("Initialized getMatchIDs")


def getMatchIDs(stop):
    # Create an offset variable for lists that are paginated on HLTV
    offset = 0

    # Create an array of all of the Demo URLs on the page
    matchIDs = findMatchIDsAtURL("https://www.hltv.org/results?offset=%s" % (offset))

    # Determien if we need to paginate and createa  varibale to keep track of pages
    morePages = endCheck(matchIDs, stop)
    page = 1
    while morePages:
        # Offset by 100 to get the next 100 matches
        offset += 100

        moreMatchIDs = findMatchIDsAtURL("https://www.hltv.org/results?offset=%s" % (offset))
        # Append the new IDs to the master list
        for m in moreMatchIDs:
            matchIDs.append(m)
        # Continue paginating adn updating the user
        page += 1
        print("Parsed page %s. %s IDs found so far." % (page, len(matchIDs)))
        morePages = endCheck(matchIDs, stop)

    if len(matchIDs) > 100:
        print("HLTV altered results page layout or offset %s" % (offset))
    # Determines where to stop the array
    slice = matchIDs.index(stop)
    # Remove unecessary entries
    matchIDs = matchIDs[:slice]
    # Adds the unique match identifier as an aray to each item
    for i in range(0, len(matchIDs)):
        string = matchIDs[i]
        split = string.split("/", 1)[0:1]
        split.append(string)
        matchIDs[i] = split
    # Reverse the array so the most recent match is last
    matchIDs = matchIDs[::-1]
    print("Parsed %s page(s)." % (page))
    return matchIDs


def endCheck(matchIDs, stop):
    if stop in matchIDs:
        return False
    return True


def findMatchIDsAtURL(url):
    # Get the HTML using getHTML()
    html = getHTML(url)

    # Create an array of all of the Match URLs on the page
    matchIDs = re.findall('"(.*?000"><a href="/matches/.*?)"', html)

    # Loop through the messy array and removes the pesky parts
    for i in range(0, len(matchIDs)):
        matchIDs[i] = matchIDs[i].split('/', 2)[-1]
    return matchIDs


def getHTML(url):
    # Open the URL
    # Spoof the user agent
    request = Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0')
    # Read the response as HTML
    html = urlopen(request).read().decode('ascii', 'ignore')
    return html


threads = multiprocessing.cpu_count()
# matchIDs = getMatchIDs()
# for i in range(0, len(matchIDs)):
#     print(matchIDs[i])
