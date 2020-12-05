from functionalities.validation.exceptions import *
from interface.ui.colors import *


class UiBook:
    def __init__(self, book_service, rental_service, action_service):
        self._book_service = book_service
        self._action_service = action_service
        self._rental_service = rental_service

    def add(self):
        title = input("      Title:")
        author = input("      Author:")
        self._book_service.add_book(title, author)
        print_successful("Book successfully added.", "\n")

    def update(self):
        try:
            book_id = int(input("      Book ID:").strip())
        except ValueError:
            raise ValidError("Invalid Book ID!")
        new_title = input("      New title:")
        new_author = input("      New author:")
        self._book_service.update_book_by_book_id(book_id, new_title, new_author)
        print_successful("Book successfully updated.", "\n")

    def remove(self):
        try:
            book_id = int(input("      Book ID:").strip())
        except ValueError:
            raise ValidError("Invalid Book ID!")
        self._book_service.remove_book_by_book_id(book_id)
        self._rental_service.remove_rental_by_book_id(book_id)
        print_successful("Book successfully removed.", "\n")

    def list(self):
        books_list = self._book_service.get_all_books()
        for book in books_list:
            book_currently_rented = self._rental_service.get_book_rental_status(book.id)
            print(f"ID(", end="")
            print_orange(f"{book.id}", "")
            print("): '", end="")
            print_yellow(f"{book.title}", "")
            print("' by ", end="")
            print_orange(f"{book.author}", "")
            print(": ", end="")
            if book_currently_rented is None:
                book_currently_rented = "AVAILABLE"
                print_green(book_currently_rented, "\n")
            else:
                book_currently_rented = "UNAVAILABLE"
                print_red(book_currently_rented, "\n")


class UiClient:
    def __init__(self, client_service, rental_service, action_service):
        self._client_service = client_service
        self._rental_service = rental_service
        self._action_service = action_service

    def add(self):
        name = input("      Name:")
        self._client_service.add_client(name)
        print_successful("Client successfully added.", "\n")

    def update(self):
        try:
            client_id = int(input("      Client ID:").strip())
        except ValueError:
            raise ValidError("Invalid Client ID!")
        new_name = input("      New name:")
        self._client_service.update_client_by_client_id(client_id, new_name)
        print_successful("Client successfully updated.", "\n")

    def remove(self):
        try:
            client_id = int(input("      Client ID:").strip())
        except ValueError:
            raise ValidError("Invalid Client ID!")
        self._client_service.remove_client_by_client_id(client_id)
        self._rental_service.remove_rental_by_client_id(client_id)
        print_successful("Client successfully removed.", "\n")

    def list(self):
        clients_list = self._client_service.get_all_clients()
        for client in clients_list:
            client_current_rentals = self._rental_service.get_client_active_rentals(client.id)
            print(f"ID(", end="")
            print_orange(f"{client.id}", "")
            print("): '", end="")
            print_orange(f"{client.name}", "")
            print("' renting", end="")
            length_of_client_rentals = len(client_current_rentals)
            if length_of_client_rentals == 0:
                print(" no books.")
            else:
                print(" book:", end="")
                for index, book_id in enumerate(client_current_rentals):
                    if index != length_of_client_rentals - 1:
                        print_green(f" '{book_id}'", ",")
                    else:
                        print_green(f" '{book_id}'", ".\n")


class UiRental:
    def __init__(self, book_service, client_service, rental_service, action_service):
        self._book_service = book_service
        self._client_service = client_service
        self._rental_service = rental_service
        self._action_service = action_service

    def rent_book(self):
        book_id = input("   Book ID: ").strip()
        client_id = input("   Client ID: ").strip()
        self._rental_service.add_rental(book_id, client_id)
        print_successful("Book successfully rented.", "\n")

    def return_book(self):
        book_id = input("   Book ID:").strip()
        self._rental_service.return_rental_by_book_id(book_id)
        print_successful("Book successfully returned.", "\n")

    def get_all_rentals(self):
        rentals_list = self._rental_service.get_all_rentals()
        for index, rental in enumerate(rentals_list):
            print(rental.book_id, rental.client_id, rental.rented_date, rental.returned_date)


