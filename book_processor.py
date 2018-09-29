import os
import sys
from codecs import BOM_UTF8, BOM_UTF16_BE, BOM_UTF16_LE, BOM_UTF32_BE, BOM_UTF32_LE


class BookAnalyzer:
    def __init__(self, word_analyzer=None, book_path=None, chunk_size=1000):
        self.book_path = book_path
        self.word_analyzer = word_analyzer
        self.file_length = 0
        self.chunk_size = chunk_size
        self.encode_type = ''


    def detect_file_encoding(self):
        """Detects file encoding through detecting BOM
        If no BOM is found or no corresponding encoding is found, fall back to ASCII
        """
        BOMS = (
            (BOM_UTF8, "UTF-8-SIG"),
            (BOM_UTF32_BE, "UTF-32-BE"),
            (BOM_UTF32_LE, "UTF-32-LE"),
            (BOM_UTF16_BE, "UTF-16-BE"),
            (BOM_UTF16_LE, "UTF-16-LE")
        )

        book = open(self.book_path, 'rbU')
        bombyte = book.read(3)
        book.close()
        encoding = [encoding for bom, encoding in BOMS if bombyte.startswith(bom)]

        if len(encoding) > 0:
            self.encode_type = encoding[0]
        else:
            self.encode_type = 'ascii'


    def read_file_length(self):
        """Reads total number of bytes in the file
        And stores it in file_length to be used later on in metrics monitoring
        """
        try:
            self.file_length = os.path.getsize(self.book_path)
        except:
            print('Error opening file at' + self.book_path)


    def process_book(self):
        """ This function goes through the book and processes words
        It reads chunks of bytes out of the book and process these chunks
        """
        with open(self.book_path, 'rU', encoding=self.encode_type) as book:

            current_word = ''
            reading_word = False

            while True:
                line = book.read(self.chunk_size)

                for idx, char in enumerate(line):
                    if not char.isspace():
                        current_word = current_word + char
                        reading_word = True
                    elif reading_word:
                        self.word_analyzer.insert_word(current_word)
                        current_word = ''
                        reading_word = False

                if line == '':
                    if reading_word and len(current_word) > 0:
                        self.word_analyzer.insert_word(reading_word)
                    break


    def run(self):
        self.read_file_length()
        self.detect_file_encoding()
        self.process_book()
