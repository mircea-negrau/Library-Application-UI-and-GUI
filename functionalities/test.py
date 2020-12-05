import unittest

from domain.repositories.inmemory.action_repository import ActionRepository
from domain.repositories.inmemory.book_repository import BookRepository
from domain.repositories.inmemory.client_repository import ClientRepository
from domain.repositories.inmemory.rental_repository import RentalRepository
from functionalities.services.action_service import *
from functionalities.services.book_service import *
from functionalities.services.client_service import *
from functionalities.services.rental_service import *
from functionalities.services.rental_service import RentalService
from functionalities.validation.exceptions import RepoError
from functionalities.validation.validators import *
from functionalities.generators.populate_repositories import *


class BookServiceTest(unittest.TestCase):
    def setUp(self):
        self.action_repository = ActionRepository()
        self.book_repository = BookRepository()
        self.client_repository = ClientRepository()
        self.rental_repository = RentalRepository()
        self.action_service = ActionService(self.action_repository, self.book_repository,
                                            self.client_repository, self.rental_repository)
        self.book_validator = BookValidator()
        self.book_service = BookService(self.action_service, self.book_repository, self.book_validator)
        self.book_service.add_book("Title", "Author")
        assert (len(self.book_repository.get_all_books()) == 1)

    def test_book_service_add_book(self):
        self.book_service.add_book("Title", "Author")
        assert (len(self.book_repository.get_all_books()) == 2)
        self.action_service.undo()
        assert (len(self.book_repository.get_all_books()) == 1)
        self.action_service.redo()
        assert (len(self.book_repository.get_all_books()) == 2)
        self.assertRaises(RepoError, self.action_service.redo)

    def test_book_service_remove_book_by_book_id(self):
        self.book_service.remove_book_by_book_id(1)
        assert (len(self.book_repository.get_all_books()) == 0)
        self.assertRaises(RepoError, self.book_service.remove_book_by_book_id, 5)
        self.action_service.undo()
        assert (len(self.book_repository.get_all_books()) == 1)
        self.action_service.undo()
        self.assertRaises(RepoError, self.action_service.undo)
        self.action_service.redo()
        assert (len(self.book_repository.get_all_books()) == 1)

    def test_book_service_update_book_by_book_id(self):
        self.book_service.update_book_by_book_id(1, "New Title", "New Author")
        book = self.book_service.get_book_by_book_id(1)
        assert book.id == 1
        assert book.title == "New Title"
        assert book.author == "New Author"
        self.assertRaises(RepoError, self.book_service.update_book_by_book_id, 5, "New", "New")
        self.action_service.undo()
        book = self.book_service.get_book_by_book_id(1)
        assert book.id == 1
        assert book.title == "Title"
        assert book.author == "Author"
        self.action_service.redo()
        book = self.book_service.get_book_by_book_id(1)
        assert book.id == 1
        assert book.title == "New Title"
        assert book.author == "New Author"

    def test_book_service_find_book_by_book_id(self):
        index, book = self.book_service.find_book_by_book_id(1)
        assert index == 0
        assert isinstance(book, Book)

    def test_book_service_find_book_by_title_and_author(self):
        index, book = self.book_service.find_book_by_title_and_author("Title", "Author")
        assert index == 0
        assert isinstance(book, Book)
        index, book = self.book_service.find_book_by_title_and_author("t", "a")
        assert index is None
        assert book is None

    def test_book_service_find_all_books_with_id_containing_value(self):
        books_list = self.book_service.find_all_books_with_id_containing_value(1)
        assert len(books_list) == 1

    def test_book_service_find_all_books_with_title_containing_string(self):
        books_list = self.book_service.find_all_books_with_title_containing_string("Ti")
        assert len(books_list) == 1

    def test_book_service_find_all_books_with_author_containing_string(self):
        books_list = self.book_service.find_all_books_with_author_containing_string("a")
        assert len(books_list) == 1

    def test_book_service_get_book_by_book_id(self):
        book = self.book_service.get_book_by_book_id(2)
        assert book is None

    def tearDown(self):
        del self.book_repository
        del self.book_validator
        del self.book_service


