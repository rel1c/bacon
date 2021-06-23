import sqlite3
import wikipediaapi

# English Wikipedia pages
WIKI = wikipediaapi.Wikipedia('en')
ADDR = 'https://en.wikipedia.org/wiki/'

# Maximum depth to search for links
MAX_DEPTH = 3

def idfs(s, con, cur):
    while(len(s)):
        (page, depth) = s.pop()
        cur.execute("SELECT title, depth FROM links WHERE title == ?", (page.title,))
        r = cur.fetchone()
        if not r:
            cur.execute("INSERT INTO links VALUES (?, ?)", (page.title, depth))
            if depth >= MAX_DEPTH:
                continue
            links = page.backlinks # Work backwards from initial page
            for title, link in list(links.items())[::-1]: # Treat list like a stack
                if link.namespace != wikipediaapi.Namespace.MAIN:
                    continue
                cur.execute("SELECT title, depth FROM links WHERE title == ?", (title,))
                r = cur.fetchone()
                if not r:
                    s.append((link, depth+1))
        con.commit()
    print('Stack is empty, exiting loop.')

def main():

    # Initialize target and database
    target = WIKI.page('Kevin Bacon')
    con = sqlite3.connect('test.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS links (title, depth)")
    s = []
    s.append((target, 0)) # Initial page is at zero depth

    idfs(s, con, cur)

    con.commit()
    for i in range(MAX_DEPTH+1):
        cur.execute("SELECT * FROM links WHERE depth == ?", (i,))
        r = cur.fetchall()
        print('Number of links found at depth %d: %d' % (i, len(r)))
    con.close()

if __name__ == '__main__':
    main()
