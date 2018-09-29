import os
import sys
from codecs import BOM_UTF8, BOM_UTF16_BE, BOM_UTF16_LE, BOM_UTF32_BE, BOM_UTF32_LE


class BookAnalyzer:
    def __init__(self, word_analyzer = None, book_path = None):
        self.book_path = book_path
        self.word_analyzer = word_analyzer
        self.file_length = 0
        self.encode_type = ''


    def detect_file_encoding(self):
        BOMS = (
            (BOM_UTF8, "UTF-8-SIG"),
            (BOM_UTF32_BE, "UTF-32-BE"),
            (BOM_UTF32_LE, "UTF-32-LE"),
            (BOM_UTF16_BE, "UTF-16-BE"),
            (BOM_UTF16_LE, "UTF-16-LE")
        )

        bombyte = open(self.book_path, 'rbU').read(3)
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


    def run(self):
        self.read_file_length()
        self.detect_file_encoding()

        with open(self.book_path, 'rU', encoding=self.encode_type) as book:

            for idx, line in enumerate(book.readlines()):
                words = line.split()

                for word in words:
                    self.word_analyzer.insert_word(word)