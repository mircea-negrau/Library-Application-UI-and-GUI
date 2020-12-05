from domain.entities.client_entity import Client
from functionalities.validation.exceptions import RepoError


class ClientService:
    def __init__(self, action_service, client_repository, client_validator):
        self._action_service = action_service
        self._client_repository = client_repository
        self._client_validator = client_validator

    def add_client(self, client_name_as_string):
        """
        Function to add a client to the client repository with the name given by the parameter. The function creates a
        new 'Client' entity which then passes through the 'ClientValidator'. In case any of the client's parameters are
        incorrect, the client is not added but an error is raised instead. Otherwise, the client is added to the
        client repository.
        :param client_name_as_string: string, holds the name for the client to be added; it should be
        between 1 and 25 characters.
        """
        client_id = self._client_repository.get_next_client_id()
        client = Client(client_id, client_name_as_string)
        self._client_validator.validate_client(client)
        self._client_repository.add_client(client)
        self._action_service.push_add_action_to_undo_list(client)

    def remove_client_by_client_id(self, client_id):
        """
        Function to remove the client from the client repository that has the ID given by the parameter. If no client
        is found identified by the given ID no clients are removed, but an error is raised instead. Otherwise, the
        client is removed from the client repository. Nothing is returned.
        :param client_id: integer, holds the value of the ID of the client to be removed. It should be a natural integer
        """
        client_index, client = self.find_client_by_client_id(client_id)
        if client_index is None:
            raise RepoError("Client ID not found. ")
        self._client_repository.remove_client_by_index(client_index)
        self._action_service.push_remove_action_to_undo_list(client)

    def update_client_by_client_id(self, client_id, new_name_as_string):
        """
        Function to update the details of a client entity found in the client repository with the values given by the
        function's parameters. If no client is found in the repository identified by the given client ID, an error is
        raised instead. Otherwise, the client name is replaced by the given value. If the given value does not
        properly create a client entity, an error is raised instead. Nothing is returned.
        :param client_id: integer, holds the value of the client that the function updates. Should be an natural integer
        :param new_name_as_string: string, holds the new name of the client. Should be between 1 and 25 characters
        """
        client_index, client = self.find_client_by_client_id(client_id)
        if client is None:
            raise RepoError("Client ID not found. ")
        new_client = Client(client_id, new_name_as_string)
        self._client_validator.validate_client(new_client)
        self._client_repository.update_client(client_index, new_client)
        self._action_service.push_update_action_to_undo_list(client, new_client)

    def update_client_by_name(self, old_name_as_string, new_name_as_string):
        """
        Function to update the details of an already existing client from the client repository. The function tries to
        find the client in the client repository. If no client is found, no client is updated but an error is raised
        instead. Otherwise, the client's new details are passed through a 'ClientValidator'. If the validation fails,
        no client is updated but an error is raised instead. Otherwise, the client is updated with the new details.
        :param old_name_as_string: string, holds the name of the client to be updated in the repository.
        :param new_name_as_string: string, holds the name the client will be updated with.
        """
        client_index, client = self.find_client_by_name(old_name_as_string)
        if client is None:
            raise RepoError("Name not found. ")
        client_id = client.id
        new_client = Client(client_id, new_name_as_string)
        self._client_validator.validate_client(new_client)
        self._client_repository.update_client(client_index, new_client)
        self._action_service.push_update_action_to_undo_list(client, new_client)

    def validate_client_with_parameters(self, client_id, client_name):
        """
        Function to validate that the parameters received by the function can correctly compose together a client entity
        :param client_id: integer, holds the value of the ID of the client to be validated. It should be a natural
        integer.
        :param client_name: string, holds the name of the client to be validated.
        """
        client_to_validate = Client(client_id, client_name)
        self._client_validator.validate_client(client_to_validate)
        del client_to_validate

    def find_client_by_client_id(self, client_id):
        """
        Function to return the index and client identified in the client repository by the parameter given ID. If no
        client is found or the 'client_id' is an invalid value, nothing is returned but an error is raised instead.
        Otherwise, the positional index and the client entity are returned.
        :param client_id: integer, holds the value of the ID of the client to be found. It should be a natural integer.
        :return: Index (integer) and book (entity) of the client that the function searched for. If no client is found,
        the values 'None' and 'None' are returned for the integer and client entity.
        """
        self.validate_client_with_parameters(client_id, "Best name")
        clients_list = self._client_repository.get_all_clients()
        for index, client in enumerate(clients_list):
            if client.id == client_id:
                return index, client
        return None, None

    def find_client_by_name(self, client_name_as_string):
        """
        Function to find a client in the client repository that has the name given by the parameter. The function tries
        to validate the client to be searched for. If the client fails the validation, no client is returned but an
        error is raised instead. Otherwise, the client is looked for in the client repository. If the client is found,
        the function returns the client's positional index and the 'client' object. Otherwise, the function returns
        None and None.
        :param client_name_as_string: string, holds the name of the client to be searched for.
        :return: If client is found, returns the positional index and the 'client' object from the client repository.
        Otherwise, the function returns None for both values.
        """
        self.validate_client_with_parameters(1, client_name_as_string)
        clients_list = self._client_repository.get_all_clients()
        for index, client in enumerate(clients_list):
            if client.name == client_name_as_string:
                return index, client
        return None, None

    def find_all_clients_sharing_id_value(self, client_id):
        """
        Function to find all the clients in the client repository for which the 'client_id' matches at least partially
        the value given by the parameter.
        :param client_id: integer, holds the value of the ID of clients to at least partially match.
        :return: list, containing all the client entities matching at least partially the given 'client_id' value
        """
        clients_list = self._client_repository.get_all_clients()
        list_of_matching_clients = []
        for client in clients_list:
            if str(client_id) in str(client.id):
                list_of_matching_clients.append(client)
        return list_of_matching_clients

    def find_all_clients_sharing_name_value(self, client_name_as_string):
        """
        Function to find all the clients in the client repository for which the 'name' matches at least partially
        the value given by the parameter.
        :param client_name_as_string: string, holds the string of the name of clients to at least partially match.
        :return: list, containing all the client entities matching at least partially the given 'name' string.
        """
        clients_list = self._client_repository.get_all_clients()
        list_of_matching_clients = []
        for client in clients_list:
            if client_name_as_string in client.name.lower():
                list_of_matching_clients.append(client)
        return list_of_matching_clients

    def get_all_clients(self):
        return self._client_repository.get_all_clients()