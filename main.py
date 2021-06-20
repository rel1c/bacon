import pickledb
import sys
import wikipediaapi

from collections import deque

# English Wikipedia pages
wiki = wikipediaapi.Wikipedia('en') #TODO put in __init__ file

def main():

    # Check for correct number of arguments
    if 2 < len(sys.argv) or len(sys.argv) < 2:
        print('Usage: %s <url>' % (sys.argv[0]))
        return -1

    # Check entered URL is a valid Wikipedia page
    url = sys.argv[1]
    if not url.startswith('https://en.wikipedia.org/wiki/'):
        print('Invalid URL, must be Wikipedia article')
        return -1

    # Extract topic from URL and check if it has a Wikipedia article
    topic = url.removeprefix('https://en.wikipedia.org/wiki/')
    source = wiki.page(topic)
    if not source.exists():
        print('Invalid URL, must be Wikipedia article')
        return -1

    #TODO Check for connection, webpage request errors

    # Initialize target and database
    target = wiki.page('Kevin Bacon')
    db = pickledb.load('bacon.db', True) #Auto-dump = True
    db.dump #--DEBUG

    # Build link table
    Q = deque()
    maxdepth = 2
    Q.append((target, 0))
    d = 0
    print('Value of d: %d' % d) #--DEBUG
    while d < maxdepth:
        (page, depth) = Q.popleft()
        if depth > d:
            d = depth
        links = page.backlinks
        for title, link in links.items():
            if not db.exists(title):
                Q.append((link, d+1))
                db.set(title, d)
    #print('Size of link table: %d' % len(G))
    print('Entries in database: %d' % len(db.getall()))
    db.dump()

if __name__ == '__main__':
    main()
