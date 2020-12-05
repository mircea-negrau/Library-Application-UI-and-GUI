from domain.entities.book_entity import Book
from domain.entities.client_entity import Client
from domain.entities.rental_entity import Rental
from domain.repositories.binaryfiles.book_repository import BookBinaryRepository
from domain.repositories.binaryfiles.client_repository import ClientBinaryRepository
from domain.repositories.binaryfiles.rental_repository import RentalBinaryRepository
from domain.repositories.inmemory.action_repository import ActionRepository
from domain.repositories.inmemory.book_repository import BookRepository
from domain.repositories.inmemory.client_repository import ClientRepository
from domain.repositories.inmemory.rental_repository import RentalRepository
from domain.repositories.jsonfiles.book_repository import BookJsonRepository
from domain.repositories.jsonfiles.client_repository import ClientJsonRepository
from domain.repositories.jsonfiles.rental_repository import RentalJsonRepository
from domain.repositories.textfiles.book_repository import BookTextRepository
from domain.repositories.textfiles.client_repository import ClientTextRepository
from domain.repositories.textfiles.rental_repository import RentalTextRepository
from functionalities.generators.populate_repositories import populate_book_repository, populate_rental_repository, \
    populate_client_repository
from functionalities.services.action_service import ActionService
from functionalities.services.book_service import BookService
from functionalities.services.client_service import ClientService
from functionalities.services.rental_service import RentalService
from functionalities.validation.validators import BookValidator, RentalValidator, ClientValidator
from interface.gui.interface import GUI
from interface.ui.console import Console


class Program:
    def __init__(self):
        self.repository_type, self.action_repository = None, None
        self.book_repository, self.client_repository, self.rental_repository = None, None, None
        self.action_service, self.book_service, self.rental_service, self.client_service = None, None, None, None
        self.book_validator, self.client_validator, self.rental_validator = None, None, None
        self.repository = None
        self.populate = None
        self.interface = None
        self.settings()

    def settings(self):
        self.get_settings()
        self.configure_validators()
        self.configure_repositories()
        self.configure_services()
        self.configure_interface()

    def run(self):
        self.interface.run()

    def configure_validators(self):
        self.book_validator = BookValidator()
        self.client_validator = ClientValidator()
        self.rental_validator = RentalValidator()

    def configure_repositories(self):
        if self.repository_type == "inmemory":
            self.book_repository = BookRepository()
            self.client_repository = ClientRepository()
            self.rental_repository = RentalRepository()
        elif self.repository_type == "textfiles":
            self.book_repository = BookTextRepository(self.book_repository, Book.string_read_book,
                                                      Book.string_write_book)
            self.client_repository = ClientTextRepository(self.client_repository, Client.read_client,
                                                          Client.write_client)
            self.rental_repository = RentalTextRepository(self.rental_repository, Rental.string_read_rental,
                                                          Rental.string_write_rental)
        elif self.repository_type == "binaryfiles":
            self.book_repository = BookBinaryRepository(self.book_repository)
            self.client_repository = ClientBinaryRepository(self.client_repository)
            self.rental_repository = RentalBinaryRepository(self.rental_repository)
        elif self.repository_type == "jsonfiles":
            self.book_repository = BookJsonRepository(self.book_repository, Book.json_read_book, Book.json_write_book)
            self.client_repository = ClientJsonRepository(self.client_repository, Client.json_read_client,
                                                          Client.json_write_client)
            self.rental_repository = RentalJsonRepository(self.rental_repository, Rental.json_read_rental,
                                                          Rental.json_write_rental)
        self.action_repository = ActionRepository()

    def configure_services(self):
        self.action_service = ActionService(self.action_repository, self.book_repository, self.client_repository,
                                            self.rental_repository)
        self.book_service = BookService(self.action_service, self.book_repository, self.book_validator)
        self.client_service = ClientService(self.action_service, self.client_repository, self.client_validator)
        self.rental_service = RentalService(self.action_service, self.book_repository, self.client_repository,
                                            self.rental_repository,
                                            self.book_validator, self.client_validator, self.rental_validator)

    def configure_interface(self):
        if self.interface == "UI":
            self.interface = Console(self.book_service, self.client_service, self.rental_service, self.action_service)
            self.configure_initial_population()
        elif self.interface == "GUI":
            self.interface = GUI(self.book_service, self.client_service, self.rental_service, self.action_service)
            self.configure_initial_population()

    def configure_initial_population(self):
        if self.populate.lower() == "true":
            populate_book_repository(self.book_service)
            populate_client_repository(self.client_service)
            populate_rental_repository(self.rental_service)

    def get_settings(self):
        with open("setup/settings.properties", "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip(' ').split()
                if line != "":
                    setting = line[0]
                    value = line[2].strip('"')
                    if setting.lower() == "repository":
                        self.repository_type = value
                    elif setting.lower() == "books":
                        self.book_repository = "data\\" + value
                    elif setting.lower() == "clients":
                        self.client_repository = "data\\" + value
                    elif setting.lower() == "rentals":
                        self.rental_repository = "data\\" + value
                    elif setting.lower() == "interface":
                        self.interface = value.strip('"').upper()
                    elif setting.lower() == "populate":
                        self.populate = value
