import queue
import sys
import threading
import wikipediaapi

# English Wikipedia pages
WIKI = wikipediaapi.Wikipedia('en')
ADDR = 'https://en.wikipedia.org/wiki/'

# Number of search threads to run
NUM_THREADS = 16

# Signal for killing working threads
KILL_SIG = threading.Event()

def bfs_worker(q, target):
    '''Performs breadth first search on nodes in a queue for a given target.
    Nodes representing Wikipedia pages are tuples containing a page title
    string and their depth from the root node. Once the target has been
    found its depth from the root node is displayed and the process (and
    all running threads for the process) is terminated.'''
    while True:

        # Skip loop iteration if no pages to process
        if KILL_SIG.is_set():
            return
        elif q.empty():
            continue

        # Check if page title in queue is target
        (title, depth) = q.get()
        if title == target:
            KILL_SIG.set()
            print(depth)
            return

        # Find links for page
        page = WIKI.page(title)
        try:
            links = page.links
        except: #in case request errors, requeue the page
            q.put((page, depth))
            continue

        # Add page links to queue to be processed
        for link in links.values():
            if link.namespace == wikipediaapi.Namespace.MAIN:
                q.put((link.title, depth+1))
            if KILL_SIG.is_set():
                return

        # If no links and queue is empty, end search
        if q.empty():
            KILL_SIG.set()
            print(-1)
            return

def check_url(url):
    '''Checks if given url starts with Wikipedia prefix.'''
    return url.startswith(ADDR)

def get_page_title(url):
    '''Returns a page title for a given Wikipedia url. Returns None if no such
    page exists.'''
    title = url.removeprefix(ADDR)
    source = WIKI.page(title)
    if source.exists():
        return title
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
    title = get_page_title(url)
    if not title:
        print('Invalid URL, not an existing Wikipedia article')
        return 1

    # Initialize target and graph
    target = WIKI.page('Kevin Bacon')
    q = queue.Queue(maxsize=0)
    q.put((title, 0))

    # Start worker threads
    num_threads = NUM_THREADS
    workers = []
    for i in range(num_threads):
        worker = threading.Thread(target=bfs_worker, args=(q, target.title))
        worker.start()
        workers.append(worker)

    # Block until workers are complete
    for worker in workers:
        worker.join()

if __name__ == '__main__':
    main()
