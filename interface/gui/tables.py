from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidget, QMessageBox


class ListBooksTableWidget(QTableWidget):
    def __init__(self, book_service, rental_service):
        super().__init__(0, 0)
        self._book_service = book_service
        self._rental_service = rental_service

        self.setColumnCount(4)
        self.setColumnWidth(1, 150)
        self.setColumnWidth(2, 150)

    def add_row(self):
        self.insertRow(1)

    def update_table(self):
        self.clear()
        self.setHorizontalHeaderLabels(["ID", "Title", "Author", "Status"])
        books_list = self._book_service.get_all_books()
        self.setRowCount(len(books_list))
        for index, book in enumerate(books_list):
            book_currently_rented = self._rental_service.get_book_rental_status(book.id)
            if book_currently_rented is None:
                book_currently_rented = "AVAILABLE"
            else:
                book_currently_rented = "UNAVAILABLE"
            self.setItem(index, 0, QtWidgets.QTableWidgetItem(str(book.id)))
            self.setItem(index, 1, QtWidgets.QTableWidgetItem(book.title))
            self.setItem(index, 2, QtWidgets.QTableWidgetItem(book.author))
            self.setItem(index, 3, QtWidgets.QTableWidgetItem(book_currently_rented))


class ListClientsTableWidget(QTableWidget):
    def __init__(self, client_service, rental_service):
        super().__init__(0, 0)
        self._client_service = client_service
        self._rental_service = rental_service

        self.setColumnCount(3)
        self.setColumnWidth(1, 150)

    def add_row(self):
        self.insertRow(1)

    def update_table(self):
        self.clear()
        self.setHorizontalHeaderLabels(["ID", "Name", "Active rentals"])
        clients_list = self._client_service.get_all_clients()
        self.setRowCount(len(clients_list))
        for index, client in enumerate(clients_list):
            client_current_rentals = self._rental_service.get_client_active_rentals(client.id)
            length_of_client_rentals = len(client_current_rentals)
            self.setItem(index, 0, QtWidgets.QTableWidgetItem(str(client.id)))
            self.setItem(index, 1, QtWidgets.QTableWidgetItem(client.name))
            self.setItem(index, 2, QtWidgets.QTableWidgetItem(str(length_of_client_rentals)))


class SearchBooksTableWidget(QTableWidget):
    def __init__(self, book_service, rental_service):
        super().__init__(0, 0)
        self._book_service = book_service
        self._rental_service = rental_service
        self.update_table()

    def update_table(self):
        self.clear()
        self.setColumnCount(4)
        self.setColumnWidth(1, 150)
        self.setHorizontalHeaderLabels(["ID", "Title", "Author", "Status"])

    def filter_by_id(self, book_id):
        self.update_table()
        list_of_matching_books = self._book_service.find_all_books_with_id_containing_value(int(book_id))
        self.setRowCount(len(list_of_matching_books))
        for index, book in enumerate(list_of_matching_books):
            book_currently_rented = self._rental_service.get_book_rental_status(book.id)
            if book_currently_rented is None:
                book_currently_rented = "AVAILABLE"
            else:
                book_currently_rented = "UNAVAILABLE"
            self.setItem(index, 0, QtWidgets.QTableWidgetItem(str(book.id)))
            self.setItem(index, 1, QtWidgets.QTableWidgetItem(book.title))
            self.setItem(index, 2, QtWidgets.QTableWidgetItem(book.author))
            self.setItem(index, 3, QtWidgets.QTableWidgetItem(book_currently_rented))

    def filter_by_title(self, title):
        self.update_table()
        list_of_matching_books = self._book_service.find_all_books_with_title_containing_string(str(title))
        self.setRowCount(len(list_of_matching_books))
        for index, book in enumerate(list_of_matching_books):
            book_currently_rented = self._rental_service.get_book_rental_status(book.id)
            if book_currently_rented is None:
                book_currently_rented = "AVAILABLE"
            else:
                book_currently_rented = "UNAVAILABLE"
            self.setItem(index, 0, QtWidgets.QTableWidgetItem(str(book.id)))
            self.setItem(index, 1, QtWidgets.QTableWidgetItem(book.title))
            self.setItem(index, 2, QtWidgets.QTableWidgetItem(book.author))
            self.setItem(index, 3, QtWidgets.QTableWidgetItem(book_currently_rented))

    def filter_by_author(self, author):
        self.update_table()
        list_of_matching_books = self._book_service.find_all_books_with_author_containing_string(str(author))
        self.setRowCount(len(list_of_matching_books))
        for index, book in enumerate(list_of_matching_books):
            book_currently_rented = self._rental_service.get_book_rental_status(book.id)
            if book_currently_rented is None:
                book_currently_rented = "AVAILABLE"
            else:
                book_currently_rented = "UNAVAILABLE"
            self.setItem(index, 0, QtWidgets.QTableWidgetItem(str(book.id)))
            self.setItem(index, 1, QtWidgets.QTableWidgetItem(book.title))
            self.setItem(index, 2, QtWidgets.QTableWidgetItem(book.author))
            self.setItem(index, 3, QtWidgets.QTableWidgetItem(book_currently_rented))


