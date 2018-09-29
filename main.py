import os
from book_processor import BookAnalyzer
from word_analyzer import WordAnalyzer

# Useful variables
dirname = os.path.dirname(os.path.realpath(__file__))


# Input variables
book_name = 'short-story.txt'
book_path = os.path.join(dirname, book_name)
chunk_size = 1000


def main():
    word_analyzer = WordAnalyzer()
    book_analyzer = BookAnalyzer(word_analyzer=word_analyzer, book_path=book_path, chunk_size=chunk_size)

    book_analyzer.run()
    word_analyzer.persist_results()

if __name__ == '__main__':
    main()