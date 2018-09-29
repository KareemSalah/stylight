import json

class WordAnalyzer:

    def __init__(self):
        self.word_counter = {}

    def insert_word(self, word):
        """Inserts a word in the dictionary
        If the word is of zero length
        An exception is thrown of ValueError
        """

        if len(word) == 0:
            raise ValueError('Empty word')

        word = str.lower(word)

        if word not in self.word_counter:
            self.word_counter[word] = 1
        else:
            self.word_counter[word] += 1


    def persist_results(self):
        """Writes results on disk
        Filename is output.json
        """

        with open('output.json', 'w') as output_file:
            output_file.writelines(json.dumps(self.word_counter, indent=2))