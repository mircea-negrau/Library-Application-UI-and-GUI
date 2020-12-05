from domain.repositories.inmemory.book_repository import BookRepository


class BookTextRepository(BookRepository):
    def __init__(self, filename, read_book, write_book):
        BookRepository.__init__(self)
        self.__filename = filename
        self.__read_book = read_book
        self.__write_book = write_book
        self.set_next_book_id()

    def __read_all_from_file(self):
        self._books = []
        with open(self.__filename, "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line != "":
                    book = self.__read_book(line)
                    self._books.append(book)

    def __write_all_to_file(self):
        with open(self.__filename, "w") as file:
            for book in self._books:
                line = self.__write_book(book)
                file.write(line + "\n")

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

