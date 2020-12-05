from domain.entities.rental_entity import Rental
from domain.entities.client_entity import Client
from domain.entities.book_entity import Book
from functionalities.validation.exceptions import RepoError


class ActionService:
    def __init__(self, action_repository, book_repository, client_repository, rental_repository):
        self.__action_repository = action_repository
        self.__undo = Undo(action_repository, book_repository, client_repository, rental_repository)
        self.__redo = Redo(action_repository, book_repository, client_repository, rental_repository)

    def undo(self):
        try:
            action = self.__action_repository.get_undo()
            action_id = action["id"]
        except IndexError:
            raise RepoError("Nothing to undo")
        while action["id"] == action_id:
            entity_type = action["entity_type"]
            if entity_type == "book":
                self.__undo.undo_book(action)
            elif entity_type == "client":
                self.__undo.undo_client(action)
            elif entity_type == "rental":
                self.__undo.undo_rental(action)
            self.__action_repository.push_redo(action)
            self.__action_repository.pop_undo()
            try:
                action = self.__action_repository.get_undo()
            except IndexError:
                break

    def redo(self):
        try:
            action = self.__action_repository.get_redo()
            action_id = action["id"]
        except IndexError:
            raise RepoError("Nothing to redo")
        while action["id"] == action_id:
            entity_type = action["entity_type"]
            if entity_type == "book":
                self.__redo.redo_book(action)
            elif entity_type == "client":
                self.__redo.redo_client(action)
            elif entity_type == "rental":
                self.__redo.redo_rental(action)
            self.__action_repository.push_undo(action)
            self.__action_repository.pop_redo()
            try:
                action = self.__action_repository.get_redo()
            except IndexError:
                break

    def push_add_action_to_undo_list(self, added_entity):
        action_id = self.__action_repository.get_next_action_id()
        entity_type = self.get_action_entity_type(added_entity)
        action = {
            "id": action_id,
            "action": "add",
            "entity_type": entity_type,
            "entity": added_entity
        }
        self.__action_repository.push_undo(action)
        self.__action_repository.clear_redo_list()

    def push_update_action_to_undo_list(self, old_entity, new_entity):
        action_id = self.__action_repository.get_next_action_id()
        entity_type = self.get_action_entity_type(old_entity)
        action = {
            "id": action_id,
            "action": "update",
            "entity_type": entity_type,
            "old_entity": old_entity,
            "new_entity": new_entity
        }
        self.__action_repository.push_undo(action)
        self.__action_repository.clear_redo_list()

    def push_remove_action_to_undo_list(self, removed_entity):
        action_id = self.__action_repository.get_next_action_id()
        entity_type = self.get_action_entity_type(removed_entity)
        action = {
            "id": action_id,
            "action": "remove",
            "entity_type": entity_type,
            "removed_entity": removed_entity
        }
        self.__action_repository.push_undo(action)
        self.__action_repository.clear_redo_list()

    def push_consecutive_indirect_remove_action_to_undo_list(self, entity):
        action_id = self.__action_repository.get_last_action_id()
        entity_type = self.get_action_entity_type(entity)
        action = {
            "id": action_id,
            "action": "remove",
            "entity_type": entity_type,
            "removed_entity": entity
        }
        self.__action_repository.push_undo(action)
        self.__action_repository.clear_redo_list()

    @staticmethod
    def get_action_entity_type(entity):
        if isinstance(entity, Book):
            return "book"
        if isinstance(entity, Client):
            return "client"
        if isinstance(entity, Rental):
            return "rental"


class Undo:
    def __init__(self, action_repository, book_repository, client_repository, rental_repository):
        self.__book_action = BookAction(action_repository, book_repository, client_repository, rental_repository)
        self.__client_action = ClientAction(action_repository, book_repository, client_repository, rental_repository)
        self.__rental_action = RentalAction(action_repository, book_repository, client_repository, rental_repository)

    def undo_book(self, action):
        action_type = action["action"]
        if action_type == "add":
            self.__book_action.undo_add_book(action)
        if action_type == "update":
            self.__book_action.undo_update_book(action)
        if action_type == "remove":
            self.__book_action.undo_remove_book(action)

    def undo_client(self, action):
        action_type = action["action"]
        if action_type == "add":
            self.__client_action.undo_add_client(action)
        if action_type == "update":
            self.__client_action.undo_update_client(action)
        if action_type == "remove":
            self.__client_action.undo_remove_client(action)

    def undo_rental(self, action):
        action_type = action["action"]
        if action_type == "add":
            self.__rental_action.undo_add_rental(action)
        if action_type == "update":
            self.__rental_action.undo_update_rental(action)
        if action_type == "remove":
            self.__rental_action.undo_remove_rental(action)


