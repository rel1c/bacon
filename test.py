import hashlib

# Object representing a Wikipedia page
class Page(object):
    url = ""
    links = []

    # Initialize a page with its URL
    def __init__(self, url):
        self.url = url

    # Returns a hash based on the page's URL
    def __hash__(self):
        return hash(self.url)

    # Display page in console as its URL
    def __repr__(self):
        return self.url

# Object representing a graph of pages
class PageGraph(object):
    pages = dict()

    # Add a page to the graph
    def add_page(self, page):
        self.pages[page] = page

    # Retrieve a page from a graph, returns None if page does not exist
    def get_page(self, page):
        return self.pages.get(page)

def main():
    p1 = Page("https://www.foobar.com")
    p2 = Page("https://www.bazqux.com")
    graph = PageGraph()
    graph.add_page(p1)
    graph.add_page(p2)
    print(graph.get_page(p2))

if __name__ == '__main__':
    main()
