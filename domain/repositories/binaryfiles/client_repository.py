import pickle

from domain.repositories.inmemory.client_repository import ClientRepository


class ClientBinaryRepository(ClientRepository):
    def __init__(self, filename):
        ClientRepository.__init__(self)
        self.__filename = filename
        self.set_next_client_id()

    def __read_all_from_file(self):
        self._clients = []
        with open(self.__filename, "rb") as file:
            while True:
                try:
                    client = pickle.load(file)
                except EOFError:
                    client = None
                if client is not None:
                    self._clients.append(client)
                else:
                    break

    def __write_all_to_file(self):
        with open(self.__filename, "wb") as file:
            for client in self._clients:
                pickle.dump(client, file)

    def add_client(self, client):
        self.__read_all_from_file()
        ClientRepository.add_client(self, client)
        self.__write_all_to_file()

    def remove_client_by_index(self, index):
        self.__read_all_from_file()
        ClientRepository.remove_client_by_index(self, index)
        self.__write_all_to_file()

    def update_client(self, index, new_client):
        self.__read_all_from_file()
        ClientRepository.update_client(self, index, new_client)
        self.__write_all_to_file()

    def get_all_clients(self):
        self.__read_all_from_file()
        return ClientRepository.get_all_clients(self)

    def set_next_client_id(self):
        maximum_id = 0
        for client in self.get_all_clients():
            maximum_id = max(maximum_id, client.id)
        self._last_client_id = maximum_id
