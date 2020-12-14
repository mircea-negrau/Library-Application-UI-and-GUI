class Client:
    def __init__(self, client_id, name):
        self.__client_id = client_id
        self.__name = name

    @property
    def id(self):
        """
        Function to return the id of the client.
        :return: integer, ID of the client.
        """
        return self.__client_id

    @id.setter
    def id(self, client_id):
        """
        Function to set the id of the client to the given parameter.
        :param client_id: integer, ID of the client to be set as.
        """
        self.__client_id = client_id

    @property
    def name(self):
        """
        Function to return the name of the client.
        :return: string, name of the client.
        """
        return self.__name

    @name.setter
    def name(self, name):
        """
        Function to set the name of the client to the given parameter.
        :param name: string, name of the client to be set as.
        """
        self.__name = name

    @staticmethod
    def read_client(text_line):
        client_attributes = text_line.split(",")
        client_id, client_name = int(client_attributes[0]), client_attributes[1]
        return Client(client_id, client_name)

    @staticmethod
    def json_read_client(json_packed_client):
        return Client(int(json_packed_client["id"]), json_packed_client["name"])

    @staticmethod
    def write_client(client):
        return str(client.id) + "," + client.name

    @staticmethod
    def json_write_client(client):
        json_packed_client = {
            "id": client.id,
            "name": client.name
        }
        return json_packed_client

    @staticmethod
    def read_client_database(row):
        client_id, name = int(row[0]), row[1]
        return Client(client_id, name)

    @staticmethod
    def write_client_database(client):
        client_tuple = (client.name, client.id)
        return client_tuple