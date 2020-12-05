import unittest
from datetime import date

from domain.entities.book_entity import Book
from domain.entities.client_entity import Client
from domain.entities.rental_entity import Rental
from domain.repositories.inmemory.action_repository import ActionRepository
from domain.repositories.inmemory.book_repository import BookRepository
from domain.repositories.inmemory.client_repository import ClientRepository
from domain.repositories.inmemory.rental_repository import RentalRepository


class BookEntityTest(unittest.TestCase):
    def setUp(self):
        self.book = Book(1, "Test Title", "Test Author")
        assert (self.book.id == 1)
        assert (self.book.title == "Test Title")
        assert (self.book.author == "Test Author")

    def test_book_entity_set_id(self):
        self.book.id = 2
        assert (self.book.id == 2)

    def test_book_entity_set_title(self):
        self.book.title = "New Test Title"
        assert (self.book.title == "New Test Title")

    def test_book_entity_set_author(self):
        self.book.author = "New Test Author"
        assert (self.book.author == "New Test Author")

    def tearDown(self):
        del self.book


class ClientEntityTest(unittest.TestCase):
    def setUp(self):
        self.client = Client(1, "Test Name")
        assert (self.client.id == 1)
        assert (self.client.name == "Test Name")

    def test_client_entity_set_id(self):
        self.client.id = 2
        assert (self.client.id == 2)

    def test_client_entity_set_name(self):
        self.client.name = "New Test Name"
        assert (self.client.name == "New Test Name")

    def tearDown(self):
        del self.client


class RentalEntityTest(unittest.TestCase):
    def setUp(self):
        self.rental = Rental(1, 1, 1, date.today, date.today)
        assert (self.rental.id == 1)
        assert (self.rental.book_id == 1)
        assert (self.rental.client_id == 1)
        assert (self.rental.rented_date == date.today)
        assert (self.rental.returned_date == date.today)

    def test_rental_entity_set_rental_id(self):
        self.rental.id = 2
        assert (self.rental.id == 2)

    def test_rental_entity_set_book_id(self):
        self.rental.book_id = 2
        assert (self.rental.book_id == 2)

    def test_rental_entity_set_client_id(self):
        self.rental.client_id = 2
        assert (self.rental.client_id == 2)

    def test_rental_entity_set_rental_date(self):
        self.rental.rented_date = 2021.17
        assert (self.rental.rented_date == 2021.17)

    def test_rental_entity_set_returned_date(self):
        self.rental.returned_date = 2021.17
        assert (self.rental.returned_date == 2021.17)

    def tearDown(self):
        del self.rental


class BookRepositoryTest(unittest.TestCase):
    def setUp(self):
        self.book_repository = BookRepository()
        book = Book(1, "Title1", "Author1")
        self.book_repository.add_book(book)
        book = Book(2, "Title2", "Author2")
        self.book_repository.add_book(book)

    def test_book_repository_add_book(self):
        book = Book(3, "Title3", "Author3")
        self.book_repository.add_book(book)
        books_list = self.book_repository.get_all_books()
        book = books_list[-1]
        assert (book.id == 3)
        assert (book.title == "Title3")
        assert (book.author == "Author3")

    def test_book_repository_remove_book(self):
        books_list = self.book_repository.get_all_books()
        book = books_list[-1]
        assert (book.id == 2)
        self.book_repository.remove_book_by_index(1)
        book = books_list[-1]
        assert (book.id == 1)

    def test_book_repository_update_book(self):
        books_list = self.book_repository.get_all_books()
        book = books_list[-1]
        assert (book.id == 2)
        new_book = Book(10, "New Title", "New Author")
        self.book_repository.update_book(1, new_book)
        book = books_list[-1]
        assert (book.id == 10)
        assert (book.title == "New Title")
        assert (book.author == "New Author")

    def test_book_repository_get_next_book_id(self):
        assert (self.book_repository.get_next_book_id() == 1)
        self.book_repository.increment_last_book_id()
        assert (self.book_repository.get_next_book_id() == 3)

    def test_book_repository_get_all_books(self):
        books_list = self.book_repository.get_all_books()
        assert len(books_list) == 2

    def tearDown(self):
        del self.book_repository


