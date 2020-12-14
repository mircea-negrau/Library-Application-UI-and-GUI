import sqlite3

from domain.repositories.inmemory.rental_repository import RentalRepository


class RentalDatabaseRepository(RentalRepository):
    def __init__(self, read_rental, write_rental):
        self.connection = sqlite3.connect('library.db')
        self.__create_database()
        RentalRepository.__init__(self)
        self.__read_rental = read_rental
        self.__write_rental = write_rental
        self.set_next_rental_id()

    def __create_database(self):
        cursor = self.connection.cursor()
        command = """CREATE TABLE IF NOT EXISTS rentals(rental_id INTEGER PRIMARY KEY, book_id INTEGER, client_id 
        INTEGER, rental_date DATE, returned_date DATE, FOREIGN KEY(book_id) REFERENCES books(book_id), FOREIGN KEY(
        client_id) REFERENCES clients(client_id)) """
        cursor.execute(command)

    def add_rental(self, rental):
        self.__read_all_from_database()
        RentalRepository.add_rental(self, rental)
        self.__add_to_database(rental)

    def __add_to_database(self, rental):
        string = "INSERT INTO rentals(book_id, client_id, rental_date, returned_date, rental_id) VALUES (?, ?, ?, " \
                 "?, ?) "
        rental_formatted = self.__write_rental(rental)
        cursor = self.connection.cursor()
        cursor.execute(string, rental_formatted)
        self.connection.commit()

    def remove_rental_by_index(self, index):
        self.__read_all_from_database()
        rental = self.get_all_rentals()[index]
        RentalRepository.remove_rental_by_index(self, index)
        self.__remove_from_database(rental.id)

    def __remove_from_database(self, rental_id):
        string = """DELETE FROM rentals WHERE rental_id = ?"""
        cursor = self.connection.cursor()
        cursor.execute(string, str(rental_id))
        self.connection.commit()

    def update_rental_return_by_index(self, index, new_date):
        self.__read_all_from_database()
        RentalRepository.update_rental_return_by_index(self, index, new_date)
        self.__update_to_database(index, new_date)

    def __update_to_database(self, index, rental):
        string = "UPDATE rentals SET book_id = ? AND client_id = ? AND rental_date = ? AND returned_date = ? WHERE rental_id = ?"
        rental_formatted = self.__write_rental(rental)
        cursor = self.connection.cursor()
        cursor.execute(string, rental_formatted)
        self.connection.commit()

    def get_all_rentals(self):
        self.__read_all_from_database()
        return RentalRepository.get_all_rentals(self)

    def set_next_rental_id(self):
        maximum_id = 0
        for rental in self.get_all_rentals():
            maximum_id = max(maximum_id, rental.id)
        self._last_rental_id = maximum_id

    def __read_all_from_database(self):
        self._rentals = []
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM rentals")
        try:
            rental_row = cursor.fetchone()
            while rental_row is not None:
                rental = self.__read_rental(rental_row)
                self._rentals.append(rental)
                rental_row = cursor.fetchone()
        except Exception as exception:
            raise Exception(exception)
        finally:
            cursor.close()
