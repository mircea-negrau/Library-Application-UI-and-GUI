import datetime

from functionalities.validation.exceptions import ValidError


class BookValidator(object):
    def __init__(self):
        pass

    @staticmethod
    def validate_book(book):
        """
        Function to check whether or not a book's details are valid. If an error is found, a ValidError containing
        the string of errors found is raised.
        :param book: object, book to be validated
        """
        error_string = ""
        author = book.author
        title = book.title
        author_length = len(author)
        title_length = len(title)
        if author_length < 1 or author_length > 25:
            error_string += "Author name must have between 1 and 25 letters. "
        if title_length < 1 or title_length > 30:
            error_string += "Title must have between 1 and 25 letters. "
        if len(error_string) > 0:
            raise ValidError(error_string)


class ClientValidator(object):
    def __init__(self):
        pass

    @staticmethod
    def validate_client(client):
        """
        Function to check whether or not a client's details are valid. If an error is found, a ValidError containing
        the string of errors found is raised.
        :param client: object, client to be validated.
        """
        error_string = ""
        name = client.name
        name_length = len(name)
        if name_length < 1 or name_length > 25:
            error_string += "Client name must have between 1 and 25 letters. "
        if len(error_string) > 0:
            raise ValidError(error_string)


class RentalValidator(object):
    def __init__(self):
        pass

    @staticmethod
    def validate_rental(rental):
        """
        Function to check whether or not a rental's details are valid. If an error is found, a ValidError containing
        the string of errors found is raised.
        :param rental: object, rental to be validated.
        """
        error_string = ""
        book_id = rental.book_id
        client_id = rental.client_id
        rented_date = rental.rented_date
        returned_date = rental.returned_date
        if not isinstance(book_id, int) or book_id < 0:
            error_string += "Book ID must have a natural number value."
        if not isinstance(client_id, int) or client_id < 0:
            error_string += "Client ID must have a natural number value."
        if not isinstance(rented_date, datetime.date) and rented_date is not None:
            error_string += "Rented date must have a valid YYYY-MM-DD format. "
        if not isinstance(returned_date, datetime.date) and returned_date is not None:
            error_string += "Returned date must have a valid YYYY-MM-DD format. "
        if len(error_string) > 0:
            raise ValidError(error_string)

    @staticmethod
    def validate_book_and_client_ids(book_id, client_id):
        """
        Function to check whether or not a rental's book and client IDs are valid. If an error is found,
        a ValidError containing the string of errors found is raised.
        :param book_id: integer, ID of the book to be validated.
        :param client_id: integer, ID of the client to be validated.
        """
        error_string = ""
        if int(book_id) < 0:
            error_string += "Book ID must have a natural number value. "
        if int(client_id) < 0:
            error_string += "Client ID must have a natural number value. "
        if len(error_string) > 0:
            raise ValidError(error_string)
