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

## Performance

The program relies on parsing links in a queue in memory, so large searches may
exhaust all memory, given enough time. Breadth-first search is not the fastest
search algorithm, but it is complete in finding the shortest path. On my machine
with an Intel i5-8250 and 8Gb of memory I can execute the following searches.

|Title |Degrees| Time|
|---   |---    |---  |
|A Few Good Men |1 |0m 2s |
|Tom Cruise |2 |0m 21s |
|The Color of Money |2 |4m 19s |

## Requirements

This program was written for Python 3.9.5 and uses the `wikipedia-api` Python
package.

## Usage

Run the included Makefile to download the required Python packages.

To run a search execute the `main.py` file followed by a valid Wikipedia URL.

```bash
$ ./main.py https://en.wikipedia.org/wiki/Six_Degrees_of_Kevin_Bacon
```