class ClientServiceTest(unittest.TestCase):
    def setUp(self):
        self.action_repository = ActionRepository()
        self.book_repository = BookRepository()
        self.client_repository = ClientRepository()
        self.rental_repository = RentalRepository()
        self.action_service = ActionService(self.action_repository, self.book_repository,
                                            self.client_repository, self.rental_repository)
        self.client_validator = ClientValidator()
        self.client_service = ClientService(self.action_service, self.client_repository, self.client_validator)
        self.client_service.add_client("Name")
        assert (len(self.client_repository.get_all_clients()) == 1)

    def test_client_service_add_client(self):
        self.client_service.add_client("Name2")
        assert (len(self.client_repository.get_all_clients()) == 2)
        self.action_service.undo()
        assert (len(self.client_repository.get_all_clients()) == 1)
        self.action_service.redo()
        assert (len(self.client_repository.get_all_clients()) == 2)

    def test_client_service_remove_client_by_client_id(self):
        self.client_service.remove_client_by_client_id(1)
        assert (len(self.client_repository.get_all_clients()) == 0)
        self.assertRaises(RepoError, self.client_service.remove_client_by_client_id, 5)
        self.action_service.undo()
        assert (len(self.client_repository.get_all_clients()) == 1)
        self.action_service.redo()
        assert (len(self.client_repository.get_all_clients()) == 0)

    def test_client_service_update_client_by_client_id(self):
        self.client_service.update_client_by_client_id(1, "New Name")
        client = self.client_repository.get_all_clients()[-1]
        assert client.id == 1
        assert client.name == "New Name"
        self.action_service.undo()
        client = self.client_repository.get_all_clients()[-1]
        assert client.id == 1
        assert client.name == "Name"
        self.assertRaises(RepoError, self.client_service.update_client_by_client_id, 5, "New")
        self.action_service.redo()
        client = self.client_repository.get_all_clients()[-1]
        assert client.id == 1
        assert client.name == "New Name"

    def test_client_service_update_client_by_name(self):
        self.client_service.update_client_by_name("Name", "New Name")
        client = self.client_repository.get_all_clients()[-1]
        assert client.id == 1
        assert client.name == "New Name"
        self.assertRaises(RepoError, self.client_service.update_client_by_name, "5", "New")

    def test_client_service_find_client_by_name(self):
        index, client = self.client_service.find_client_by_name("Name")
        assert index == 0
        assert isinstance(client, Client)
        index, client = self.client_service.find_client_by_name("No Name")
        assert index is None

    def test_client_service_find_all_clients_sharing_name_value(self):
        self.client_service.add_client("Nova Scotia")
        client_list = self.client_service.find_all_clients_sharing_name_value("n")
        assert len(client_list) == 2

    def test_client_service_find_all_clients_sharing_id_value(self):
        self.client_service.add_client("Nova Scotia")
        client_list = self.client_service.find_all_clients_sharing_id_value(1)
        assert len(client_list) == 1

    def tearDown(self):
        del self.client_repository
        del self.client_validator
        del self.client_service


