from PyQt5 import QtCore

from interface.gui.tables import *
from functionalities.validation.exceptions import RepoError


class WindowMainMenu(QtWidgets.QWidget):
    switch_to_manage_entities = QtCore.pyqtSignal()
    switch_to_manage_rentals = QtCore.pyqtSignal()
    switch_to_list_entities = QtCore.pyqtSignal()
    switch_to_search_entities = QtCore.pyqtSignal()
    switch_to_statistics = QtCore.pyqtSignal()

    def __init__(self, action_service):
        self._action_service = action_service
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Library - Main Menu')
        self.setFixedWidth(800)
        self.setFixedHeight(400)

        layout = QtWidgets.QGridLayout()

        self.setStyleSheet("""
                    QLineEdit{height: 40px; font-size: 30px}
                    QLabel{font-size: 30px}
                    QPushButton{font-size: 30px}
                """)

        self.buttonManageEntities = QtWidgets.QPushButton('Manage entities')
        self.buttonManageEntities.clicked.connect(self.switch_to_manage_entities.emit)
        layout.addWidget(self.buttonManageEntities)

        self.buttonManageRentals = QtWidgets.QPushButton('Manage rentals')
        self.buttonManageRentals.clicked.connect(self.switch_to_manage_rentals.emit)
        layout.addWidget(self.buttonManageRentals)

        self.buttonListEntities = QtWidgets.QPushButton('List entities')
        self.buttonListEntities.clicked.connect(self.switch_to_list_entities.emit)
        layout.addWidget(self.buttonListEntities)

        self.buttonSearchEntities = QtWidgets.QPushButton('Search entities')
        self.buttonSearchEntities.clicked.connect(self.switch_to_search_entities.emit)
        layout.addWidget(self.buttonSearchEntities)

        self.buttonStatistics = QtWidgets.QPushButton('Statistics')
        self.buttonStatistics.clicked.connect(self.switch_to_statistics.emit)
        layout.addWidget(self.buttonStatistics)

        self.buttonUndo = QtWidgets.QPushButton('Undo')
        self.buttonUndo.clicked.connect(self.undo)
        layout.addWidget(self.buttonUndo)

        self.buttonRedo = QtWidgets.QPushButton('Redo')
        self.buttonRedo.clicked.connect(self.redo)
        layout.addWidget(self.buttonRedo)

        self.buttonExit = QtWidgets.QPushButton('Exit')
        self.buttonExit.clicked.connect(self.exit_application)
        layout.addWidget(self.buttonExit)

        self.setLayout(layout)

    def undo(self):
        try:
            self._action_service.undo()
        except RepoError:
            QMessageBox.warning(self, "ERROR", "Nothing to undo!")

    def redo(self):
        try:
            self._action_service.redo()
        except RepoError:
            QMessageBox.warning(self, "ERROR", "Nothing to redo!")

    @staticmethod
    def exit_application():
        exit()


class WindowManageEntitiesChoice(QtWidgets.QWidget):
    switch_to_main_menu = QtCore.pyqtSignal(str)
    switch_to_manage_books = QtCore.pyqtSignal()
    switch_to_manage_clients = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Library - Manage Entities')
        self.setFixedWidth(800)
        self.setFixedHeight(350)

        layout = QtWidgets.QGridLayout()

        self.setStyleSheet("""
                            QLineEdit{height: 40px; font-size: 30px}
                            QLabel{font-size: 30px}
                            QPushButton{font-size: 30px}
                        """)

        self.buttonBooks = QtWidgets.QPushButton('Books')
        self.buttonBooks.clicked.connect(self.switch_to_manage_books.emit)

        self.buttonClients = QtWidgets.QPushButton('Clients')
        self.buttonClients.clicked.connect(self.switch_to_manage_clients.emit)

        self.buttonBack = QtWidgets.QPushButton('Back to main menu')
        self.buttonBack.clicked.connect(self.back_to_main_menu)

        layout.addWidget(self.buttonBooks)
        layout.addWidget(self.buttonClients)
        layout.addWidget(self.buttonBack)

        self.setLayout(layout)

    def back_to_main_menu(self):
        self.switch_to_main_menu.emit("self.window_manage_entities.close()")


