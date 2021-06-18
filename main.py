import sys
import wikipediaapi

from collections import deque

# English Wikipedia pages
wiki = wikipediaapi.Wikipedia('en') #TODO put in __init__ file

class PageNode(object):

    def __init__(self, page):
        self.page = page
        self.links = []

    def __hash__(self):
        return hash(self.page.title)

    def __eq__(self, other):
        return self.page.title == other.page.title

    def gen_links(self):
        links = self.page.links
        for _, page in links.items():
            self.links.append(PageNode(page))

def search(G, targetNode):
    for node in G:
        if node == targetNode:
            return True
    return False
'''
def idfs(G, targetNode):
    d = 0
    maxdepth = 6
    while d <= maxdepth:
        print('Depth is %d' % d)
        for 
        d += 1
'''
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

    # Initialize target and search graph
    target = wiki.page('Kevin Bacon')
    targetNode = PageNode(target)
    sourceNode = PageNode(source)
    G = [sourceNode]
    found = search(G, targetNode)
    #found = idfs(G, targetNode)
    print(found)

if __name__ == '__main__':
    main()
