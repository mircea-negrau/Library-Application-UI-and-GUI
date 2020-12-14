from domain.entities.book_entity import Book
from functionalities.validation.exceptions import RepoError


class BookService:
    def __init__(self, action_service, book_repository, book_validator):
        self.__action_service = action_service
        self.__book_repository = book_repository
        self.__book_validator = book_validator

    def add_book(self, title_as_string, author_name_as_string):
        """
        Function to add a book to the book repository with the title and author name given by the parameters. The
        function creates a new 'Book' entity which then passes through the 'BookValidator'. In case any of the book's
        parameters are incorrect, the book is not added but an error is raised instead. Otherwise, the book is added
        to the book repository.
        :param title_as_string: string, holds the title for the book to be added; it should be between 1 and
        25 characters.
        :param author_name_as_string: string, holds the name of the author for the book to be added; it should be
        between 1 and 25 characters.
        """
        current_book_id = self.__book_repository.get_next_book_id()
        current_book = Book(current_book_id, title_as_string, author_name_as_string)
        self.__book_validator.validate_book(current_book)
        self.__book_repository.add_book(current_book)
        self.__action_service.push_add_action_to_undo_list(current_book)

    def remove_book_by_book_id(self, book_id):
        """
        Function to remove the book from the book repository that has the ID given by the parameter. If no book is found
        identified by the given ID no books are removed, but an error is raised instead. Otherwise, the book is removed
        from the book repository. Nothing is returned.
        :param book_id: integer, holds the value of the ID of the book to be removed. It should be a natural integer.
        """
        book_index, book = self.find_book_by_book_id(book_id)
        if book_index is None:
            raise RepoError("Book not found. ")
        self.__book_repository.remove_book_by_index(book_index)
        self.__action_service.push_remove_action_to_undo_list(book)

    def update_book_by_book_id(self, book_id, new_title_as_string, new_author_name_as_string):
        """
        Function to update the details of a book entity found in the book repository with the values given by the
        function's parameters. If no book is found in the repository identified by the given book ID, an error is raised
        instead. Otherwise, the title and author name are replaced by the given values. If the given values do not
        properly create a book entity, an error is raised instead. Nothing is returned.
        :param book_id: integer, holds the value of the book that the function updates. Should be an natural integer.
        :param new_title_as_string: string, holds the new name of the title. Should be between 1 and 25 characters.
        :param new_author_name_as_string: string, holds the new name of the author. Should be between 1 and
            25 characters.
        """
        book_index, book_to_update = self.find_book_by_book_id(book_id)
        if book_to_update is None:
            raise RepoError("Book not found. ")
        updated_book = Book(book_id, new_title_as_string, new_author_name_as_string)
        self.__book_validator.validate_book(updated_book)
        self.__book_repository.update_book(book_index, updated_book)
        self.__action_service.push_update_action_to_undo_list(book_to_update, updated_book)

    def validate_book_with_parameters(self, book_id, title_as_string, author_name_as_string):
        """
        Function to validate that the parameters received by the function can correctly compose together a book entity.
        :param book_id: integer, holds the value of the ID of the book to be validated. It should be a natural integer.
        :param title_as_string: string, holds the title of the book to be validated.
        :param author_name_as_string: string, holds the name of the author of the book to be validated.
        """
        book_to_validate = Book(book_id, title_as_string, author_name_as_string)
        self.__book_validator.validate_book(book_to_validate)
        del book_to_validate

    def find_book_by_book_id(self, book_id):
        """
        Function to return the index and book identified in the book repository by the ID given by the parameter. If no
        book is found or the 'book_id' is an invalid value, nothing is returned but an error is raised instead.
        Otherwise, the positional index and the book entity are returned.
        :param book_id: integer, holds the value of the ID of the book to be found. It should be a natural integer.
        :return: Index (integer) and book (entity) of the book that the function searched for. If no book is found,
        the values 'None' and 'None' are returned for the integer and book entity.
        """
        self.validate_book_with_parameters(book_id, "Best Title", "Best Author")
        books_list = self.__book_repository.get_all_books()
        for index, book in enumerate(books_list):
            found_book = book.id == book_id
            if found_book:
                return index, book
        return None, None

    def find_book_by_title_and_author(self, title_as_string, author_name_as_string):
        """
        Function to search for a book in the book repository that has the title and author name as the parameters given.
        The title and author name go through a validator. If the book fails the validator, no book is found, but an
        error is raised instead. Otherwise, if the book is found in the book repository, the function returns the book's
        positional index in the repository as well as the 'book' object. If no book is found in the repository, the
        function returns None values for both the index and the 'book' object.
        :param title_as_string: string, holds the title of the book to be found.
        :param author_name_as_string: string, holds the name of the author of the book to be found.
        :return: If book is found, returns the positional index and the 'book' object of the book. Otherwise, returns
        None and None.
        """
        self.validate_book_with_parameters(1, title_as_string, author_name_as_string)
        books_list = self.__book_repository.get_all_books()
        for index, book in enumerate(books_list):
            found_book = book.title == title_as_string and book.author == author_name_as_string
            if found_book:
                return index, book
        return None, None

    def find_all_books_with_id_containing_value(self, book_id_value):
        """
        Function to find all the books in the book repository for which the 'book_id' matches at least partially
        the value given by the parameter.
        :param book_id_value: integer, holds the value of the ID of books to at least partially match.
        :return: list, containing all the book entities matching at least partially the given 'book_id' value
        """
        books_list = self.__book_repository.get_all_books()
        list_of_matching_books = []
        for book in books_list:
            if str(book_id_value) in str(book.id):
                list_of_matching_books.append(book)
        return list_of_matching_books

    def find_all_books_with_title_containing_string(self, book_title_as_string):
        """
        Function to find all the books in the book repository for which the 'title' matches at least partially
        the value given by the parameter.
        :param book_title_as_string: string, holds the string of the title of books to at least partially match.
        :return: list, containing all the book entities matching at least partially the given 'title' string.
        """
        books_list = self.__book_repository.get_all_books()
        list_of_matching_books = []
        for book in books_list:
            if book_title_as_string.lower() in book.title.lower():
                list_of_matching_books.append(book)
        return list_of_matching_books

    def find_all_books_with_author_containing_string(self, book_author_as_string):
        """
        Function to find all the books in the book repository for which the 'author' matches at least partially
        the value given by the parameter.
        :param book_author_as_string: string, holds the string of the author of books to at least partially match.
        :return: list, containing all the book entities matching at least partially the given 'author' string.
        """
        books_list = self.__book_repository.get_all_books()
        list_of_matching_books = []
        for book in books_list:
            if book_author_as_string.lower() in book.author.lower():
                list_of_matching_books.append(book)
        return list_of_matching_books

    def get_book_by_book_id(self, book_id):
        """
        Function to return the book from the book repository that matches the 'book_id' value as the one received by the
        function's parameter. If no books are found, the function returns None.
        :param book_id: integer, holds the value of the ID for the book be returned
        :return: book entity, matching the ID. If none found, 'None' is returned
        """
        books_list = self.__book_repository.get_all_books()
        for book in books_list:
            if book.id == book_id:
                return book
        return None

    def get_all_books(self):
        books_list = sorted(self.__book_repository.get_all_books(), key=lambda book: book.id)
        return books_list