class RentalServiceTest(unittest.TestCase):
    def setUp(self):
        self.action_repository = ActionRepository()
        self.book_repository = BookRepository()
        self.client_repository = ClientRepository()
        self.rental_repository = RentalRepository()

        self.action_service = ActionService(self.action_repository, self.book_repository,
                                            self.client_repository, self.rental_repository)

        self.book_validator = BookValidator()
        self.client_validator = ClientValidator()
        self.rental_validator = RentalValidator()

        self.rental_service = RentalService(self.action_service, self.book_repository, self.client_repository,
                                            self.rental_repository, self.book_validator, self.client_validator,
                                            self.rental_validator)

        client = Client(1, "Name1")
        self.client_repository.add_client(client)
        client = Client(2, "Name2")
        self.client_repository.add_client(client)
        book = Book(1, "Title1", "Author1")
        self.book_repository.add_book(book)
        book = Book(2, "Title2", "Author2")
        self.book_repository.add_book(book)

        self.rental_service.add_rental(1, 1)

        assert (len(self.rental_repository.get_all_rentals()) == 1)

    def test_rental_service_add_rental(self):
        self.rental_service.add_rental(2, 2)
        assert (len(self.rental_repository.get_all_rentals()) == 2)
        self.assertRaises(RepoError, self.rental_service.add_rental, 1, 1)
        self.assertRaises(RepoError, self.rental_service.add_rental, 1, 5)
        self.assertRaises(RepoError, self.rental_service.add_rental, 5, 1)
        self.action_service.undo()
        assert (len(self.rental_repository.get_all_rentals()) == 1)
        self.action_service.redo()
        assert (len(self.rental_repository.get_all_rentals()) == 2)

    def test_rental_service_return_rental_by_id(self):
        self.rental_service.return_rental_by_id(1)
        assert (len(self.rental_repository.get_all_rentals()) == 1)
        assert self.rental_repository.get_all_rentals()[-1].returned_date == date.today()
        self.assertRaises(ValidError, self.rental_service.return_rental_by_id, "k")
        self.assertRaises(RepoError, self.rental_service.return_rental_by_id, 5)
        self.action_service.undo()
        assert self.rental_repository.get_all_rentals()[-1].returned_date is None
        self.action_service.redo()
        assert self.rental_repository.get_all_rentals()[-1].returned_date == date.today()

    def test_rental_service_return_rental_by_book_id(self):
        self.rental_service.return_rental_by_book_id(1)
        assert (len(self.rental_repository.get_all_rentals()) == 1)
        assert self.rental_repository.get_all_rentals()[-1].returned_date == date.today()
        self.assertRaises(RepoError, self.rental_service.return_rental_by_book_id, 5)
        self.assertRaises(RepoError, self.rental_service.return_rental_by_book_id, 1)
        self.action_service.undo()
        assert self.rental_repository.get_all_rentals()[-1].returned_date is None
        self.action_service.redo()
        assert self.rental_repository.get_all_rentals()[-1].returned_date == date.today()

    def test_rental_service_remove_rental_by_book_id(self):
        assert (len(self.rental_repository.get_all_rentals()) == 1)
        self.rental_service.remove_rental_by_book_id(1)
        assert (len(self.rental_repository.get_all_rentals()) == 0)
        self.action_service.undo()
        assert (len(self.rental_repository.get_all_rentals()) == 0)
        self.action_service.redo()

    def test_rental_service_remove_rental_by_client_id(self):
        self.rental_service.add_rental(2, 1)
        assert (len(self.rental_repository.get_all_rentals()) == 2)
        self.rental_service.remove_rental_by_client_id(1)
        assert (len(self.rental_repository.get_all_rentals()) == 0)
        assert self.rental_service.remove_rental_by_client_id(1) is None
        self.action_service.undo()
        assert (len(self.rental_repository.get_all_rentals()) == 1)
        self.action_service.redo()
        assert (len(self.rental_repository.get_all_rentals()) == 0)

    def test_rental_service_get_client_active_rentals(self):
        self.rental_service.add_rental(2, 1)
        assert (len(self.rental_repository.get_all_rentals()) == 2)
        rentals_list = self.rental_service.get_client_active_rentals(1)
        assert (len(rentals_list) == 2)

    def test_rental_service_get_book_rental_status(self):
        assert self.rental_service.get_book_rental_status(1) == 1
        assert self.rental_service.get_book_rental_status(5) is None

    def test_rental_service_get_statistics_for_most_active_clients(self):
        self.rental_service.add_rental(2, 1)
        assert (len(self.rental_repository.get_all_rentals()) == 2)
        rentals_list = self.rental_service.get_statistics_for_most_active_clients()
        assert rentals_list[-1]["ID"] == 1

    def test_rental_service_get_statistics_for_most_rented_books(self):
        self.rental_service.return_rental_by_id(1)
        self.rental_service.add_rental(1, 1)
        self.rental_service.add_rental(2, 2)
        assert (len(self.rental_repository.get_all_rentals()) == 3)
        rentals_list = self.rental_service.get_statistics_for_most_rented_books()
        most_rented_book = rentals_list[0]
        assert most_rented_book["Title"] == "Title1"
        assert most_rented_book["Author"] == "Author1"
        assert most_rented_book["Rental amount"] == 2

    def test_rental_service_get_book_by_book_id(self):
        book = self.rental_service.get_book_by_book_id(1)
        assert isinstance(book, Book)
        assert book.id == 1
        assert self.rental_service.get_book_by_book_id(10) is None

    def test_rental_service_get_most_rented_author(self):
        self.rental_service.add_rental(2, 2)
        self.rental_service.return_rental_by_id(1)
        self.rental_service.add_rental(1, 1)
        book = Book(5, "New Title Book", "Author1")
        self.book_repository.add_book(book)
        self.rental_service.add_rental(5, 1)
        author = self.rental_service.get_most_rented_author()
        assert author["Name"] == "Author1"
        books_list = self.rental_service.get_list_of_books_of_most_rented_author(author)
        assert len(books_list) == 2

    def tearDown(self):
        del self.book_repository
        del self.client_repository
        del self.rental_repository
        del self.book_validator
        del self.client_validator
        del self.rental_validator
        del self.rental_service