class WindowManageBooks(QtWidgets.QWidget):
    switch_to_main_menu = QtCore.pyqtSignal(str)
    switch_to_add_books = QtCore.pyqtSignal()
    switch_to_update_books = QtCore.pyqtSignal()
    switch_to_remove_books = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Library - Manage Books')
        self.setFixedWidth(800)
        self.setFixedHeight(300)

        layout = QtWidgets.QGridLayout()

        self.setStyleSheet("""
                            QLineEdit{height: 40px; font-size: 30px}
                            QLabel{font-size: 30px}
                            QPushButton{font-size: 30px}
                        """)

        self.buttonAddBooks = QtWidgets.QPushButton('Add books')
        self.buttonAddBooks.clicked.connect(self.switch_to_add_books.emit)

        self.buttonUpdateBooks = QtWidgets.QPushButton('Update books')
        self.buttonUpdateBooks.clicked.connect(self.switch_to_update_books.emit)

        self.buttonRemoveBooks = QtWidgets.QPushButton('Remove books')
        self.buttonRemoveBooks.clicked.connect(self.switch_to_remove_books.emit)

        self.buttonBack = QtWidgets.QPushButton('Back to main menu')
        self.buttonBack.clicked.connect(self.back_to_main_menu)

        layout.addWidget(self.buttonAddBooks)
        layout.addWidget(self.buttonUpdateBooks)
        layout.addWidget(self.buttonRemoveBooks)
        layout.addWidget(self.buttonBack)

        self.setLayout(layout)

    def back_to_main_menu(self):
        self.switch_to_main_menu.emit("self.window_manage_books.close()")


class WindowAddBooks(QtWidgets.QWidget):
    switch_to_main_menu = QtCore.pyqtSignal(str)

    def __init__(self, book_service):
        self._book_service = book_service

        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Library - Add Books')
        self.setFixedWidth(800)
        self.setFixedHeight(300)

        layout = QtWidgets.QGridLayout()

        self.setStyleSheet("""
                            QLineEdit{height: 40px; font-size: 30px}
                            QLabel{font-size: 30px}
                            QPushButton{font-size: 30px}
                        """)

        self.lineEditTitle = QtWidgets.QLineEdit()
        self.lineEditTitle.setPlaceholderText("Title")
        self.lineEditAuthor = QtWidgets.QLineEdit()
        self.lineEditAuthor.setPlaceholderText('Author')
        self.buttonAdd = QtWidgets.QPushButton('Add book')
        self.buttonAdd.clicked.connect(self.check_if_valid)
        self.buttonBack = QtWidgets.QPushButton('Back to main menu')
        self.buttonBack.clicked.connect(self.back_to_main_menu)
        layout.addWidget(self.lineEditTitle)
        layout.addWidget(self.lineEditAuthor)
        layout.addWidget(self.buttonAdd)
        layout.addWidget(self.buttonBack)

        self.setLayout(layout)

    def check_if_valid(self):
        title = self.lineEditTitle.text()
        author = self.lineEditAuthor.text()
        valid_title = 0 < len(title) < 26
        valid_author = 0 < len(author) < 26
        valid_input = valid_title and valid_author
        if valid_input:
            self._book_service.add_book(title, author)
            self.back_to_main_menu()
        else:
            QMessageBox.warning(self, "ERROR", "Invalid values!")

    def back_to_main_menu(self):
        self.switch_to_main_menu.emit("self.window_add_books.close()")


class WindowUpdateBooks(QtWidgets.QWidget):
    switch_to_main_menu = QtCore.pyqtSignal(str)

    def __init__(self, book_service):
        self._book_service = book_service

        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Library - Update Book')
        self.setFixedWidth(800)
        self.setFixedHeight(300)

        layout = QtWidgets.QGridLayout()

        self.setStyleSheet("""
                            QLineEdit{height: 40px; font-size: 30px}
                            QLabel{font-size: 30px}
                            QPushButton{font-size: 30px}
                        """)

        self.lineID = QtWidgets.QLineEdit()
        self.lineID.setPlaceholderText('ID')
        self.lineEditTitle = QtWidgets.QLineEdit()
        self.lineEditTitle.setPlaceholderText('Title')
        self.lineEditAuthor = QtWidgets.QLineEdit()
        self.lineEditAuthor.setPlaceholderText('Author')
        self.buttonUpdate = QtWidgets.QPushButton('Update book')
        self.buttonUpdate.clicked.connect(self.check_if_valid)
        self.buttonBack = QtWidgets.QPushButton('Back to main menu')
        self.buttonBack.clicked.connect(self.back_to_main_menu)
        layout.addWidget(self.lineID)
        layout.addWidget(self.lineEditTitle)
        layout.addWidget(self.lineEditAuthor)
        layout.addWidget(self.buttonUpdate)
        layout.addWidget(self.buttonBack)

        self.setLayout(layout)

    def check_if_valid(self):
        try:
            book_id = int(self.lineID.text())
            new_title = self.lineEditTitle.text()
            new_author = self.lineEditAuthor.text()
            valid_title = 0 < len(new_title) < 26
            valid_author = 0 < len(new_author) < 26
            valid_input = valid_title and valid_author
            if valid_input:
                self._book_service.update_book_by_book_id(book_id, new_title, new_author)
                self.back_to_main_menu()
            else:
                QMessageBox.warning(self, "ERROR", "Invalid values!")
        except ValueError:
            QMessageBox.warning(self, "ERROR", "Invalid ID!")
        except RepoError:
            QMessageBox.warning(self, "ERROR", "Book not found!")


    def back_to_main_menu(self):
        self.switch_to_main_menu.emit("self.window_update_books.close()")


