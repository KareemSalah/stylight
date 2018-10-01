### Problem 1 Solution

## Solution Algorith Walkthrough:
  Here's how I approached this problem:
  1. I did some analysis on the file to have an idea on what might be inside, what special characters in ther, how they're used (I wrote code for that)
  2. I found many patterns and based on them I started to design the solution
  3. I created 2 modules, word analyzer (Given a word as input, processes it and inserts it into a datastructure for counting)
  4. Another module is book processor (takes a path to a book, starts reading it in chunks, extracts words and sends them to word analyzer)
  5. I started researching on using the perfect datastructure, I thought of using a Trie, it turned out that dictionaries are faster
  6. I thought of using a collections.counter container, but again the performance of dictionaries are faster
  7. I used a dictionary and I picked Python 3.5 for this (so that it can be ran on PyPy)
  8. I started the implementation incrementally (see github pull requests)

## Processing words:
  1. Words are stripped first of these characters `.,_;:!?\'"*-`
  2. I look for square brackets, if I find a perfect pair [], then I keep them, if I don't find a perfect pair, I remove them (consider this case `[hello`)
  3. I do the same for parenthesis as in step 2
  4. I remove all double quotes
  5. Last step, if I find words that are joined in `--`, I split them and process them again (consider this case `and--doing`)
  6. Eventually I insert it into a dictionary
  7. For printing them sorted descendingly, I get the key-values and sort them out on values and print


## Complexsity Analysis:
  1. I'm reading the whole book one time, this means O(N) where N is the length of the book in bytes
  2. I'm doing processing on the words in a constant fashion, strip is O(N), searching a string is O(N) (searching for one character), yielding O(c*N) for analysis, since c is a constant, it's O(N)
  3. Inserting into the dictionary is O(1) time, however since keys are strings and worst case there will be only collisions, then it's O(N)
  4. Since worst case scenario is extremely rare (No book has the same words everywhere), then time should be linear O(N) plus some constant factors

## Notes:
  1. The reason I process words like this is that I tried to learn about the requirement, and try to achieve the best result, the requirement says to split words only on whitespaces, that won't work for cases like `and--doing`, and that would produce words like `[hello` and `hello` as 2 different words in dictionary, same with `hello,` and `hello`.
  2. Although I had to do this on weekend, I couldn't get much feedback from you before working, I assumed that what I'm doing is required by you, however in real life, I should have meetings with the client to understand them completely and agree on requirements, my software engineering teacher always told me that client doesn't completely konw what they want :)