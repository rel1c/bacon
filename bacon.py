import queue
import sqlite3
import sys
import threading
import wikipediaapi

# Wikipedia address format for English articles
WIKI = wikipediaapi.Wikipedia('en')
ADDR = 'https://en.wikipedia.org/wiki/'

# Number of search threads to run
NUM_THREADS = 16

# Signal for killing working threads
KILL_SIG = threading.Event()

def bfs_worker(currFrontier, nextFrontier):
    '''Performs breadth first search on nodes in a queue for a given target.
    Nodes representing Wikipedia pages are tuples containing a page title
    string and their depth from the root node. Once the target has been
    found, its depth from the root node is displayed and the process (and
    all running threads for the process) is terminated.'''
    while True:

        # Skip loop iteration if no pages to process
        if KILL_SIG.is_set():
            return
        elif nextFrontier.empty():
            continue

        # Find links for page
        (title, depth) = nextFrontier.get()
        page = WIKI.page(title)
        try:
            links = page.links
        except: # in case of request errors, requeue the page
            nextFrontier.put((page, depth))
            continue

        # Add page links to queue to be processed
        for link in links.values():
            if KILL_SIG.is_set():
                return
            if link.namespace == wikipediaapi.Namespace.MAIN:
                currFrontier.put((link.title, depth+1))

        # If no links and queue is empty, end search
        if currFrontier.empty():
            KILL_SIG.set()
            print(-1)

def search_db(currFrontier, nextFrontier, con):
    '''Searches a database of links given by a connection object. If a link in
    the current frontier is found to exist, the function outputs the sum of
    its degrees of separation and the current depth of the frontier.'''
    cur = con.cursor()
    while not KILL_SIG.is_set():
        if currFrontier.empty():
            continue
        # Grab link title in current queue
        (title, depth) = currFrontier.get()
        cur.execute("SELECT depth FROM links WHERE title = ?", (title,))
        result = cur.fetchone()
        # If the title exists in the database, return its depth from the source
        if result:
            rec_depth = result[0]
            KILL_SIG.set()
            print(rec_depth + depth)
        else:
            nextFrontier.put((title, depth))

def check_url(url):
    '''Checks if given url starts with Wikipedia prefix.'''
    return url.startswith(ADDR)

def get_page_title(url):
    '''Returns a page title for a given Wikipedia url. Returns None if no such
    page exists.'''
    title = url.removeprefix(ADDR)
    source = WIKI.page(title)
    if source.exists():
        return source.title
    return None

def main():
    '''This program performs a multi-threaded breadth-first search to find the
    shortest path between a given Wikipedia article and the Wikipedia article
    for actor Kevin Bacon.'''

    # Check for correct number of arguments
    if 2 < len(sys.argv) or len(sys.argv) < 2:
        print('Usage: %s <url>' % (sys.argv[0]))
        return -1

    # Check entered URL is a valid Wikipedia page
    url = sys.argv[1]
    if not check_url(url):
        print('Invalid URL, must start with "%s"' % ADDR)
        return 1
    source = get_page_title(url)
    if not source:
        print('Invalid URL, not an existing Wikipedia article')
        return 1

    # Initialize target and graph
    target = WIKI.page('Kevin Bacon')
    currFrontier = queue.Queue(maxsize=0)
    nextFrontier = queue.Queue(maxsize=0)
    currFrontier.put((source, 0))

    # Open database
    con = sqlite3.connect('links.db')

    # Start worker threads
    num_threads = NUM_THREADS
    workers = []
    for i in range(num_threads):
        worker = threading.Thread(target=bfs_worker, args=(currFrontier, nextFrontier), daemon=True)
        workers.append(worker)
        worker.start()

    # Search database for results from worker threads
    if not KILL_SIG.is_set():
        search_db(currFrontier, nextFrontier, con)

    # Close database
    con.close()

if __name__ == '__main__':
    main()
