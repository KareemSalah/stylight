import os
import sys
import threading
import resource
import time
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
        print('\n====== Begin Detecting file encoding ======')

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
            print('Detected BOM byte: ' + str(bombyte))
            print('Using encoding: ' + self.encode_type)
        else:
            self.encode_type = 'ascii'

        print('====== End Detecting file encoding ======\n')


    def read_file_length(self):
        """Reads total number of bytes in the file
        And stores it in file_length to be used later on in metrics monitoring
        """

        print('\n====== Begin Reading File Length ======')

        try:
            self.file_length = os.path.getsize(self.book_path)
            print('File size is: ' + str(self.file_length) + ' Bytes')
        except:
            print('Error opening file at' + self.book_path)

        print('====== End Reading File Length ======\n')


    def process_book(self):
        """ This function goes through the book and processes words
        It reads chunks of bytes out of the book and process these chunks
        """

        print('\n====== Begin Processing File ======')

        with open(self.book_path, 'rU', encoding=self.encode_type) as book:

            current_word = ''
            reading_word = False
            chunk_number = 0
            completed = False
            rate = 0

            # def print_memory_usage():
            #     if completed == False:
            #         threading.Timer(0.001, print_memory_usage).start()
            #         print('Memory usage: ' + str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) + ' KB')
            #         print('Processing rate: ' + str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) + ' Bytes per second')

            # print_memory_usage()

            while True:
                chunk_number = chunk_number + 1
                line = book.read(self.chunk_size)

                print('Reading chunk #' + str(chunk_number) + ' with chunk size: ' + str(self.chunk_size) + ' Bytes')

                time_begin = time.perf_counter()

                for idx, char in enumerate(line):
                    if not char.isspace():
                        current_word = current_word + char
                        reading_word = True
                    elif reading_word:
                        self.word_analyzer.insert_word(current_word)
                        current_word = ''
                        reading_word = False

                time_end = time.perf_counter()
                print(time_begin)
                print(time_end)
                print('Completed ' + str(round(chunk_number * self.chunk_size / self.file_length * 100.0)) + '%')
                print('Processing rate (Bytes Per Second): ' + str(self.chunk_size / (time_end - time_begin)) + ' Bytes per second')
                print('Processing rate (MegaBytes Per Second): ' + str(self.chunk_size / (time_end - time_begin) / 1000000) + ' MB per second')
                print('Memory usage: ' + str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) + ' KB')

                if line == '':
                    if reading_word and len(current_word) > 0:
                        self.word_analyzer.insert_word(reading_word)

                    completed = True
                    print('No more chunks to read')
                    break

        print('====== End Processing File ======\n')


    def run(self):
        self.read_file_length()
        self.detect_file_encoding()
        self.process_book()