class UiSearch:
    def __init__(self, book_service, client_service, rental_service):
        self._book_service = book_service
        self._client_service = client_service
        self._rental_service = rental_service

    def search_client_by_id(self):
        client_id = input("Client ID=")
        try:
            if client_id == '':
                raise ValidError("Client ID must be completed!")
            client_id = int(client_id)
            if client_id < 0:
                raise ValueError()
        except ValueError:
            raise ValidError("Client ID must have a natural integer value.")

        list_of_matching_clients = self._client_service.find_all_clients_sharing_id_value(client_id)
        number_of_matching_clients = len(list_of_matching_clients)

        if number_of_matching_clients == 0:
            raise RepoError(f"No clients found by ID: {client_id}")

        self.print_client_list(list_of_matching_clients)

    def search_client_by_name(self):
        client_name = input("Client name=")
        if client_name == '':
            raise ValidError("Client name cannot be empty!")
        list_of_matching_clients = self._client_service.find_all_clients_sharing_name_value(client_name.lower())

        number_of_matching_clients = len(list_of_matching_clients)
        if number_of_matching_clients == 0:
            raise RepoError(f"No clients found by name: {client_name}")

        self.print_client_list(list_of_matching_clients)

    def print_client_list(self, client_list):
        for client in client_list:
            client_current_rentals = self._rental_service.get_client_active_rentals(client.id)
            print(f"ID(", end="")
            print_orange(f"{client.id}", "")
            print("): '", end="")
            print_orange(f"{client.name}", "")
            print("' renting", end="")
            length_of_client_rentals = len(client_current_rentals)
            if length_of_client_rentals == 0:
                print(" no books.")
            else:
                print(" book:", end="")
                for index, book_id in enumerate(client_current_rentals):
                    if index != length_of_client_rentals - 1:
                        print_green(f" '{book_id}'", ",")
                    else:
                        print_green(f" '{book_id}'", ".\n")

    def search_book_by_id(self):
        book_id = input("Book ID=")
        try:
            if book_id == '':
                raise ValidError("Book ID must be completed!")
            book_id = int(book_id)
            if book_id < 0:
                raise ValueError()
        except ValueError:
            raise ValidError("Book ID must have a natural integer value.")

        list_of_matching_books = self._book_service.find_all_books_with_id_containing_value(book_id)

        number_of_matching_books = len(list_of_matching_books)
        if number_of_matching_books == 0:
            raise RepoError(f"No books found by ID: {book_id}")

        for book in list_of_matching_books:
            book_currently_rented = self._rental_service.get_book_rental_status(book.id)
            print(f"{book.id} - '{book.title}' by {book.author}: ", end="")
            if book_currently_rented is None:
                book_currently_rented = "AVAILABLE"
                print_green(book_currently_rented, "\n")
            else:
                book_currently_rented = "UNAVAILABLE"
                print_red(book_currently_rented, "\n")

    def search_book_by_title(self):
        book_title = input("Book title=")
        list_of_matching_books = self._book_service.find_all_books_with_title_containing_string(book_title.lower())

        number_of_matching_books = len(list_of_matching_books)
        if number_of_matching_books == 0:
            raise RepoError(f"No books found by title: {book_title}")

        self.print_book_list(list_of_matching_books)

    def search_book_by_author(self):
        book_author = input("Book author=")
        list_of_matching_books = self._book_service.find_all_books_with_author_containing_string(book_author.lower())

        number_of_matching_books = len(list_of_matching_books)
        if number_of_matching_books == 0:
            raise RepoError(f"No books found by author: {book_author}")

        self.print_book_list(list_of_matching_books)

    def print_book_list(self, book_list):
        for book in book_list:
            book_currently_rented = self._rental_service.get_book_rental_status(book.id)
            print(f"ID(", end="")
            print_orange(f"{book.id}", "")
            print("): '", end="")
            print_yellow(f"{book.title}", "")
            print("' by ", end="")
            print_orange(f"{book.author}", "")
            print(": ", end="")
            if book_currently_rented is None:
                book_currently_rented = "AVAILABLE"
                print_green(book_currently_rented, "\n")
            else:
                book_currently_rented = "UNAVAILABLE"
                print_red(book_currently_rented, "\n")


