class ClientRepository(object):
    def __init__(self):
        self._clients = []
        self._last_client_id = 0

    def add_client(self, client):
        """
        Function to add a client to the client repository.
        :param client: object, contains the client object to be appended to the repository.
        """
        self._clients.append(client)

    def remove_client_by_index(self, index):
        """
        Function to remove a client from the client repository.
        :param index: integer, holds the value of the positional index of the client to be removed from the repository.
        """
        del self._clients[index]
        return

    def update_client(self, index, new_client):
        """
        Function to update the details of a client found in the client repository.
        :param index: integer, holds the value of the positional index of the client to be updated from the repository.
        :param new_client: object, contains the updated client object to replace the one found at index in the
        repository.
        """
        self._clients[index] = new_client

    def get_next_client_id(self):
        """
        Function to return the next valid ID for a client in the repository.
        :return: integer, next valid ID for a client.
        """
        self.increment_last_client_id()
        return self._last_client_id

    def increment_last_client_id(self):
        """
        Function to increment the last used client ID in the repository.
        """
        self._last_client_id += 1

    def get_all_clients(self):
        """
        Function to return the full list of client found in the repository.
        :return: list, containing the full list of clients.
        """
        return self._clients