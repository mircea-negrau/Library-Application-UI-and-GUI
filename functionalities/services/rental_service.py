from datetime import date

from domain.entities.rental_entity import Rental
from functionalities.validation.exceptions import RepoError, ValidError


class RentalService:
    def __init__(self, action_service, book_repository, client_repository, rental_repository,
                 book_validator, client_validator, rental_validator):
        self._book_repository = book_repository
        self._client_repository = client_repository
        self._rental_repository = rental_repository

        self._book_validator = book_validator
        self._client_validator = client_validator
        self._rental_validator = rental_validator

        self._action_service = action_service

    def add_rental(self, book_id, client_id):
        """
        Function to add a rental to the rental repository with the book and client IDs given by the parameters. The
        function creates a new 'Rental' entity which then passes through the 'RentalValidator'. In case any of the
        rental's parameters are incorrect, the rental is not added but an error is raised instead. Otherwise, the
        function checks whether the book is available for rent. If it is not, then no rental is added but an error is
        raised instead. Otherwise, the rental is added to the rental repository.
        :param book_id: integer, holds the ID value of the book that is rented.
        :param client_id: integer, holds the ID value of the client that rents the book.
        """
        self._rental_validator.validate_book_and_client_ids(book_id, client_id)

        book_id = int(book_id)
        client_id = int(client_id)

        is_valid_book = self.is_book_id_in_repository(book_id)
        is_valid_client = self.is_client_id_in_repository(client_id)
        is_available_book = self.is_book_available_by_book_id(book_id)

        if is_valid_book:
            if is_valid_client:
                if is_available_book:
                    rental_id = self._rental_repository.get_next_rental_id()
                    rented_date = date.today()
                    returned_date = None
                    rental = Rental(rental_id, book_id, client_id, rented_date, returned_date)
                    self._rental_validator.validate_rental(rental)
                    self._rental_repository.add_rental(rental)
                    self._action_service.push_add_action_to_undo_list(rental)
                else:
                    raise RepoError("Book is currently rented. ")
            else:
                raise RepoError("Client ID not found. ")
        else:
            raise RepoError("Book ID not found. ")

    def return_rental_by_id(self, rental_id):
        """
        Function to return a rental by the 'rental_id'. The function verifies if the 'rental_id' is valid. If it is not,
        then no rental is returned but an error is raised instead. Otherwise, the function searches for the rental in
        the rental repository. If no rental is found, no rental is returned but an error is raised instead. Otherwise,
        the rental is marked as returned with the current date as the 'returned_date'.
        :param rental_id: integer, holds the ID of the rental to be returned.
        """
        try:
            rental_id = int(rental_id)
        except ValueError:
            raise ValidError("Rental ID must have natural number value. ")
        rental_index, rental = self.find_rental_index_by_id(rental_id)
        if rental_index is None:
            raise RepoError("Rental ID not found. ")
        today = date.today()
        new_rental = Rental(rental.id, rental.book_id, rental.client_id, rental.rented_date, date.today())
        self._action_service.push_update_action_to_undo_list(rental, new_rental)
        self._rental_repository.update_rental_return_by_index(rental_index, today)

    def return_rental_by_book_id(self, book_id):
        """
        Function to return the rental by the 'book_id'. The function verifies if the 'book_id' is valid. If it is not,
        then no rental is returned but an error is raised instead. Otherwise, the function searches for the book in the
        book repository. If no book is found, no rental is returned but an error is raised instead. Otherwise, the ID of
        rental of the book is looked for. If no rental ID is found active for the book at the moment, no rental is
        returned but an error is raised instead. Otherwise, the rental is marked as returned with the 'returned_date' of
        today.
        :param book_id: integer, holds the ID of the book whose rental will be returned.
        """
        self._rental_validator.validate_book_and_client_ids(book_id, 5)
        book_id = int(book_id)

        is_valid_book = self.is_book_id_in_repository(book_id)
        if not is_valid_book:
            raise RepoError("Book ID not found. ")

        rental_id = self.find_active_rental_id_by_book_id(book_id)
        if rental_id is None:
            raise RepoError("Book is not rented. ")

        self.return_rental_by_id(rental_id)

    def remove_rental_by_book_id(self, book_id):
        """
        Function to remove the rental found in the rental repository that is identified by the 'book_id' given by the
        function's parameter. If no book is found by the given book ID, nothing is done.
        If no rented book matching the book ID is found, nothing is done. Otherwise, the rental found is deleted.
        :param book_id: integer, holds the value of the ID of the rental's book. Should be a natural integer.
        """
        book_id = int(book_id)
        while True:
            rental_id = self.find_rental_id_by_book_id(book_id)
            if rental_id is None:
                return
            rental_index, rental = self.find_rental_index_by_id(rental_id)
            self._rental_repository.remove_rental_by_index(rental_index)
            self._action_service.push_consecutive_indirect_remove_action_to_undo_list(rental)

    def remove_rental_by_client_id(self, client_id):
        """
        Function to remove the rental found in the rental repository that is identified by the 'client_id' given by the
        function's parameter. If no client is found by the given client ID, nothing is done.
        If no client renting books matching the client ID is found, nothing is done. Otherwise, while the client is
        still found in the rental repository, the function searches and removes every rental linked to the client.
        :param client_id: integer, holds the value of the ID of the rental's client. Should be a natural integer.
        """
        client_id = int(client_id)
        while True:
            rental_id = self.find_rental_id_by_client_id(client_id)
            if rental_id is None:
                break
            rental_index, rental = self.find_rental_index_by_id(rental_id)
            self._rental_repository.remove_rental_by_index(rental_index)
            self._action_service.push_consecutive_indirect_remove_action_to_undo_list(rental)

    def find_active_rental_id_by_book_id(self, book_id):
        """
        Function to search for a 'rental_id' being given the 'book_id' of the rental. If the active rental having the
        'book_id' value as the given parameter is found, the function returns the ID of the rental. Otherwise, it
        returns None.
        :param book_id: integer, holds the ID value of the rental's 'book_id'.
        :return: If rental is found, it returns the rental's ID. Otherwise, it returns None.
        """
        rentals_list = self._rental_repository.get_all_rentals()
        for rental in rentals_list:
            if rental.book_id == book_id and rental.returned_date is None:
                return rental.id
        return None

    def find_rental_id_by_book_id(self, book_id):
        """
        Function to search for a 'rental_id' being given the 'book_id' of the rental. If the rental having the
        'book_id' value as the given parameter is found, the function returns the ID of the rental. Otherwise, it
        returns None.
        :param book_id: integer, holds the ID value of the rental's 'book_id'.
        :return: If rental is found, it returns the rental's ID. Otherwise, it returns None.
        """
        rentals_list = self._rental_repository.get_all_rentals()
        for rental in rentals_list:
            if rental.book_id == book_id:
                return rental.id
        return None

    def find_rental_id_by_client_id(self, client_id):
        """
        Function to search for a 'rental_id' being given the 'client_id' of the rental. If the active rental having the
        'book_id' value as the given parameter is found, the function returns the ID of the rental. Otherwise, it
        returns None.
        :param client_id: integer, holds the ID value of the rental's 'book_id'.
        :return: If rental is found, it returns the rental's ID. Otherwise, it returns None.
        """
        rentals_list = self._rental_repository.get_all_rentals()
        for rental in rentals_list:
            if rental.client_id == client_id:
                return rental.id
        return None

    def find_rental_index_by_id(self, rental_id):
        """
        Function to search for the index of the rental being given the 'rental_id' of it. If the active rental with
        'rental_id' value as the given parameter is found, the function returns the index of the rental. Otherwise, it
        returns None.
        :param rental_id: integer, holds the ID value of the rental.
        :return: If rental is found, it returns the rental's index. Otherwise, it returns None.
        """
        rentals_list = self._rental_repository.get_all_rentals()
        for index, rental in enumerate(rentals_list):
            if rental.id == rental_id:
                return index, rental
        return None, None

    def is_book_available_by_book_id(self, book_id):
        """
        Function to return whether or not a book from the book repository is currently available for rent or not.
        If a book having the book_id value as the given parameter is found having the 'returned_date' as None, it means
        that the book is currently rented already, so the function returns that the book's availability is False.
        Otherwise, it returns True.
        :param book_id: integer, holds the ID value of the book to be checked if available in the book repository.
        :return: True/False, whether or not the book having the 'book_id' given by the parameter is available or not.
        """
        rentals_list = self._rental_repository.get_all_rentals()
        for rental in rentals_list:
            if rental.book_id == book_id and rental.returned_date is None:
                return False
        return True

    def is_book_id_in_repository(self, book_id):
        """
        Function to return whether or not a book having the 'book_id' as the given parameter is found in the book
        repository.
        :param book_id: integer, holds the ID value of the book to be looked for in the repository.
        :return: True/False, whether or not the book having the 'book_id' given by the parameter is found or not.
        """
        books_list = self._book_repository.get_all_books()
        for book in books_list:
            if book.id == book_id:
                return True
        return False

    def is_client_id_in_repository(self, client_id):
        """
        Function to return whether or not a book having the 'client_id' as the given parameter is found in the book
        repository.
        :param client_id: integer, holds the ID value of the client to be looked for in the repository.
        :return: True/False, whether or not the book having the 'client_id' given by the parameter is found or not.
        """
        clients_list = self._client_repository.get_all_clients()
        for client in clients_list:
            if client.id == client_id:
                return True
        return False

    def get_client_active_rentals(self, client_id):
        """
        Function to get the full list of active rentals found in the rental repository appointed to the client holding
        the 'client_id' as the given parameter.
        :param client_id: integer, holds the ID value of the client whose active rentals will be searched for.
        :return: list, all the active rentals found in the rental repository appointed to the given client.
        """
        rentals_list = self._rental_repository.get_all_rentals()
        client_active_rentals_list = []
        for rental in rentals_list:
            if rental.client_id == client_id and rental.returned_date is None:
                client_active_rentals_list.append(rental.book_id)
        return client_active_rentals_list[:]

    def get_book_rental_status(self, book_id):
        """
        Function to return the ID of the client that currently rents the book having the 'book_id' as the given
        parameter. If no rental is found, the function returns None. Otherwise, the function returns the ID of the
        client.
        :param book_id: integer, holds the ID value of the book to be looked for in the active rentals from the
        rentals repository.
        :return: the ID of the client that currently rents the book, otherwise None
        """
        rentals_list = self._rental_repository.get_all_rentals()
        for rental in rentals_list:
            if rental.book_id == book_id and rental.returned_date is None:
                return rental.client_id
        return None

    def get_statistics_for_most_active_clients(self):
        """
        Function to return the list of most active clients, according to how many days in total they have rented books
        for in the book repository.
        :return: list, containing the most active clients sorted in descending order
        """
        clients_list = self.get_list_of_most_active_clients()
        clients_list = self.get_list_sorted_descending(clients_list, "Rental days")
        return clients_list

    def get_list_of_most_active_clients(self):
        """
        Function to return the list of clients that have rentals in rental repository. The list contains the client's ID
        and the number of days they have rented books for in total.
        :return: list, containing the list of clients found to have rented books in the rental repository.
        """
        rentals_list = self._rental_repository.get_all_rentals()
        clients_list = []
        for rental in rentals_list:
            is_client_in_list = False
            for client in clients_list:
                if client["ID"] == rental.client_id:
                    is_client_in_list = True
                    rental_period = self.get_spent_days_of_rental(rental.rented_date, rental.returned_date)
                    client["Rental days"] += int(rental_period)
                    break
            if not is_client_in_list:
                clients_list.append({"ID": rental.client_id, "Rental days": 1})
        return clients_list

    def get_statistics_for_most_rented_books(self):
        """
        Function to return the list of books sorted by the amount of times they were rented, according to the
        information found in the rental repository. The list is sorted in descending order, filtered by the amount of
        rentals.
        :return: list, containing the most rented books sorted in descending order
        """
        list_of_books = self.get_list_of_most_rented_books()
        list_of_books = self.get_list_sorted_descending(list_of_books, "Rental amount")
        return list_of_books

    def get_list_of_most_rented_books(self):
        """
        Function to return the list of books found to be rented in the rental repository. The list contains the title
        and author of the book and the amount of times the book has been rented.
        :return: list, containing the books found to have been rented in the rental repository.
        """
        rentals_list = self._rental_repository.get_all_rentals()
        list_of_books = []
        for rental in rentals_list:
            is_book_in_list = False
            rental_book = self.get_book_by_book_id(rental.book_id)
            for book in list_of_books:
                if book["Title"] == rental_book.title and book["Author"] == rental_book.author:
                    is_book_in_list = True
                    book["Rental amount"] += 1
                    break
            if not is_book_in_list:
                list_of_books.append({"Title": rental_book.title, "Author": rental_book.author, "Rental amount": 1})
        return list_of_books

    def get_most_rented_author(self):
        """
        Function to return the most rented author from the list of authors. The list of authors is composed of the
        authors found to have books that were rented in the rental repository. The amount of times their books were
        rented is the filter applied to order the authors.
        :return: dictionary, holding the name and amount of rentals that the most rented author has.
        """
        rentals_list = self._rental_repository.get_all_rentals()
        list_of_authors = []
        for rental in rentals_list:
            rented_book = self.get_book_by_book_id(rental.book_id)
            rented_book_author = rented_book.author
            is_author_in_list = False
            for author in list_of_authors:
                if author["Name"] == rented_book_author:
                    is_author_in_list = True
                    author["Rental amount"] += 1
                    break
            if not is_author_in_list:
                list_of_authors.append({"Name": rented_book_author, "Rental amount": 1})
        list_of_authors = self.get_list_sorted_descending(list_of_authors, "Rental amount")
        if len(list_of_authors) != 0:
            most_rented_author = list_of_authors[0]
        else:
            most_rented_author = None
        return most_rented_author

    def get_list_of_books_of_most_rented_author(self, author):
        """
        Function to return the list of books that share the 'author' as the value given by the parameter. The list gets
        returned sorted in descending order, filtered by the amount of times each book was rented.
        :param author: string, contains the exact value that books must have as their 'author'.
        :return: list, containing "Title" and "Rental amount" for each book authored by the given author.
        """
        rentals_list = self._rental_repository.get_all_rentals()
        list_of_books = []
        for rental in rentals_list:
            is_book_in_list = False
            rental_book = self.get_book_by_book_id(rental.book_id)
            if rental_book.author == author["Name"]:
                for book in list_of_books:
                    if book["Title"] == rental_book.title:
                        is_book_in_list = True
                        book["Rental amount"] += 1
                        break
                if not is_book_in_list:
                    list_of_books.append({"Title": rental_book.title, "Rental amount": 1})

        list_of_books = self.get_list_sorted_descending(list_of_books, "Rental amount")
        return list_of_books

    def get_book_by_book_id(self, book_id):
        """
        Function to return the book from the book repository that matches the 'book_id' value as the one received by the
        function's parameter. If no books are found, the function returns None.
        :param book_id: integer, holds the value of the ID for the book be returned
        :return: book entity, matching the ID. If none found, 'None' is returned
        """
        books_list = self._book_repository.get_all_books()
        for book in books_list:
            if book.id == book_id:
                return book
        return None

    @staticmethod
    def get_spent_days_of_rental(rented_date, returned_date):
        """
        Function to calculate the amount of days the book has been rented for. If the book has not been yet returned,
        the method calculates how many days have elapsed since renting it, counting the returned date as the current day
        :param rented_date: date, the date the book has been rented.
        :param returned_date: date, the date the book has been returned. Can be None.
        :return: integer, the amount of days the rental took place.
        """
        if returned_date is None:
            returned_date = date.today()
        rental_time = returned_date - rented_date
        return rental_time.days + 1

    @staticmethod
    def get_list_sorted_descending(list_to_sort, key):
        return sorted(list_to_sort, key=lambda list_element: list_element[key], reverse=True)