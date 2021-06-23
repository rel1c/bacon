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
    s = []
    s.append((target, 0)) # Initial page is at zero depth
    while(len(s)):
        # Fetch page and its depth from stack
        (page, depth) = s.pop()
        cur.execute("SELECT title, depth FROM links WHERE title == ?", (page.title,))
        r = cur.fetchone()
        # If page is not in database, insert it
        if not r:
            cur.execute("INSERT INTO links VALUES (?, ?)", (page.title, depth))
            con.commit()
        # If page depth is less than what is recorded, update it
        elif depth < r[1]:
            cur.execute("UPDATE links SET depth = ? WHERE title = ?", (depth, page.title))
            con.commit()
        if depth >= MAX_DEPTH:
            continue

        links = page.backlinks # Work backwards from initial page
        for title, link in links.items():
            if link.namespace != wikipediaapi.Namespace.MAIN:
                continue
            cur.execute("SELECT title, depth FROM links WHERE title == ?", (title,))
            r = cur.fetchone()
            if not r or depth < r[1]:
                s.append((link, depth+1))

def main():

    # Initialize target and database
    con = sqlite3.connect('links.db')
    target = WIKI.page('Kevin Bacon')
    build_db(con, target)
    con.commit()
    con.close()

if __name__ == '__main__':
    main()
