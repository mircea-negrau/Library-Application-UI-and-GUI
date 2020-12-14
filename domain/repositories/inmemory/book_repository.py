class BookRepository(object):
    def __init__(self):
        self._books = []
        self._last_book_id = 0

    def add_book(self, book):
        """
        Function to add a book to the book repository.
        :param book: object, contains the book object to be appended to the repository
        """
        self._books.append(book)

    def remove_book_by_index(self, index):
        """
        Function to remove a book from the book repository.
        :param index: integer, holds the value of the positional index of the book to be removed from the repository.
        """
        del self._books[index]
        return

    def update_book(self, index, new_book):
        """
        Function to update the details of a book found in the book repository.
        :param index: integer, holds the value of the positional index of the book to be updated from the repository.
        :param new_book: object, contains the updated book object to replace the one found at index in the repository.
        """
        self._books[index] = new_book

    def get_next_book_id(self):
        """
        Function to return the next valid ID for a book in the repository.
        :return: integer, next valid ID for a book.
        """
        self.increment_last_book_id()
        return self._last_book_id

    def increment_last_book_id(self):
        """
        Function to increment the last used book ID in the repository.
        """
        self._last_book_id += 1

    def get_all_books(self):
        """
        Function to return the full list of books found in the repository.
        :return: list, containing the full list of books.
        """
        return self._books