class UiStatistics:
    def __init__(self, book_service, client_service, rental_service):
        self._book_service = book_service
        self._client_service = client_service
        self._rental_service = rental_service

    def get_most_active_clients(self):
        list_of_clients = self._rental_service.get_statistics_for_most_active_clients()
        previous_position, previous_amount = None, None
        for index, client in enumerate(list_of_clients):
            client_id = client["ID"]
            _, client_data = self._client_service.find_client_by_client_id(client_id)
            client_name = client_data.name
            if index == 0:
                print("#" + str(index + 1), end=" | ")
                previous_position = 1
            else:
                if previous_amount == client['Rental days']:
                    print("#" + str(previous_position), end=" | ")
                else:
                    print("#" + str(index + 1), end=" | ")
                    previous_position = index + 1
            print(f"ID(", end="")
            print_orange(f"{client_id}", "")
            print("): '", end="")
            print_orange(f"{client_name}", "")
            print("' renting for ", end="")
            print_orange(f"{client['Rental days']} days.", "\n")
            previous_amount = client['Rental days']

    def get_most_rented_books(self):
        list_of_books = self._rental_service.get_statistics_for_most_rented_books()
        previous_position, previous_amount = None, None
        for index, book in enumerate(list_of_books):
            if index == 0:
                print("#" + str(index + 1), end=" | '")
                previous_position = 1
            else:
                if previous_amount == book['Rental amount']:
                    print("#" + str(previous_position), end=" | '")
                else:
                    print("#" + str(index + 1), end=" | '")
                    previous_position = index + 1
            print_yellow(f"{book['Title']}", "")
            print("' by ", end="")
            print_orange(f"{book['Author']}", "")
            print(": rented ", end="")
            print_orange(f"{book['Rental amount']}", "")
            if book['Rental amount'] == 1:
                print(" time.", end="\n")
            else:
                print(" times.", end="\n")
            previous_amount = book['Rental amount']

    def get_most_rented_author(self):
        author = self._rental_service.get_most_rented_author()
        books_list = self._rental_service.get_list_of_books_of_most_rented_author(author)
        print_orange("Most rented author:", " ")
        print_successful(author["Name"], " - ")
        print_red(author["Rental amount"], " ")
        print_orange("rentals:", "\n")
        for book in books_list:
            print_orange("Title:", " ")
            print("'", end="")
            print_successful(book["Title"], "")
            print("'", end=" : ")
            print_red(book["Rental amount"], "")
            if book["Rental amount"] == 1:
                print_orange(f" time.", "\n")
            else:
                print_orange(f" times.", "\n")


class UiUndoRedo:
    def __init__(self, action_service):
        self._action_service = action_service

    def undo(self):
        self._action_service.undo()

    def redo(self):
        self._action_service.redo()


