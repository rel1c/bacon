import queue
import sqlite3
import wikipediaapi

# Wikipedia address format for English articles
WIKI = wikipediaapi.Wikipedia('en')

# Maximum depth to search for links
MAX_DEPTH = 3

def build_db(con, target):
    '''Builds a database of links and their depth from an initial set of
    Wikipedia pages in a stack. The function uses a search similar to iterative
    deepening DFS to save on memory and record the shallowest depth.'''
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS links (title, depth)")
    pages = []
    pages.append((target, 0)) # Initial page is at zero depth
    while(len(pages)):
        # Fetch page and its depth from stack
        (page, depth) = pages.pop()
        cur.execute("SELECT title, depth FROM links WHERE title == ?", (page.title,))
        result= cur.fetchone()
        # If page is not in database, insert it
        if not result:
            cur.execute("INSERT INTO links VALUES (?, ?)", (page.title, depth))
            con.commit()
        # If page depth is less than what is recorded, update it
        elif depth < result[1]:
            cur.execute("UPDATE links SET depth = ? WHERE title = ?", (depth, page.title))
            con.commit()
        if depth >= MAX_DEPTH:
            continue

        links = page.backlinks # Work backwards from initial page
        for title, link in links.items():
            if link.namespace != wikipediaapi.Namespace.MAIN:
                continue
            cur.execute("SELECT title, depth FROM links WHERE title == ?", (title,))
            result = cur.fetchone()
            if not result or depth < result[1]:
                pages.append((link, depth+1))

def main():

    # Initialize target and database
    con = sqlite3.connect('links.db')
    target = WIKI.page('Kevin Bacon')
    build_db(con, target)
    con.commit()
    con.close()

if __name__ == '__main__':
    main()