class ValidatorsTest(unittest.TestCase):
    def setUp(self):
        self.book_validator = BookValidator()
        self.client_validator = ClientValidator()
        self.rental_validator = RentalValidator()

    def test_book_validator(self):
        book = Book(1, "Title", "Author")
        assert self.book_validator.validate_book(book) is None
        book = Book(1, "", "Author")
        self.assertRaises(ValidError, self.book_validator.validate_book, book)
        book = Book(1, "Title", "")
        self.assertRaises(ValidError, self.book_validator.validate_book, book)

    def test_client_validator(self):
        client = Client(1, "Name")
        assert self.client_validator.validate_client(client) is None
        client = Client(1, "")
        self.assertRaises(ValidError, self.client_validator.validate_client, client)

    def test_rental_validator(self):
        rental = Rental(1, 1, 1, date.today(), None)
        assert self.rental_validator.validate_rental(rental) is None
        rental = Rental(1, "1", 1, date.today(), None)
        self.assertRaises(ValidError, self.rental_validator.validate_rental, rental)
        rental = Rental(1, 1, "1", date.today(), None)
        self.assertRaises(ValidError, self.rental_validator.validate_rental, rental)
        rental = Rental(1, 1, 1, "None", None)
        self.assertRaises(ValidError, self.rental_validator.validate_rental, rental)
        rental = Rental(1, 1, 1, date.today(), "None")
        self.assertRaises(ValidError, self.rental_validator.validate_rental, rental)

    def test_validate_book_and_client_ids(self):
        self.assertRaises(ValidError, self.rental_validator.validate_book_and_client_ids, "-1", 2)
        self.assertRaises(ValidError, self.rental_validator.validate_book_and_client_ids, 1, "-2")


class PopulateRepositoriesTest(unittest.TestCase):
    def setUp(self):
        self.book_repository = BookRepository()
        self.client_repository = ClientRepository()
        self.rental_repository = RentalRepository()
        self.action_repository = ActionRepository()
        self.action_service = ActionService(self.action_repository, self.book_repository,
                                            self.client_repository, self.rental_repository)
        self.book_validator = BookValidator()
        self.book_service = BookService(self.action_service, self.book_repository, self.book_validator)
        self.client_validator = ClientValidator()
        self.rental_validator = RentalValidator()
        self.client_service = ClientService(self.action_service, self.client_repository, self.client_validator)
        self.rental_service = RentalService(self.action_service, self.book_repository, self.client_repository,
                                            self.rental_repository, self.book_validator, self.client_validator,
                                            self.rental_validator)

    def test_populate_book_repository(self):
        populate_book_repository(self.book_service)
        assert len(self.book_repository.get_all_books()) > 0

    def test_populate_client_repository(self):
        populate_client_repository(self.client_service)
        assert len(self.client_repository.get_all_clients()) > 0

    def test_populate_rental_repository(self):
        self.test_populate_book_repository()
        self.test_populate_client_repository()
        populate_rental_repository(self.rental_service)
        assert len(self.rental_repository.get_all_rentals()) > 0
