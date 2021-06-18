import sys
import wikipediaapi

from collections import deque

# English Wikipedia pages
wiki = wikipediaapi.Wikipedia('en') #TODO put in __init__ file

def bfs(tree, target, seen):
    page = tree.popleft()
    if page.title == target.title:
        return True
    links = page.links
    for title, link in links.items():
        if title not in seen:
            seen[title] = link
            tree.append(link)
    return False

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

    # Initialize search "trees"
    '''
    target = wiki.page('Kevin Bacon')
    tree_bot = dict()
    tree_top = dict()
    tree_bot[target.title] = target
    tree_top[source.title] = source
    print(tree_bot)
    print(tree_top)
    '''

    target = wiki.page('Kevin Bacon')
    tree = deque()
    tree.append(source)
    n = 0
    seen = dict()
    found = bfs(tree, target, seen)
    while not found:
        #print('Examined %d nodes' % n)
        found = bfs(tree, target, seen)
        print('Number of active nodes %d' % len(tree))
        n += 1
    print('Found after examining %d nodes' % (n))

if __name__ == '__main__':
    main()
