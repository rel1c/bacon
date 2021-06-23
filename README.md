## Problem Description

The goal of this project was to write a program that can take any page on
Wikipedia and compute the number of links to the Wikipedia page for actor
Kevin Bacon.

For example, there is a one-link separation between Footloose and Kevin Bacon,
a two-link separation between Tom Cruise and Kevin Bacon, and a three-link
separation between Kevin Bacon and the Taj Mahal.

Inputs to the program are a valid English Wikipedia article URL, and the output
is an integer representing the degree of separation between the given URL and
the Kevin Bacon Wikipedia page. The program returns -1 in the rare case when
there is no such series of links.

## Methodology

To search for the shortest connection the program uses breadth-first search.
The program relies on using the Python Wikipedia API for requesting pages and
their links from Wikipedia. Due to the slow nature of waiting on API requests,
the breadth-first search algorithm is executed in parallel on multiple threads.

Since all links of interest exist on a path towards the Kevin Bacon, it made
sense to build a simple database of backlinks from Kevin Bacon. The program
`build_db.py` uses a form of iterative-deepening depth-first search to discover
backlinks spreading out from Kevin Bacon, to a default degree of 3. The
database takes the form of a "glorified dictionary" holding only article titles
and their degree of separation from Kevin Bacon.

When the main `bacon.py` encounters an article outside of the database it runs
the aforementioned breadth-first search until it finds one. It is very rare a
search is 6 or more degrees away, and the average search is around 3 degrees
which is already stored in the database.

The database is relatively small at under 20MB, even though it takes a *long*
time to build. The `build_db.py` is not optimized well, and could in future
use a methodology similar to the parallelization in `bacon.py`. The alternative
of downloading and parsing the latest Wikipedia database
(at a whopping 8GB+ compressed) seemed like overkill when 3 degrees and under
is common for most articles.

## Performance

The program relies on parsing links in a queue in memory, so large searches may
exhaust all memory, given enough time. Breadth-first search is not the fastest
search algorithm, but it is complete in finding the shortest path. On my machine
with an Intel i5-8250 and 8GB of memory I can execute the following searches.

|Title |Degrees| Time|
|---   |---    |---  |
|Amandeep Drall *Orphaned article* |-1|0.559s |
|A Few Good Men                    |1 |0.454s |
|The Color of Money                |2 |0.373s |
|Communist Part of Great Britain   |3 |0.413s |
|Peanut butter                     |4 |1.029s |
|Lion Express                      |5 |1.096s |

## Requirements

This program was written for Python 3.9.5 and uses the `wikipedia-api` and 
`sqlite3` Python package.

## Usage

Run the included Makefile to download the required Python packages.

To run a search execute the `bacon.py` file followed by a valid Wikipedia URL.

```bash
$ python3 bacon.py https://en.wikipedia.org/wiki/Six_Degrees_of_Kevin_Bacon
```

To generate a new database, or update an existing simply run the `build_db.py`
file.
