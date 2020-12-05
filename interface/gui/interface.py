import sys
from PyQt5 import QtWidgets
from interface.gui.windows import *


class GUI:
    def __init__(self, book_service, client_service, rental_service, action_service):
        self._book_service = book_service
        self._client_service = client_service
        self._rental_service = rental_service
        self._action_service = action_service

    def run(self):
        app = QtWidgets.QApplication(sys.argv)
        controller = Controller(self._book_service, self._client_service, self._rental_service, self._action_service)
        controller.show_main()
        sys.exit(app.exec_())


class Controller:
    def __init__(self, book_service, client_service, rental_service, action_service):
        self._book_service = book_service
        self._client_service = client_service
        self._rental_service = rental_service
        self._action_service = action_service
        self.create_windows()
        self.create_connectors()

    def create_windows(self):
        self.create_main_menus()
        self.create_book_menus()
        self.create_client_menus()
        self.create_rental_menus()

    def create_main_menus(self):
        self.window_main_menu = WindowMainMenu(self._action_service)
        self.window_manage_entities = WindowManageEntitiesChoice()
        self.window_manage_rentals = WindowManageRentals()
        self.window_list_entities = WindowListEntities()
        self.window_search_entities = WindowSearchEntities()
        self.window_statistics = WindowStatistics(self._client_service, self._rental_service)

    def create_book_menus(self):
        self.window_manage_books = WindowManageBooks()
        self.window_add_books = WindowAddBooks(self._book_service)
        self.window_update_books = WindowUpdateBooks(self._book_service)
        self.window_remove_books = WindowRemoveBooks(self._book_service, self._rental_service)
        self.window_list_books = WindowListBooks(self._book_service, self._rental_service)
        self.window_search_books = WindowSearchBooks(self._book_service, self._rental_service)

    def create_client_menus(self):
        self.window_manage_clients = WindowManageClients()
        self.window_add_clients = WindowAddClients(self._client_service)
        self.window_update_clients = WindowUpdateClients(self._client_service)
        self.window_remove_clients = WindowRemoveClients(self._client_service, self._rental_service)
        self.window_list_clients = WindowListClients(self._client_service, self._rental_service)
        self.window_search_clients = WindowSearchClients(self._client_service, self._rental_service)

    def create_rental_menus(self):
        self.window_rent_book = WindowRentBook(self._rental_service)
        self.window_return_book = WindowReturnBook(self._rental_service)

    def create_connectors(self):
        self.window_main_menu.switch_to_manage_entities.connect(self.show_manage_entities)
        self.window_manage_entities.switch_to_manage_books.connect(self.show_manage_books)
        self.window_manage_entities.switch_to_manage_clients.connect(self.show_manage_clients)
        self.window_main_menu.switch_to_manage_rentals.connect(self.show_manage_rentals)
        self.window_main_menu.switch_to_list_entities.connect(self.show_list_entities)
        self.window_main_menu.switch_to_search_entities.connect(self.show_search_entities)
        self.window_main_menu.switch_to_statistics.connect(self.show_statistics)

        self.window_manage_books.switch_to_add_books.connect(self.show_add_books)
        self.window_manage_clients.switch_to_add_clients.connect(self.show_add_clients)
        self.window_manage_books.switch_to_update_books.connect(self.show_update_books)
        self.window_manage_clients.switch_to_update_clients.connect(self.show_update_clients)
        self.window_manage_books.switch_to_remove_books.connect(self.show_remove_books)
        self.window_manage_clients.switch_to_remove_clients.connect(self.show_remove_clients)

        self.window_list_entities.switch_to_list_books.connect(self.show_list_books)
        self.window_list_entities.switch_to_list_clients.connect(self.show_list_clients)

        self.window_manage_rentals.switch_to_rent.connect(self.show_rent_book)
        self.window_manage_rentals.switch_to_return.connect(self.show_return_book)

        self.window_search_entities.switch_to_search_books.connect(self.show_search_books)
        self.window_search_entities.switch_to_search_clients.connect(self.show_search_clients)

        self.window_manage_entities.switch_to_main_menu.connect(self.back_to_main_menu)
        self.window_manage_books.switch_to_main_menu.connect(self.back_to_main_menu)
        self.window_add_books.switch_to_main_menu.connect(self.back_to_main_menu)
        self.window_update_books.switch_to_main_menu.connect(self.back_to_main_menu)
        self.window_remove_books.switch_to_main_menu.connect(self.back_to_main_menu)
        self.window_manage_clients.switch_to_main_menu.connect(self.back_to_main_menu)
        self.window_add_clients.switch_to_main_menu.connect(self.back_to_main_menu)
        self.window_update_clients.switch_to_main_menu.connect(self.back_to_main_menu)
        self.window_remove_clients.switch_to_main_menu.connect(self.back_to_main_menu)
        self.window_list_entities.switch_to_main_menu.connect(self.back_to_main_menu)
        self.window_list_books.switch_to_main_menu.connect(self.back_to_main_menu)
        self.window_list_clients.switch_to_main_menu.connect(self.back_to_main_menu)
        self.window_statistics.switch_to_main_menu.connect(self.back_to_main_menu)
        self.window_search_entities.switch_to_main_menu.connect(self.back_to_main_menu)
        self.window_manage_rentals.switch_to_main_menu.connect(self.back_to_main_menu)
        self.window_return_book.switch_to_main_menu.connect(self.back_to_main_menu)
        self.window_rent_book.switch_to_main_menu.connect(self.back_to_main_menu)
        self.window_search_books.switch_to_main_menu.connect(self.back_to_main_menu)
        self.window_search_clients.switch_to_main_menu.connect(self.back_to_main_menu)

    def show_main(self):
        self.window_main_menu.show()

    def show_manage_entities(self):
        self.window_manage_entities.show()
        self.window_main_menu.close()

    def show_rent_book(self):
        self.window_rent_book.show()
        self.window_manage_rentals.close()

    def show_return_book(self):
        self.window_return_book.show()
        self.window_manage_rentals.close()

    def show_manage_books(self):
        self.window_manage_books.show()
        self.window_manage_entities.close()

    def show_add_books(self):
        self.window_add_books.show()
        self.window_manage_books.close()

    def show_update_books(self):
        self.window_update_books.show()
        self.window_manage_books.close()

    def show_remove_books(self):
        self.window_remove_books.show()
        self.window_manage_books.close()

    def show_manage_clients(self):
        self.window_manage_clients.show()
        self.window_manage_entities.close()

    def show_add_clients(self):
        self.window_add_clients.show()
        self.window_manage_clients.close()

    def show_update_clients(self):
        self.window_update_clients.show()
        self.window_manage_clients.close()

    def show_remove_clients(self):
        self.window_remove_clients.show()
        self.window_manage_clients.close()

    def show_manage_rentals(self):
        self.window_manage_rentals.show()
        self.window_main_menu.close()

    def show_list_entities(self):
        self.window_list_entities.show()
        self.window_main_menu.close()

    def show_list_books(self):
        self.window_list_books.update_table()
        self.window_list_books.show()
        self.window_list_entities.close()

    def show_list_clients(self):
        self.window_list_clients.update_table()
        self.window_list_clients.show()
        self.window_list_entities.close()

    def show_search_entities(self):
        self.window_search_entities.show()
        self.window_main_menu.close()

    def show_search_books(self):
        self.window_search_books.show()
        self.window_search_entities.close()

    def show_search_clients(self):
        self.window_search_clients.show()
        self.window_search_entities.close()

    def show_statistics(self):
        self.window_statistics.show()
        self.window_main_menu.close()

    def back_to_main_menu(self, close_previous_page):
        self.show_main()
        exec(close_previous_page)
