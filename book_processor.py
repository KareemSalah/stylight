import os
import sys


class BookAnalyzer:
    def __init__(self, word_analyzer = None, book_path = None):
        self.book_path = book_path
        self.word_analyzer = word_analyzer
        self.file_length = 0

    def read_file_length(self):
        """Reads total number of bytes in the file
        And stores it in file_length to be used later on in metrics monitoring
        """
        try:
            self.file_length = os.path.getsize(self.book_path)
        except:
            print('Error opening file at' + self.book_path)

    def run(self):
        self.read_file_length()

        with open(self.book_path, 'rU') as book:

            for idx, line in enumerate(book.readlines()):
                words = line.split()

                for word in words:
                    self.word_analyzer.insert_word(word)