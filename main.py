import sys
import time
import wikipediaapi

from collections import deque

# English Wikipedia pages
wiki = wikipediaapi.Wikipedia('en')

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

    # Initialize target and graph
    target = wiki.page('Kevin Bacon')
    G = dict()
    CF = deque() #Current frontier
    NF = deque() #Next frontier
    maxdepth = 2
    depth = 0
    CF.append(target)
    G[target.title] = depth

    sum_link = 0
    sum_look = 0
    num_link = 0
    num_look = 0

    # Build link table
    while depth < maxdepth:
        print('Depth is %d' % depth)
        print('CF is size %d' % len(CF))
        for page in CF:
            tic_link = time.perf_counter_ns()
            links = page.backlinks
            toc_link = time.perf_counter_ns()
            sum_link += toc_link - tic_link
            num_link += 1
            for title, link in links.items():
                tic_look = time.perf_counter_ns()
                if link not in G:
                    NF.append(link)
                    G[title] = depth
                toc_look = time.perf_counter_ns()
                sum_look += toc_link - tic_link
                num_look += 1
        CF = NF
        NF = deque()
        depth += 1
    print('Entries in database: %d' % len(G))
    print('Average time to request links: %f' % (sum_link / num_link))
    print('Average time to find links in graph: %f' % (sum_look / num_look))

if __name__ == '__main__':
    main()
