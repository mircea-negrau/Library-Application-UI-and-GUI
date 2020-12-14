import sqlite3

from domain.repositories.inmemory.book_repository import BookRepository


class BookDatabaseRepository(BookRepository):
    def __init__(self, read_book, write_book):
        self.connection = sqlite3.connect('library.db')
        self.__create_database()
        BookRepository.__init__(self)
        self.__read_book = read_book
        self.__write_book = write_book
        self.set_next_book_id()

    def __create_database(self):
        cursor = self.connection.cursor()
        command = """CREATE TABLE IF NOT EXISTS books(book_id INTEGER PRIMARY KEY, title TEXT, author TEXT)"""
        cursor.execute(command)

    def add_book(self, book):
        self.__read_all_from_database()
        BookRepository.add_book(self, book)
        self.__add_to_database(book)

    def __add_to_database(self, book):
        string = """INSERT INTO books(title,author,book_id) VALUES (?,?,?)"""
        book_formatted = self.__write_book(book)
        cursor = self.connection.cursor()
        cursor.execute(string, book_formatted)
        self.connection.commit()

    def remove_book_by_index(self, index):
        self.__read_all_from_database()
        book = self.get_all_books()[index]
        BookRepository.remove_book_by_index(self, index)
        self.__remove_from_database(book.id)

    def __remove_from_database(self, book):
        string = """DELETE FROM books WHERE book_id = ?"""
        cursor = self.connection.cursor()
        cursor.execute(string, str(book))
        self.connection.commit()

    def update_book(self, index, book):
        self.__read_all_from_database()
        BookRepository.update_book(self, index, book)
        self.__update_to_database(index, book)

    def __update_to_database(self, _, book):
        string = "UPDATE books SET title = ?, author = ? WHERE book_id = ?"
        book_formatted = self.__write_book(book)
        cursor = self.connection.cursor()
        cursor.execute(string, book_formatted)
        self.connection.commit()

    def get_all_books(self):
        self.__read_all_from_database()
        return BookRepository.get_all_books(self)

    def set_next_book_id(self):
        maximum_id = 0
        for book in self.get_all_books():
            maximum_id = max(maximum_id, book.id)
        self._last_book_id = maximum_id

    def __read_all_from_database(self):
        self._books = []
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM books")
        try:
            book_row = cursor.fetchone()
            while book_row is not None:
                book = self.__read_book(book_row)
                self._books.append(book)
                book_row = cursor.fetchone()
        except Exception as exception:
            raise Exception(exception)
        finally:
            cursor.close()
