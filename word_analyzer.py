import json

class WordAnalyzer:

    def __init__(self):
        self.word_counter = {}
        self.chars_stripping = '.,_;:!?\'"*-'


    def process_word(self, word):
        """Processes a word by stripping special characters
        From begining and end of string only
        Don't touch special characters in middle of word
        """

        if len(word) == 0:
            raise ValueError('Empty word')

        squar_bracket_left = 0
        squar_bracket_right = 0
        parenthesis_left = 0
        parenthesis_right = 0
        double_quotes = 0

        for char in word:
            if char == '[':
                squar_bracket_left = 1
            elif char == ']':
                squar_bracket_right = 1
            elif char == '(':
                parenthesis_left = 1
            elif char == ')':
                parenthesis_right = 1
            elif char == '"':
                double_quotes = 1

        word = word.strip(self.chars_stripping)
        word = str.lower(word)

        if squar_bracket_left + squar_bracket_right == 1:
            word = word.strip('][')

        if parenthesis_left + parenthesis_right == 1:
            word = word.strip(')(')

        if double_quotes:
            word = word.replace('"', '')

        word = word.strip(self.chars_stripping)

        # Returning a list because in future, a word might needs to be splitted into other words
        if '--' in word:
            return word.split('--')
        return [word]


    def insert_word(self, word):
        """Inserts a word in the dictionary
        If the word is of zero length
        An exception is thrown of ValueError
        """

        result = self.process_word(word)

        for processed_word in result:
            if not len(processed_word):
                continue
            if processed_word not in self.word_counter:
                self.word_counter[processed_word] = 1
            else:
                self.word_counter[processed_word] += 1


    def persist_results(self):
        """Writes results on disk
        Filename is output.json
        """

        with open('output.json', 'w') as output_file:
            output_file.writelines(json.dumps(self.word_counter, indent=2))