class Console:
    def __init__(self, book_service, client_service, rental_service, action_service):
        self._book_service = book_service
        self._client_service = client_service
        self._rental_service = rental_service
        self._action_service = action_service

        self._ui_book = UiBook(self._book_service, self._rental_service, self._action_service)
        self._ui_client = UiClient(self._client_service, self._rental_service, self._action_service)
        self._ui_rental = UiRental(self._book_service, self._client_service, self._rental_service, self._action_service)
        self._ui_search = UiSearch(self._book_service, self._client_service, self._rental_service)
        self._ui_statistics = UiStatistics(self._book_service, self._client_service, self._rental_service)
        self.__ui_undo_redo = UiUndoRedo(self._action_service)

        self._main_menu_commands = {
            1: {"description": "Manage entities", "function_name": self.__ui_get_clients_or_books_for_manage_command},
            2: {"description": "Manage rentals", "function_name": self.__ui_get_manage_rental_option},
            3: {"description": "List entities", "function_name": self.__ui_get_option_for_list_command},
            4: {"description": "Search entities", "function_name": self.__ui_get_option_for_search_command},
            5: {"description": "Create statistics", "function_name": self.__ui_get_option_for_statistics_option},
            6: {"description": "Undo", "function_name": self.__ui_undo_redo.undo},
            7: {"description": "Redo", "function_name": self.__ui_undo_redo.redo},
            0: {"description": "Exit application", "function_name": exit}
        }

    def __ui_get_clients_or_books_for_manage_command(self):
        manage_commands = {
            1: {"description": "Clients", "function_name": self.__ui_get_manage_client_option},
            2: {"description": "Books", "function_name": self.__ui_get_manage_book_option},
            0: {"description": "Back to main menu", "function_name": self.__ui_get_back_to_main_menu}
        }
        print("      MANAGE ")
        self.__ui_print_menu_commands_of(manage_commands)
        self.__ui_get_command_from(manage_commands)

    def __ui_get_manage_book_option(self):
        book_commands = {
            1: {"description": "Add book", "function_name": self._ui_book.add},
            2: {"description": "Update book", "function_name": self._ui_book.update},
            3: {"description": "Remove book", "function_name": self._ui_book.remove},
            0: {"description": "Back to main menu", "function_name": self.__ui_get_back_to_main_menu}
        }
        print("      BOOKS")
        self.__ui_print_menu_commands_of(book_commands)
        self.__ui_get_command_from(book_commands)

    def __ui_get_manage_client_option(self):
        client_commands = {
            1: {"description": "Add client", "function_name": self._ui_client.add},
            2: {"description": "Update client", "function_name": self._ui_client.update},
            3: {"description": "Remove client", "function_name": self._ui_client.remove},
            0: {"description": "Back to main menu", "function_name": self.__ui_get_back_to_main_menu}
        }
        print("      CLIENTS")
        self.__ui_print_menu_commands_of(client_commands)
        self.__ui_get_command_from(client_commands)

    def __ui_get_manage_rental_option(self):
        rental_menu_commands = {
            1: {"description": "Rent a book", "function_name": self._ui_rental.rent_book},
            2: {"description": "Return a book", "function_name": self._ui_rental.return_book},
            0: {"description": "Back to main menu", "function_name": self.__ui_get_back_to_main_menu}
        }
        print("    RENTALS")
        self.__ui_print_menu_commands_of(rental_menu_commands)
        self.__ui_get_command_from(rental_menu_commands)

    def __ui_get_option_for_list_command(self):
        list_commands = {
            1: {"description": "Clients", "function_name": self._ui_client.list},
            2: {"description": "Books", "function_name": self._ui_book.list},
            0: {"description": "Back to main menu", "function_name": self.__ui_get_back_to_main_menu}
        }
        print("      LIST")
        self.__ui_print_menu_commands_of(list_commands)
        self.__ui_get_command_from(list_commands)

    def __ui_get_option_for_statistics_option(self):
        statistics_commands = {
            1: {"description": "Most rented books", "function_name": self._ui_statistics.get_most_rented_books},
            2: {"description": "Most active clients", "function_name": self._ui_statistics.get_most_active_clients},
            3: {"description": "Most rented authors", "function_name": self._ui_statistics.get_most_rented_author},
            0: {"description": "Back to main menu", "function_name": self.__ui_get_back_to_main_menu}
        }
        print("      STATISTICS ")
        self.__ui_print_menu_commands_of(statistics_commands)
        self.__ui_get_command_from(statistics_commands)

    def __ui_get_option_for_search_command(self):
        search_commands = {
            1: {"description": "Clients", "function_name": self.__ui_get_option_for_search_client_command},
            2: {"description": "Books", "function_name": self.__ui_get_option_for_search_book_command},
            0: {"description": "Back to main menu", "function_name": self.__ui_get_back_to_main_menu}
        }
        print("      SEARCH ")
        self.__ui_print_menu_commands_of(search_commands)
        self.__ui_get_command_from(search_commands)

    def __ui_get_option_for_search_client_command(self):
        search_commands = {
            1: {"description": "ID", "function_name": self._ui_search.search_client_by_id},
            2: {"description": "Name", "function_name": self._ui_search.search_client_by_name},
            0: {"description": "Back to main menu", "function_name": self.__ui_get_back_to_main_menu}
        }
        print("      SEARCH BY ")
        self.__ui_print_menu_commands_of(search_commands)
        self.__ui_get_command_from(search_commands)

    def __ui_get_option_for_search_book_command(self):
        search_commands = {
            1: {"description": "ID", "function_name": self._ui_search.search_book_by_id},
            2: {"description": "Title", "function_name": self._ui_search.search_book_by_title},
            3: {"description": "Author", "function_name": self._ui_search.search_book_by_author},
            0: {"description": "Back to main menu", "function_name": self.__ui_get_back_to_main_menu}
        }
        print("      SEARCH BY ")
        self.__ui_print_menu_commands_of(search_commands)
        self.__ui_get_command_from(search_commands)

    @staticmethod
    def __ui_print_menu_commands_of(current_menu):
        for key in current_menu:
            print(key, current_menu[key]["description"])

    @staticmethod
    def __ui_get_command_from(current_menu):
        input_from_console = int(input(">"))
        try:
            command_key = int(input_from_console)
            if command_key in current_menu:
                command = current_menu[command_key]["function_name"]
                command()
            else:
                raise ValueError("Invalid menu option.")
        except ValueError:
            raise ValueError("Invalid menu option.")

    def __ui_get_back_to_main_menu(self):
        pass

    def run(self):
        while True:
            print("    MAIN MENU")
            self.__ui_print_menu_commands_of(self._main_menu_commands)
            try:
                self.__ui_get_command_from(self._main_menu_commands)
            except ValueError as value_error:
                print_error(value_error, "\n")
            except TypeError:
                raise ValueError()
            except ValidError as valid_error:
                print_error(valid_error, "\n")
            except RepoError as repo_error:
                print_error(repo_error, "\n")
            print()