class WindowRemoveBooks(QtWidgets.QWidget):
    switch_to_main_menu = QtCore.pyqtSignal(str)

    def __init__(self, book_service, rental_service):
        self._book_service = book_service
        self._rental_service = rental_service

        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Library - Remove Book')
        self.setFixedWidth(800)
        self.setFixedHeight(300)

        layout = QtWidgets.QGridLayout()

        self.setStyleSheet("""
                            QLineEdit{height: 40px; font-size: 30px}
                            QLabel{font-size: 30px}
                            QPushButton{font-size: 30px}
                        """)

        self.lineID = QtWidgets.QLineEdit()
        self.lineID.setPlaceholderText('ID')
        self.buttonRemove = QtWidgets.QPushButton('Remove book')
        self.buttonRemove.clicked.connect(self.check_if_valid)
        self.buttonBack = QtWidgets.QPushButton('Back to main menu')
        self.buttonBack.clicked.connect(self.back_to_main_menu)
        layout.addWidget(self.lineID)
        layout.addWidget(self.buttonRemove)
        layout.addWidget(self.buttonBack)

        self.setLayout(layout)

    def check_if_valid(self):
        try:
            book_id = int(self.lineID.text())
            self._book_service.remove_book_by_book_id(book_id)
            self._rental_service.remove_rental_by_book_id(book_id)
            self.back_to_main_menu()
        except ValueError:
            QMessageBox.warning(self, "ERROR", "Invalid ID!")
        except RepoError as error:
            QMessageBox.warning(self, "ERROR", str(error))

    def back_to_main_menu(self):
        self.switch_to_main_menu.emit("self.window_remove_books.close()")


class WindowManageClients(QtWidgets.QWidget):
    switch_to_main_menu = QtCore.pyqtSignal(str)
    switch_to_add_clients = QtCore.pyqtSignal()
    switch_to_update_clients = QtCore.pyqtSignal()
    switch_to_remove_clients = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Library - Manage Clients')
        self.setFixedWidth(800)
        self.setFixedHeight(300)

        layout = QtWidgets.QGridLayout()

        self.setStyleSheet("""
                            QLineEdit{height: 40px; font-size: 30px}
                            QLabel{font-size: 30px}
                            QPushButton{font-size: 30px}
                        """)

        self.buttonAddClients = QtWidgets.QPushButton('Add clients')
        self.buttonAddClients.clicked.connect(self.switch_to_add_clients.emit)

        self.buttonUpdateClients = QtWidgets.QPushButton('Update clients')
        self.buttonUpdateClients.clicked.connect(self.switch_to_update_clients.emit)

        self.buttonRemoveClients = QtWidgets.QPushButton('Remove clients')
        self.buttonRemoveClients.clicked.connect(self.switch_to_remove_clients.emit)

        self.buttonBack = QtWidgets.QPushButton('Back to main menu')
        self.buttonBack.clicked.connect(self.back_to_main_menu)

        layout.addWidget(self.buttonAddClients)
        layout.addWidget(self.buttonUpdateClients)
        layout.addWidget(self.buttonRemoveClients)
        layout.addWidget(self.buttonBack)

        self.setLayout(layout)

    def back_to_main_menu(self):
        self.switch_to_main_menu.emit("self.window_manage_clients.close()")


