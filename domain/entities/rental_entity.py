from datetime import date


class Rental:
    def __init__(self, rental_id, book_id, client_id, rented_date, returned_date):
        self.__rental_id = rental_id
        self.__book_id = book_id
        self.__client_id = client_id
        self.__rented_date = rented_date
        self.__returned_date = returned_date

    @property
    def id(self):
        """
        Function to return the id of the rental.
        :return: integer, ID of the rental.
        """
        return self.__rental_id

    @id.setter
    def id(self, rental_id):
        """
        Function to set the ID of the rental to the given parameter.
        :param rental_id: string, ID of the rental to be set as.
        """
        self.__rental_id = rental_id

    @property
    def book_id(self):
        """
        Function to return the ID of the book.
        :return: integer, ID of the book.
        """
        return self.__book_id

    @book_id.setter
    def book_id(self, book_id):
        """
        Function to set the ID of the client to the given parameter.
        :param book_id: integer, ID of the book to be set as.
        """
        self.__book_id = book_id

    @property
    def client_id(self):
        """
        Function to return the ID of the client.
        :return: integer, ID of the client.
        """
        return self.__client_id

    @client_id.setter
    def client_id(self, client_id):
        """
        Function to set the ID of the client to the given parameter.
        :param client_id: integer, ID of the client to be set as.
        """
        self.__client_id = client_id

    @property
    def rented_date(self):
        """
        Function to return the date of the rental.
        :return: date, date of the rental.
        """
        return self.__rented_date

    @rented_date.setter
    def rented_date(self, rented_date):
        """
        Function to set the date of the client to the given parameter.
        :param rented_date: date, date of the rental to be set as.
        """
        self.__rented_date = rented_date

    @property
    def returned_date(self):
        """
        Function to return the returned date of the rental.
        :return: date, returned date of the rental.
        """
        return self.__returned_date

    @returned_date.setter
    def returned_date(self, returned_date):
        """
        Function to set the returned date of the rental to the given parameter.
        :param returned_date: date, date of the rental's return to be set as.
        """
        self.__returned_date = returned_date

    @staticmethod
    def string_read_rental(line):
        parts = line.split(",")
        rental_id, book_id, client_id = int(parts[0]), int(parts[1]), int(parts[2])
        rented_date, returned_date = parts[3], parts[4]
        if rented_date != "None":
            rented_date_split = rented_date.split("-")
            year = int(rented_date_split[0])
            month = int(rented_date_split[1])
            day = int(rented_date_split[2])
            rented_date = date(year, month, day)
        else:
            rented_date = None
        if returned_date != "None":
            returned_date_split = returned_date.split("-")
            year = int(returned_date_split[0])
            month = int(returned_date_split[1])
            day = int(returned_date_split[2])
            returned_date = date(year, month, day)
        else:
            returned_date = None
        return Rental(rental_id, book_id, client_id, rented_date, returned_date)

    @staticmethod
    def json_read_rental(dictionary):
        if dictionary["rented_date"] != "None":
            dictionary["rented_date"] = dictionary["rented_date"].split("-")
            year = int(dictionary["rented_date"][0])
            month = int(dictionary["rented_date"][1])
            day = int(dictionary["rented_date"][2])
            dictionary["rented_date"] = date(year, month, day)
        else:
            dictionary["rented_date"] = None
        if dictionary["returned_date"] != "None":
            dictionary["returned_date"] = dictionary["returned_date"].split("-")
            year = int(dictionary["returned_date"][0])
            month = int(dictionary["returned_date"][1])
            day = int(dictionary["returned_date"][2])
            dictionary["returned_date"] = date(year, month, day)
        else:
            dictionary["returned_date"] = None
        return Rental(int(dictionary["id"]), dictionary["book_id"], dictionary["client_id"], dictionary["rented_date"],
                      dictionary["returned_date"])

    @staticmethod
    def string_write_rental(rental):
        return str(rental.id) + "," + str(rental.book_id) + "," + str(
            rental.client_id) + "," + str(rental.rented_date) + "," + str(rental.returned_date)

    @staticmethod
    def json_write_rental(rental):
        dictionary = {
            "id": rental.id,
            "book_id": rental.book_id,
            "client_id": rental.client_id,
            "rented_date": str(rental.rented_date),
            "returned_date": str(rental.returned_date)
        }
        return dictionary

    @staticmethod
    def read_rental_database(row):
        rental_id, book_id, client_id = int(row[0]), int(row[1]), int(row[2])
        rented_date, returned_date = row[3], row[4]
        if rented_date != "None":
            rented_date_split = rented_date.split("-")
            year = int(rented_date_split[0])
            month = int(rented_date_split[1])
            day = int(rented_date_split[2])
            rented_date = date(year, month, day)
        else:
            rented_date = None
        if returned_date != "None":
            returned_date_split = returned_date.split("-")
            year = int(returned_date_split[0])
            month = int(returned_date_split[1])
            day = int(returned_date_split[2])
            returned_date = date(year, month, day)
        else:
            returned_date = None
        return Rental(rental_id, book_id, client_id, rented_date, returned_date)

    @staticmethod
    def write_rental_database(rental):
        rental_tuple = (rental.book_id, rental.client_id, str(rental.rented_date), str(rental.returned_date), rental.id)
        return rental_tuple
