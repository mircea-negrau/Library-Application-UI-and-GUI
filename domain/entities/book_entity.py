class Book:
    def __init__(self, book_id, title, author):
        self.__book_id = book_id
        self.__title = title
        self.__author = author

    @property
    def id(self):
        """
        Function to return the id of the book.
        :return: integer, ID of the book.
        """
        return self.__book_id

    @id.setter
    def id(self, book_id):
        """
        Function to set the id of the book to the given parameter.
        :param book_id: integer, ID of the book to be set as.
        """
        self.__book_id = book_id

    @property
    def title(self):
        """
        Function to return the title of the book.
        :return: string, title of the book.
        """
        return self.__title

    @title.setter
    def title(self, title):
        """
        Function to set the title of the book to the given parameter.
        :param title: string, title of the book to be set as.
        """
        self.__title = title

    @property
    def author(self):
        """
        Function to return the author of the book.
        :return: string, author of the book.
        """
        return self.__author

    @author.setter
    def author(self, author):
        """
        Function to set the author of the book to the given parameter.
        :param author: string, author of the book to be set as.
        """
        self.__author = author

    @staticmethod
    def string_read_book(line):
        parts = line.split(",")
        return Book(int(parts[0]), parts[1], parts[2])

    @staticmethod
    def json_read_book(dictionary):
        return Book(int(dictionary["id"]), dictionary["title"], dictionary["author"])

    @staticmethod
    def string_write_book(book):
        return str(book.id) + "," + book.title + "," + book.author

    @staticmethod
    def json_write_book(book):
        dictionary = {
            "id": book.id,
            "title": book.title,
            "author": book.author
        }
        return dictionary