class WindowAddClients(QtWidgets.QWidget):
    switch_to_main_menu = QtCore.pyqtSignal(str)

    def __init__(self, client_service):
        self._client_service = client_service

        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Library - Add Client')
        self.setFixedWidth(800)
        self.setFixedHeight(300)

        layout = QtWidgets.QGridLayout()

        self.setStyleSheet("""
                            QLineEdit{height: 40px; font-size: 30px}
                            QLabel{font-size: 30px}
                            QPushButton{font-size: 30px}
                        """)

        self.lineEditName = QtWidgets.QLineEdit()
        self.lineEditName.setPlaceholderText('Name')
        self.buttonAdd = QtWidgets.QPushButton('Add name')
        self.buttonAdd.clicked.connect(self.check_if_valid)
        self.buttonBack = QtWidgets.QPushButton('Back to main menu')
        self.buttonBack.clicked.connect(self.back_to_main_menu)
        layout.addWidget(self.lineEditName)
        layout.addWidget(self.buttonAdd)
        layout.addWidget(self.buttonBack)

        self.setLayout(layout)

    def check_if_valid(self):
        name = self.lineEditName.text()
        valid = 0 < len(name) < 26
        if valid:
            self._client_service.add_client(name)
            self.back_to_main_menu()
        else:
            QMessageBox.warning(self, "ERROR", "Invalid values!")

    def back_to_main_menu(self):
        self.switch_to_main_menu.emit("self.window_add_clients.close()")


class WindowUpdateClients(QtWidgets.QWidget):
    switch_to_main_menu = QtCore.pyqtSignal(str)

    def __init__(self, client_service):
        self._client_service = client_service

        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Library - Update Client')
        self.setFixedWidth(800)
        self.setFixedHeight(300)

        layout = QtWidgets.QGridLayout()

        self.setStyleSheet("""
                            QLineEdit{height: 40px; font-size: 30px}
                            QLabel{font-size: 30px}
                            QPushButton{font-size: 30px}
                        """)

        self.lineID = QtWidgets.QLineEdit()
        self.lineID.setPlaceholderText('ID')
        self.lineEditName = QtWidgets.QLineEdit()
        self.lineEditName.setPlaceholderText('Name')
        self.buttonUpdate = QtWidgets.QPushButton('Update client')
        self.buttonUpdate.clicked.connect(self.check_if_valid)
        self.buttonBack = QtWidgets.QPushButton('Back to main menu')
        self.buttonBack.clicked.connect(self.back_to_main_menu)
        layout.addWidget(self.lineID)
        layout.addWidget(self.lineEditName)
        layout.addWidget(self.buttonUpdate)
        layout.addWidget(self.buttonBack)

        self.setLayout(layout)

    def check_if_valid(self):
        try:
            client_id = int(self.lineID.text())
            new_name = self.lineEditName.text()
            valid = 0 < len(new_name) < 26
            if valid:
                self._client_service.update_client_by_client_id(client_id, new_name)
                self.back_to_main_menu()
            else:
                QMessageBox.warning(self, "ERROR", "Invalid values!")
        except RepoError as text:
            QMessageBox.warning(self, "ERROR", "Client not found!")
        except ValueError as text:
            QMessageBox.warning(self, "ERROR", "Invalid ID")

    def back_to_main_menu(self):
        self.switch_to_main_menu.emit("self.window_update_clients.close()")


class WindowRemoveClients(QtWidgets.QWidget):
    switch_to_main_menu = QtCore.pyqtSignal(str)

    def __init__(self, client_service, rental_service):
        self._client_service = client_service
        self._rental_service = rental_service

        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Library - Remove Client')
        self.setFixedWidth(800)
        self.setFixedHeight(300)

        layout = QtWidgets.QGridLayout()

        self.setStyleSheet("""
                            QLineEdit{height: 40px; font-size: 30px}
                            QLabel{font-size: 30px}
                            QPushButton{font-size: 30px}
                        """)

        self.lineID = QtWidgets.QLineEdit()
        self.lineID.setPlaceholderText('ID')
        self.buttonRemove = QtWidgets.QPushButton('Remove client')
        self.buttonRemove.clicked.connect(self.check_if_valid)
        self.buttonBack = QtWidgets.QPushButton('Back to main menu')
        self.buttonBack.clicked.connect(self.back_to_main_menu)
        layout.addWidget(self.lineID)
        layout.addWidget(self.buttonRemove)
        layout.addWidget(self.buttonBack)

        self.setLayout(layout)

    def check_if_valid(self):
        try:
            client_id = int(self.lineID.text())
            self._client_service.remove_client_by_client_id(client_id)
            self._rental_service.remove_rental_by_client_id(client_id)
            self.back_to_main_menu()
        except ValueError:
            QMessageBox.warning(self, "ERROR", "Invalid ID!")
        except RepoError as error:
            QMessageBox.warning(self, "ERROR", str(error))

    def back_to_main_menu(self):
        self.switch_to_main_menu.emit("self.window_remove_clients.close()")