class Redo:
    def __init__(self, action_repository, book_repository, client_repository, rental_repository):
        self.__book_action = BookAction(action_repository, book_repository, client_repository, rental_repository)
        self.__client_action = ClientAction(action_repository, book_repository, client_repository, rental_repository)
        self.__rental_action = RentalAction(action_repository, book_repository, client_repository, rental_repository)

    def redo_book(self, action):
        action_type = action["action"]
        if action_type == "add":
            self.__book_action.redo_add_book(action)
        if action_type == "update":
            self.__book_action.redo_update_book(action)
        if action_type == "remove":
            self.__book_action.redo_remove_book(action)

    def redo_client(self, action):
        action_type = action["action"]
        if action_type == "add":
            self.__client_action.redo_add_client(action)
        if action_type == "update":
            self.__client_action.redo_update_client(action)
        if action_type == "remove":
            self.__client_action.redo_remove_client(action)

    def redo_rental(self, action):
        action_type = action["action"]
        if action_type == "add":
            self.__rental_action.redo_add_rental(action)
        if action_type == "update":
            self.__rental_action.redo_update_rental(action)
        if action_type == "remove":
            self.__rental_action.redo_remove_rental(action)


class BookAction:
    def __init__(self, action_repository, book_repository, client_repository, rental_repository):
        self._action_repository = action_repository
        self._book_repository = book_repository
        self._client_repository = client_repository
        self._rental_repository = rental_repository

    def undo_add_book(self, action):
        for index, book in enumerate(self._book_repository.get_all_books()):
            if book.id == action["entity"].id:
                self._book_repository.remove_book_by_index(index)
                break

    def undo_update_book(self, action):
        for index, book in enumerate(self._book_repository.get_all_books()):
            if book.id == action["old_entity"].id:
                self._book_repository.update_book(index, action["old_entity"])
                break

    def undo_remove_book(self, action):
        self._book_repository.add_book(action["removed_entity"])

    def redo_add_book(self, action):
        self._book_repository.add_book(action["entity"])

    def redo_update_book(self, action):
        for index, book in enumerate(self._book_repository.get_all_books()):
            if book.id == action["new_entity"].id:
                self._book_repository.update_book(index, action["new_entity"])
                break

    def redo_remove_book(self, action):
        for index, book in enumerate(self._book_repository.get_all_books()):
            if book.id == action["removed_entity"].id:
                self._book_repository.remove_book_by_index(index)
                break


class ClientAction:
    def __init__(self, action_repository, book_repository, client_repository, rental_repository):
        self._action_repository = action_repository
        self._book_repository = book_repository
        self._client_repository = client_repository
        self._rental_repository = rental_repository

    def undo_add_client(self, action):
        for index, client in enumerate(self._client_repository.get_all_clients()):
            if client.id == action["entity"].id:
                self._client_repository.remove_client_by_index(index)
                break

    def undo_update_client(self, action):
        for index, client in enumerate(self._client_repository.get_all_clients()):
            if client.id == action["old_entity"].id:
                self._client_repository.update_client(index, action["old_entity"])
                break

    def undo_remove_client(self, action):
        self._client_repository.add_client(action["removed_entity"])

    def redo_add_client(self, action):
        self._client_repository.add_client(action["entity"])

    def redo_update_client(self, action):
        for index, client in enumerate(self._client_repository.get_all_clients()):
            if client.id == action["new_entity"].id:
                self._client_repository.update_client(index, action["new_entity"])
                break

    def redo_remove_client(self, action):
        for index, client in enumerate(self._client_repository.get_all_clients()):
            if client.id == action["removed_entity"].id:
                self._client_repository.remove_client_by_index(index)
                break


class RentalAction:
    def __init__(self, action_repository, book_repository, client_repository, rental_repository):
        self._action_repository = action_repository
        self._book_repository = book_repository
        self._client_repository = client_repository
        self._rental_repository = rental_repository

    def undo_add_rental(self, action):
        for index, rental in enumerate(self._rental_repository.get_all_rentals()):
            if rental.id == action["entity"].id:
                self._rental_repository.remove_rental_by_index(index)
                break

    def undo_update_rental(self, action):
        for index, rental in enumerate(self._rental_repository.get_all_rentals()):
            if rental.id == action["old_entity"].id:
                self._rental_repository.update_rental_return_by_index(index, None)
                auxiliary = action["new_entity"]
                action["new_entity"] = action["old_entity"]
                action["old_entity"] = auxiliary
                break

    def undo_remove_rental(self, action):
        self._rental_repository.add_rental(action["removed_entity"])

    def redo_add_rental(self, action):
        self._rental_repository.add_rental(action["entity"])

    def redo_update_rental(self, action):
        for index, rental in enumerate(self._rental_repository.get_all_rentals()):
            if rental.id == action["old_entity"].id:
                self._rental_repository.update_rental_return_by_index(index, action["old_entity"].returned_date)
                auxiliary = action["new_entity"]
                action["new_entity"] = action["old_entity"]
                action["old_entity"] = auxiliary
                break

    def redo_remove_rental(self, action):
        for index, rental in enumerate(self._rental_repository.get_all_rentals()):
            if rental.id == action["removed_entity"].id:
                self._rental_repository.remove_rental_by_index(index)
                break