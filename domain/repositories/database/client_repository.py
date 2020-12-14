import sqlite3

from domain.repositories.inmemory.client_repository import ClientRepository


class ClientDatabaseRepository(ClientRepository):
    def __init__(self, read_client, read_book):
        self.connection = sqlite3.connect('library.db')
        self.__create_database()
        ClientRepository.__init__(self)
        self.__read_client = read_client
        self.__write_client = read_book
        self.set_next_client_id()

    def __create_database(self):
        cursor = self.connection.cursor()
        command = """CREATE TABLE IF NOT EXISTS clients(client_id INTEGER PRIMARY KEY, name TEXT)"""
        cursor.execute(command)

    def add_client(self, client):
        self.__read_all_from_database()
        ClientRepository.add_client(self, client)
        self.__add_to_database(client)

    def __add_to_database(self, client):
        string = "INSERT INTO clients(name, client_id) VALUES (?,?)"
        client_formatted = self.__write_client(client)
        cursor = self.connection.cursor()
        cursor.execute(string, client_formatted)
        self.connection.commit()

    def remove_client_by_index(self, index):
        self.__read_all_from_database()
        client = self.get_all_clients()[index]
        ClientRepository.remove_client_by_index(self, index)
        self.__remove_from_database(client.id)

    def __remove_from_database(self, client_id):
        string = """DELETE FROM clients WHERE client_id = ?"""
        cursor = self.connection.cursor()
        cursor.execute(string, str(client_id))
        self.connection.commit()

    def update_client(self, index, book):
        self.__read_all_from_database()
        ClientRepository.update_client(self, index, book)
        self.__update_to_database(index, book)

    def __update_to_database(self, index, client):
        string = """UPDATE clients SET name = ? WHERE client_id = ?"""
        client_formatted = self.__write_client(client)
        cursor = self.connection.cursor()
        cursor.execute(string, client_formatted)
        self.connection.commit()

    def get_all_clients(self):
        self.__read_all_from_database()
        return ClientRepository.get_all_clients(self)

    def set_next_client_id(self):
        maximum_id = 0
        for client in self.get_all_clients():
            maximum_id = max(maximum_id, client.id)
        self._last_client_id = maximum_id

    def __read_all_from_database(self):
        self._clients = []
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM clients")
        try:
            client_row = cursor.fetchone()
            while client_row is not None:
                client = self.__read_client(client_row)
                self._clients.append(client)
                client_row = cursor.fetchone()
        except Exception as exception:
            raise Exception(exception)
        finally:
            cursor.close()
