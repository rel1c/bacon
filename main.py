import queue
import sys
import wikipediaapi

def main():

    # Check for correct number of arguments
    if 2 < len(sys.argv) or len(sys.argv) < 2:
        print('Usage: %s <url>' % (sys.argv[0]))
        return -1

    # English Wikipedia pages
    wiki = wikipediaapi.Wikipedia('en')

    # Check entered URL is a valid Wikipedia page
    url = sys.argv[1]
    if not url.startswith('https://en.wikipedia.org/wiki/'):
        print('Invalid URL, must be Wikipedia article')
        return -1

    # Extract topic from URL and check if it has a Wikipedia article
    topic = url.removeprefix('https://en.wikipedia.org/wiki/')
    page = wiki.page(topic)
    if not page.exists():
        print('Invalid URL, must be Wikipedia article')
        return -1

if __name__ == '__main__':
    main()