class WindowManageRentals(QtWidgets.QWidget):
    switch_to_main_menu = QtCore.pyqtSignal(str)
    switch_to_rent = QtCore.pyqtSignal()
    switch_to_return = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Library - Manage Rentals')
        self.setFixedWidth(800)
        self.setFixedHeight(300)

        layout = QtWidgets.QGridLayout()

        self.setStyleSheet("""
                            QLineEdit{height: 40px; font-size: 30px}
                            QLabel{font-size: 30px}
                            QPushButton{font-size: 30px}
                        """)

        self.buttonRent = QtWidgets.QPushButton('Rent a book')
        self.buttonReturn = QtWidgets.QPushButton('Return a book')
        self.buttonBack = QtWidgets.QPushButton('Back to main menu')
        self.buttonRent.clicked.connect(self.switch_to_rent.emit)
        self.buttonReturn.clicked.connect(self.switch_to_return.emit)
        self.buttonBack.clicked.connect(self.back_to_main_menu)

        layout.addWidget(self.buttonRent)
        layout.addWidget(self.buttonReturn)
        layout.addWidget(self.buttonBack)

        self.setLayout(layout)

    def back_to_main_menu(self):
        self.switch_to_main_menu.emit("self.window_manage_rentals.close()")


class WindowRentBook(QtWidgets.QWidget):
    switch_to_main_menu = QtCore.pyqtSignal(str)

    def __init__(self, rental_service):
        QtWidgets.QWidget.__init__(self)
        self._rental_service = rental_service
        self.setWindowTitle('Library - Rent')
        self.setFixedWidth(800)
        self.setFixedHeight(300)

        layout = QtWidgets.QGridLayout()

        self.setStyleSheet("""
                            QLineEdit{height: 40px; font-size: 30px}
                            QLabel{font-size: 30px}
                            QPushButton{font-size: 30px}
                        """)

        self.lineEditBookID = QtWidgets.QLineEdit()
        self.lineEditBookID.setPlaceholderText('Book ID')
        self.lineEditClientID = QtWidgets.QLineEdit()
        self.lineEditClientID.setPlaceholderText('Client ID')
        self.buttonRent = QtWidgets.QPushButton('Rent book')
        self.buttonRent.clicked.connect(self.check_if_valid)
        self.buttonBack = QtWidgets.QPushButton('Back to main menu')
        self.buttonBack.clicked.connect(self.back_to_main_menu)
        layout.addWidget(self.lineEditBookID)
        layout.addWidget(self.lineEditClientID)
        layout.addWidget(self.buttonRent)
        layout.addWidget(self.buttonBack)

        self.setLayout(layout)

    def check_if_valid(self):
        try:
            book_id = int(self.lineEditBookID.text())
            client_id = int(self.lineEditClientID.text())
            self._rental_service.add_rental(book_id, client_id)
            self.back_to_main_menu()
        except ValueError:
            QMessageBox.warning(self, "ERROR", "Invalid ID!")
        except RepoError as error:
            QMessageBox.warning(self, "ERROR", str(error))

    def back_to_main_menu(self):
        self.switch_to_main_menu.emit("self.window_rent_book.close()")


class WindowReturnBook(QtWidgets.QWidget):
    switch_to_main_menu = QtCore.pyqtSignal(str)

    def __init__(self, rental_service):
        QtWidgets.QWidget.__init__(self)
        self._rental_service = rental_service
        self.setWindowTitle('Library - Return')
        self.setFixedWidth(800)
        self.setFixedHeight(300)

        layout = QtWidgets.QGridLayout()

        self.setStyleSheet("""
                            QLineEdit{height: 40px; font-size: 30px}
                            QLabel{font-size: 30px}
                            QPushButton{font-size: 30px}
                        """)

        self.lineEditID = QtWidgets.QLineEdit()
        self.lineEditID.setPlaceholderText('Book ID')
        self.buttonReturn = QtWidgets.QPushButton('Return book')
        self.buttonReturn.clicked.connect(self.check_if_valid)
        self.buttonBack = QtWidgets.QPushButton('Back to main menu')
        self.buttonBack.clicked.connect(self.back_to_main_menu)
        layout.addWidget(self.lineEditID)
        layout.addWidget(self.buttonReturn)
        layout.addWidget(self.buttonBack)

        self.setLayout(layout)

    def check_if_valid(self):
        try:
            book_id = int(self.lineEditID.text())
            self._rental_service.return_rental_by_book_id(book_id)
            self.back_to_main_menu()
        except ValueError:
            QMessageBox.warning(self, "ERROR", "Invalid ID!")
        except RepoError as error:
            QMessageBox.warning(self, "ERROR", str(error))

    def back_to_main_menu(self):
        self.switch_to_main_menu.emit("self.window_return_book.close()")