class SearchClientsTableWidget(QTableWidget):
    def __init__(self, client_service, rental_service):
        super().__init__(0, 0)
        self._client_service = client_service
        self._rental_service = rental_service
        self.update_table()

    def update_table(self):
        self.clear()
        self.setColumnCount(3)
        self.setColumnWidth(1, 150)
        self.setHorizontalHeaderLabels(["ID", "Name", "Active rentals"])

    def filter_by_id(self, client_id):
        self.update_table()
        list_of_matching_clients = self._client_service.find_all_clients_sharing_id_value(int(client_id))
        self.setRowCount(len(list_of_matching_clients))
        for index, client in enumerate(list_of_matching_clients):
            client_current_rentals = self._rental_service.get_client_active_rentals(client.id)
            self.setItem(index, 0, QtWidgets.QTableWidgetItem(str(client.id)))
            self.setItem(index, 1, QtWidgets.QTableWidgetItem(client.name))
            self.setItem(index, 3, QtWidgets.QTableWidgetItem(len(client_current_rentals)))

    def filter_by_name(self, name):
        self.update_table()
        list_of_matching_clients = self._client_service.find_all_clients_sharing_name_value(str(name))
        self.setRowCount(len(list_of_matching_clients))
        for index, client in enumerate(list_of_matching_clients):
            client_current_rentals = self._rental_service.get_client_active_rentals(client.id)
            self.setItem(index, 0, QtWidgets.QTableWidgetItem(str(client.id)))
            self.setItem(index, 1, QtWidgets.QTableWidgetItem(client.name))
            self.setItem(index, 3, QtWidgets.QTableWidgetItem(len(client_current_rentals)))


class StatisticsTableWidget(QTableWidget):
    def __init__(self, client_service, rental_service):
        super().__init__(0, 0)
        self._client_service = client_service
        self._rental_service = rental_service
        self.update_table()

    def update_table(self):
        self.clear()
        self.setColumnWidth(1, 150)

    def get_most_active_clients(self):
        self.update_table()
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["Rank", "ID", "Name", "Rental days"])

        list_of_clients = self._rental_service.get_statistics_for_most_active_clients()
        self.setRowCount(len(list_of_clients))
        previous_position, previous_amount = None, None

        if len(list_of_clients) != 0:
            for index, client in enumerate(list_of_clients):
                client_id = client["ID"]
                _, client_data = self._client_service.find_client_by_client_id(client_id)
                client_name = client_data.name
                if index == 0:
                    self.setItem(index, 0, QtWidgets.QTableWidgetItem(str(index + 1)))
                    previous_position = 1
                else:
                    if previous_amount == client['Rental days']:
                        self.setItem(index, 0, QtWidgets.QTableWidgetItem(str(previous_position)))
                    else:
                        self.setItem(index, 0, QtWidgets.QTableWidgetItem(str(index + 1)))
                        previous_position = index + 1
                self.setItem(index, 1, QtWidgets.QTableWidgetItem(str(client_id)))
                self.setItem(index, 2, QtWidgets.QTableWidgetItem(str(client_name)))
                self.setItem(index, 3, QtWidgets.QTableWidgetItem(str(client['Rental days'])))
                previous_amount = client['Rental days']
        else:
            QMessageBox.warning(self, "Most active clients", "No clients renting!")

    def get_most_rented_books(self):
        self.update_table()
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["Rank", "Title", "Author", "Rental amount"])

        list_of_books = self._rental_service.get_statistics_for_most_rented_books()
        self.setRowCount(len(list_of_books))
        previous_position, previous_amount = None, None

        if len(list_of_books) != 0:
            for index, book in enumerate(list_of_books):
                if index == 0:
                    self.setItem(index, 0, QtWidgets.QTableWidgetItem(str(index + 1)))
                    previous_position = 1
                else:
                    if previous_amount == book['Rental amount']:
                        self.setItem(index, 0, QtWidgets.QTableWidgetItem(str(previous_position)))
                    else:
                        self.setItem(index, 0, QtWidgets.QTableWidgetItem(str(index + 1)))
                        previous_position = index + 1
                self.setItem(index, 1, QtWidgets.QTableWidgetItem(book["Title"]))
                self.setItem(index, 2, QtWidgets.QTableWidgetItem(book["Author"]))
                self.setItem(index, 3, QtWidgets.QTableWidgetItem(str(book["Rental amount"])))
                previous_amount = book['Rental amount']
        else:
            QMessageBox.warning(self, "Most rented books", "Empty book repository!")

    def get_most_rented_author(self):
        self.update_table()
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["Title", "Author", "Rental amount"])

        author = self._rental_service.get_most_rented_author()
        books_list = self._rental_service.get_list_of_books_of_most_rented_author(author)
        self.setRowCount(len(books_list))
        if len(books_list) != 0:
            QMessageBox.information(self, "Most rented author", author["Name"] + "-" + str(author["Rental amount"]))
            for index, book in enumerate(books_list):
                self.setItem(index, 0, QtWidgets.QTableWidgetItem(book["Title"]))
                self.setItem(index, 1, QtWidgets.QTableWidgetItem(str(author["Name"])))
                self.setItem(index, 2, QtWidgets.QTableWidgetItem(str(book["Rental amount"])))
        else:
            QMessageBox.warning(self, "Most rented author", "No books rented!")