class ClientRepositoryTest(unittest.TestCase):
    def setUp(self):
        self.client_repository = ClientRepository()
        client = Client(1, "Name1")
        self.client_repository.add_client(client)
        client = Client(2, "Name2")
        self.client_repository.add_client(client)

    def test_client_repository_add_client(self):
        client = Client(3, "Name3")
        self.client_repository.add_client(client)
        client = self.client_repository.get_all_clients()
        client = client[-1]
        assert client.id == 3
        assert client.name == "Name3"

    def test_client_repository_remove_client(self):
        clients_list = self.client_repository.get_all_clients()
        client = clients_list[-1]
        assert client.id == 2
        self.client_repository.remove_client_by_index(1)
        client = clients_list[-1]
        assert client.id == 1

    def test_client_repository_update_client(self):
        clients_list = self.client_repository.get_all_clients()
        client = clients_list[-1]
        assert client.id == 2
        assert client.name == "Name2"
        client = Client(10, "New Name")
        self.client_repository.update_client(1, client)
        clients_list = self.client_repository.get_all_clients()
        client = clients_list[-1]
        assert client.id == 10
        assert client.name == "New Name"

    def test_client_repository_get_next_client_id(self):
        assert self.client_repository.get_next_client_id() == 1
        self.client_repository.increment_last_client_id()
        assert self.client_repository.get_next_client_id() == 3

    def test_client_repository_get_all_clients(self):
        clients_list = self.client_repository.get_all_clients()
        assert len(clients_list) == 2

    def tearDown(self):
        del self.client_repository


class RentalRepositoryTest(unittest.TestCase):
    def setUp(self):
        self.rental_repository = RentalRepository()
        rental = Rental(1, 1, 1, date.today(), date.today())
        self.rental_repository.add_rental(rental)
        rental = Rental(2, 2, 2, date.today(), None)
        self.rental_repository.add_rental(rental)

    def test_rental_repository_add_rental(self):
        rental = Rental(3, 3, 3, date.today(), None)
        self.rental_repository.add_rental(rental)
        rental = self.rental_repository.get_all_rentals()
        rental = rental[-1]
        assert rental.id == 3
        assert rental.book_id == 3
        assert rental.client_id == 3
        assert rental.rented_date == date.today()
        assert rental.returned_date is None

    def test_rental_repository_delete_rental_by_index(self):
        rental = self.rental_repository.get_all_rentals()
        rental = rental[-1]
        assert rental.id == 2
        self.rental_repository.remove_rental_by_index(1)
        rental = self.rental_repository.get_all_rentals()
        rental = rental[-1]
        assert rental.id == 1

    def test_rental_repository_return_rental_by_index(self):
        rental = self.rental_repository.get_all_rentals()
        rental = rental[-1]
        assert rental.id == 2
        assert rental.returned_date is None
        self.rental_repository.update_rental_return_by_index(1, date.today())
        assert rental.returned_date == date.today()

    def test_rental_repository_get_next_rental_id(self):
        assert self.rental_repository.get_next_rental_id() == 1
        self.rental_repository.increment_last_rental_id()
        assert self.rental_repository.get_next_rental_id() == 3

    def test_rental_repository_get_all_rentals(self):
        rentals_list = self.rental_repository.get_all_rentals()
        assert len(rentals_list) == 2

    def tearDown(self):
        del self.rental_repository


class ActionRepositoryTest(unittest.TestCase):
    def setUp(self):
        self.action_repository = ActionRepository()

    def test_action_repository_get_all_actions(self):
        assert len(self.action_repository.get_all_actions()) == 0

    def tearDown(self):
        del self.action_repository