class WindowListEntities(QtWidgets.QWidget):
    switch_to_main_menu = QtCore.pyqtSignal(str)
    switch_to_list_books = QtCore.pyqtSignal()
    switch_to_list_clients = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Library - List Entities')
        self.setFixedWidth(800)
        self.setFixedHeight(300)

        layout = QtWidgets.QGridLayout()

        self.setStyleSheet("""
                            QLineEdit{height: 40px; font-size: 30px}
                            QLabel{font-size: 30px}
                            QPushButton{font-size: 30px}
                        """)

        self.buttonListBooks = QtWidgets.QPushButton('List books')
        self.buttonListBooks.clicked.connect(self.switch_to_list_books.emit)
        self.buttonListClients = QtWidgets.QPushButton('List clients')
        self.buttonListClients.clicked.connect(self.switch_to_list_clients.emit)

        self.buttonBack = QtWidgets.QPushButton('Back to main menu')
        self.buttonBack.clicked.connect(self.back_to_main_menu)

        layout.addWidget(self.buttonListBooks)
        layout.addWidget(self.buttonListClients)
        layout.addWidget(self.buttonBack)

        self.tableWidget = QtWidgets.QTableWidget()

        self.setLayout(layout)

    def back_to_main_menu(self):
        self.switch_to_main_menu.emit("self.window_list_entities.close()")


class WindowListBooks(QtWidgets.QWidget):
    switch_to_main_menu = QtCore.pyqtSignal(str)

    def __init__(self, book_service, rental_service):
        super().__init__()
        self._book_service = book_service
        self._rental_service = rental_service
        self.setWindowTitle('Library - List Books')
        self.setFixedWidth(800)
        self.setFixedHeight(300)

        self.layout = QtWidgets.QVBoxLayout()
        self.tableWidget = ListBooksTableWidget(book_service, rental_service)
        self.buttonBack = QtWidgets.QPushButton('Back to main menu')
        self.buttonBack.clicked.connect(self.back_to_main_menu)

        self.setStyleSheet("""
                            QLineEdit{height: 40px; font-size: 30px}
                            QLabel{font-size: 30px}
                            QPushButton{font-size: 30px}
                        """)

        self.layout.addWidget(self.tableWidget)
        self.layout.addWidget(self.buttonBack)

        self.setLayout(self.layout)

    def update_table(self):
        self.tableWidget.update_table()

    def back_to_main_menu(self):
        self.switch_to_main_menu.emit("self.window_list_books.close()")


class WindowListClients(QtWidgets.QWidget):
    switch_to_main_menu = QtCore.pyqtSignal(str)

    def __init__(self, client_service, rental_service):
        super().__init__()
        self._client_service = client_service
        self._rental_service = rental_service
        self.setWindowTitle('Library - List Clients')
        self.setFixedWidth(800)
        self.setFixedHeight(300)

        self.layout = QtWidgets.QVBoxLayout()
        self.tableWidget = ListClientsTableWidget(client_service, rental_service)
        self.buttonBack = QtWidgets.QPushButton('Back to main menu')
        self.buttonBack.clicked.connect(self.back_to_main_menu)

        self.setStyleSheet("""
                            QLineEdit{height: 40px; font-size: 30px}
                            QLabel{font-size: 30px}
                            QPushButton{font-size: 30px}
                        """)

        self.layout.addWidget(self.tableWidget)
        self.layout.addWidget(self.buttonBack)

        self.setLayout(self.layout)

    def update_table(self):
        self.tableWidget.update_table()

    def back_to_main_menu(self):
        self.switch_to_main_menu.emit("self.window_list_clients.close()")


