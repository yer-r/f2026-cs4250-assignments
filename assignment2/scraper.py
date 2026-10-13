#-------------------------------------------------------------------------
# AUTHOR: Eric Kim
# FILENAME: scraper.py
# SPECIFICATION: this is a crawler for the Circular Link section from testingurl.dev. It starts from seed url and then retrieve each page
#                  through a request, and then parses it with beautifulsoup. after that it should print the text of element <h1>
#                   and it should follow hyperlinks where the url only begins with testingurl.dev.
# FOR: CS 4250 - Assignment #2
# TIME SPENT: about 5 hours total (3 in one day, 2 another)
#-------------------------------------------------------------------------

# Importing Python libraries
import requests
from bs4 import BeautifulSoup

# Defining the seed URL
seed = "https://testingurl.dev/scraping/links/circular"
baseURL = "https://testingurl.dev"

# Creating the frontier and seen collections
frontier = [seed]
seen = {seed}

# Crawling until the frontier is empty
while frontier:

    # Removing the first URL from the frontier
    url = frontier.pop(0)

    # Retrieving and parsing the Web page
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Printing the text contained in the <h1> element
    h1 = soup.find("h1")
    if h1 is not None:
        print(h1.get_text(strip=True))

    # Extracting and processing hyperlinks
    for a in soup.find_all("a", href=True):
        link = a["href"]

        # Converting relative URLs to absolute URLs
        if link.startswith("/"):
            link = baseURL + link

        # Ignoring links outside the Circular Links section
        if not link.startswith(seed):
            continue

        # Adding each new link to seen and the frontier
        if link not in seen:
            seen.add(link)
            frontier.append(link)

# Printing all URLs in seen
for link in sorted(seen):
    print(link)