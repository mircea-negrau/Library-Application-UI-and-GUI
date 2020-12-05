class RentalRepository(object):
    def __init__(self):
        self._rentals = []
        self._last_rental_id = 0

    def add_rental(self, rental):
        """
        Function to add a rental to the rental repository.
        :param rental: object, contains the rental object to be appended to the repository.
        """
        self._rentals.append(rental)

    def remove_rental_by_index(self, index):
        """
        Function to remove a rental from the rental repository.
        :param index: integer, integer, holds the value of the positional index of the rental to be removed
            from the repository.
        :return:
        """
        del self._rentals[index]
        return

    def update_rental_return_by_index(self, index, new_date):
        """
        Function to remove a rental from the rental repository.
        :param new_date: date, holds the date of return to be assigned to the rental
        :param index: integer, holds the value of the positional index of the rental to be set as returned from
            the repository.
        """
        self._rentals[index].returned_date = new_date

    def get_next_rental_id(self):
        """
        Function to return the next valid ID for a rental in the repository.
        :return: integer, next valid ID for a rental.
        """
        self.increment_last_rental_id()
        return self._last_rental_id

    def increment_last_rental_id(self):
        """
        Function to increment the last used rental ID in the repository.
        """
        self._last_rental_id += 1

    def get_all_rentals(self):
        """
        Function to return the full list of rental found in the repository.
        :return: list, containing the full list of rentals.
        """
        self._rentals = sorted(self._rentals, key=lambda rental: rental.id)
        return self._rentals