class WindowSearchEntities(QtWidgets.QWidget):
    switch_to_main_menu = QtCore.pyqtSignal(str)
    switch_to_search_books = QtCore.pyqtSignal()
    switch_to_search_clients = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Library - Search Entities')
        self.setFixedWidth(800)
        self.setFixedHeight(300)

        layout = QtWidgets.QGridLayout()

        self.setStyleSheet("""
                            QLineEdit{height: 40px; font-size: 30px}
                            QLabel{font-size: 30px}
                            QPushButton{font-size: 30px}
                        """)

        self.buttonBooks = QtWidgets.QPushButton('Search Books')
        self.buttonClients = QtWidgets.QPushButton('Search Clients')
        self.buttonBooks.clicked.connect(self.switch_to_search_books.emit)
        self.buttonClients.clicked.connect(self.switch_to_search_clients.emit)

        self.buttonBack = QtWidgets.QPushButton('Back to main menu')
        self.buttonBack.clicked.connect(self.back_to_main_menu)

        layout.addWidget(self.buttonBooks)
        layout.addWidget(self.buttonClients)
        layout.addWidget(self.buttonBack)

        self.setLayout(layout)

    def back_to_main_menu(self):
        self.switch_to_main_menu.emit("self.window_search_entities.close()")


class WindowSearchBooks(QtWidgets.QWidget):
    switch_to_main_menu = QtCore.pyqtSignal(str)
    filter_by_id = QtCore.pyqtSignal(int)
    filter_by_title = QtCore.pyqtSignal(str)
    filter_by_author = QtCore.pyqtSignal(str)

    def __init__(self, book_service, rental_service):
        QtWidgets.QWidget.__init__(self)
        self._books_service = book_service
        self._rental_service = rental_service
        self.setWindowTitle('Library - Search Books')
        self.setFixedWidth(800)
        self.setFixedHeight(300)

        self.setStyleSheet("""
                            QLineEdit{height: 40px; font-size: 30px}
                            QLabel{font-size: 30px}
                            QPushButton{font-size: 30px}
                        """)

        mainLayout = QtWidgets.QHBoxLayout()
        table = SearchBooksTableWidget(self._books_service, self._rental_service)
        mainLayout.addWidget(table)
        buttonLayout = QtWidgets.QVBoxLayout()

        self.text_entry = QtWidgets.QLineEdit()
        self.text_entry.setPlaceholderText('Filter')
        buttonLayout.addWidget(self.text_entry)

        self.button_id = QtWidgets.QPushButton('ID')
        self.button_id.clicked.connect(self.search_by_id)
        buttonLayout.addWidget(self.button_id)

        self.button_title = QtWidgets.QPushButton('Title')
        self.button_title.clicked.connect(self.search_by_title)
        buttonLayout.addWidget(self.button_title)

        self.button_author = QtWidgets.QPushButton('Author')
        self.button_author.clicked.connect(self.search_by_author)
        buttonLayout.addWidget(self.button_author)

        self.buttonBack = QtWidgets.QPushButton('Back to main menu')
        self.buttonBack.clicked.connect(self.back_to_main_menu)
        buttonLayout.addWidget(self.buttonBack)

        self.filter_by_id.connect(table.filter_by_id)
        self.filter_by_title.connect(table.filter_by_title)
        self.filter_by_author.connect(table.filter_by_author)

        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)

    def search_by_id(self):
        try:
            self.filter_by_id.emit(int(self.text_entry.text()))
        except ValueError:
            QMessageBox.warning(self, "ERROR", "Invalid ID!")
        except RepoError as error:
            QMessageBox.warning(self, "ERROR", str(error))

    def search_by_title(self):
        try:
            self.filter_by_title.emit(self.text_entry.text())
        except ValueError:
            QMessageBox.warning(self, "ERROR", "Invalid ID!")
        except RepoError as error:
            QMessageBox.warning(self, "ERROR", str(error))

    def search_by_author(self):
        try:
            self.filter_by_author.emit(self.text_entry.text())
        except RepoError as error:
            QMessageBox.warning(self, "ERROR", str(error))

    def back_to_main_menu(self):
        self.switch_to_main_menu.emit("self.window_search_books.close()")


