# Grephy
A python script which emulates grep.

- As a note to begin, this is a brute force method for recognizing a string based on an NFA. In no way shape or form is this the most efficient way of making grep.

- The project uses the following imports:

`argparse, re, networkx, ConfigParser, and io`

Please run  `pip install [PACKAGE]` to get these files to run my code.

- To run the file, do `python grephy.py [-n NFA_FILE] [-d DFA_FILE] REGEX FILE`. ***Note: Please wrap your regex in "quotes".***

- The REGEX will recognize characters, the kleene star (\*), the or operator (+), and parenthesis. 

`-n` and `-d` are optional parameters which respectively output the NFA or DFA to a txt file in the format of:

```{node, node transitioning to, {transition: transition character} }```

All that you need to do is specify what file you want the NFA or DFA to output to.

- Here is an example of an NFA that will be printed for the regex `abc`

(0, 1, {'transition': 'a'})
(1, 2, {'transition': 'b'})
(2, 3, {'transition': 'c'})

- For a DFA, the transitions are a little out of order, however, they still produce a valid DFA.
(0, 1, {'transition': ['c', 'b']})
(0, 2, {'transition': 'a'})
(1, 1, {'transition': ['a', 'c', 'b']})
(2, 3, {'transition': ['a', 'c']})
(2, 4, {'transition': 'b'})
(3, 3, {'transition': ['a', 'c', 'b']})
(4, 5, {'transition': ['a', 'b']})
(4, 6, {'transition': 'c'})
(5, 5, {'transition': ['a', 'c', 'b']})

- The output will be printed either in a list to the console of all of the words of the test file which match. If there are no matches, the program will print "No Matches."

- There are a few test files which exist in the `testFiles/` folder. Here are a few descriptions:

    - `pride.txt` : Contains the Wikipedia plot summary for the book 'Pride and Prejudice' by Jane Austen.
    - `fresh.txt` : Contains the lyrics to the song "The Fresh Prince of Belair"
    - `roster.txt`: Contains the roster to the Pittsburgh Steelers Football Team.

- There are also `nfaExample.txt` and `dfaExample.txt` files which show what an outputted DFA and NFA look like.

- `testing.txt` in testFiles which shows sample regex inputs on testFiles and what output that you should recieve.

If there are any questions, email me at `taddbindas@gmail.com`
