from domain.repositories.inmemory.book_repository import BookRepository
import pickle


class BookBinaryRepository(BookRepository):
    def __init__(self, filename):
        BookRepository.__init__(self)
        self.__filename = filename
        self.set_next_book_id()

    def __read_all_from_file(self):
        self._books = []
        with open(self.__filename, "rb") as file:
            while True:
                try:
                    book = pickle.load(file)
                except EOFError:
                    book = None
                if book is not None:
                    self._books.append(book)
                else:
                    break

    def __write_all_to_file(self):
        with open(self.__filename, "wb") as file:
            for book in self._books:
                pickle.dump(book, file)

    def add_book(self, book):
        self.__read_all_from_file()
        BookRepository.add_book(self, book)
        self.__write_all_to_file()

    def remove_book_by_index(self, index):
        self.__read_all_from_file()
        BookRepository.remove_book_by_index(self, index)
        self.__write_all_to_file()

    def update_book(self, index, new_book):
        self.__read_all_from_file()
        BookRepository.update_book(self, index, new_book)
        self.__write_all_to_file()

    def get_all_books(self):
        self.__read_all_from_file()
        return BookRepository.get_all_books(self)

    def set_next_book_id(self):
        maximum_id = 0
        for book in self.get_all_books():
            maximum_id = max(maximum_id, book.id)
        self._last_book_id = maximum_id