class WindowSearchClients(QtWidgets.QWidget):
    switch_to_main_menu = QtCore.pyqtSignal(str)
    filter_by_id = QtCore.pyqtSignal(int)
    filter_by_name = QtCore.pyqtSignal(str)

    def __init__(self, client_service, rental_service):
        QtWidgets.QWidget.__init__(self)
        self._client_service = client_service
        self._rental_service = rental_service
        self.setWindowTitle('Library - Search Clients')
        self.setFixedWidth(800)
        self.setFixedHeight(300)

        self.setStyleSheet("""
                            QLineEdit{height: 40px; font-size: 30px}
                            QLabel{font-size: 30px}
                            QPushButton{font-size: 30px}
                        """)

        mainLayout = QtWidgets.QHBoxLayout()
        table = SearchClientsTableWidget(self._client_service, self._rental_service)
        mainLayout.addWidget(table)
        buttonLayout = QtWidgets.QVBoxLayout()

        self.text_entry = QtWidgets.QLineEdit()
        self.text_entry.setPlaceholderText('Filter')
        buttonLayout.addWidget(self.text_entry)

        self.button_id = QtWidgets.QPushButton('ID')
        self.button_id.clicked.connect(self.search_by_id)
        buttonLayout.addWidget(self.button_id)

        self.button_name = QtWidgets.QPushButton('Name')
        self.button_name.clicked.connect(self.search_by_name)
        buttonLayout.addWidget(self.button_name)

        self.buttonBack = QtWidgets.QPushButton('Back to main menu')
        self.buttonBack.clicked.connect(self.back_to_main_menu)
        buttonLayout.addWidget(self.buttonBack)

        self.filter_by_id.connect(table.filter_by_id)
        self.filter_by_name.connect(table.filter_by_name)

        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)

    def search_by_id(self):
        try:
            self.filter_by_id.emit(int(self.text_entry.text()))
        except ValueError:
            QMessageBox.warning(self, "ERROR", "Invalid ID!")
        except RepoError as error:
            QMessageBox.warning(self, "ERROR", str(error))

    def search_by_name(self):
        try:
            self.filter_by_name.emit(self.text_entry.text())
        except RepoError as error:
            QMessageBox.warning(self, "ERROR", str(error))

    def back_to_main_menu(self):
        self.switch_to_main_menu.emit("self.window_search_clients.close()")


class WindowStatistics(QtWidgets.QWidget):
    switch_to_main_menu = QtCore.pyqtSignal(str)
    signal_get_most_rented_books = QtCore.pyqtSignal()
    signal_get_most_active_clients = QtCore.pyqtSignal()
    signal_get_most_rented_author = QtCore.pyqtSignal()

    def __init__(self, client_service, rental_service):
        QtWidgets.QWidget.__init__(self)
        self._client_service = client_service
        self._rental_service = rental_service
        self.setWindowTitle('Library - Statistics')
        self.setFixedWidth(800)
        self.setFixedHeight(300)

        self.setStyleSheet("""
                            QLineEdit{height: 40px; font-size: 30px}
                            QLabel{font-size: 30px}
                            QPushButton{font-size: 30px}
                        """)

        mainLayout = QtWidgets.QHBoxLayout()
        table = StatisticsTableWidget(self._client_service, self._rental_service)
        mainLayout.addWidget(table)
        buttonLayout = QtWidgets.QVBoxLayout()

        self.button_most_active_clients = QtWidgets.QPushButton('Most active clients')
        self.button_most_active_clients.clicked.connect(self.get_most_active_clients)
        buttonLayout.addWidget(self.button_most_active_clients)

        self.button_most_rented_books = QtWidgets.QPushButton('Most rented books')
        self.button_most_rented_books.clicked.connect(self.get_most_rented_books)
        buttonLayout.addWidget(self.button_most_rented_books)

        self.button_most_rented_author = QtWidgets.QPushButton('Most rented author')
        self.button_most_rented_author.clicked.connect(self.get_most_rented_author)
        buttonLayout.addWidget(self.button_most_rented_author)

        self.buttonBack = QtWidgets.QPushButton('Back to main menu')
        self.buttonBack.clicked.connect(self.back_to_main_menu)
        buttonLayout.addWidget(self.buttonBack)

        self.signal_get_most_active_clients.connect(table.get_most_active_clients)
        self.signal_get_most_rented_books.connect(table.get_most_rented_books)
        self.signal_get_most_rented_author.connect(table.get_most_rented_author)

        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)

    def get_most_active_clients(self):
        self.signal_get_most_active_clients.emit()

    def get_most_rented_books(self):
        self.signal_get_most_rented_books.emit()

    def get_most_rented_author(self):
        self.signal_get_most_rented_author.emit()

    def back_to_main_menu(self):
        self.switch_to_main_menu.emit("self.window_statistics.close()")
