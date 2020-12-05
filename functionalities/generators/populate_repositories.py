import random


def populate_book_repository(book_service):
    """
    Populate the book repository with 10 procedurally generated books at startup.
    :param book_service: The service through which the 10 books will be added, that is already pointing towards
        a book repository.
    """
    authors_list = ["Lamont Fitting", "Dudley Labrie", "Fidel Nielson", "Perry Eppler", "Raymond Luechtefeld",
                    "Otha Clayborne", "Walton Kottke", "Ernesto Nettles", "Abe Kerber", "Curtis Connon",
                    "Cortez Tijerina", "Antione Brakebill", "Nicolas Grimshaw", "Quinn Remillard",
                    "Darrick Estrada",
                    "Damion Cassel", "Bradly Moser", "Lloyd Tschanz", "Lenard Rolon", "Isaias Hixson"]
    titles_list = ["Opponent Of Dawn", "Phantom Of The Day", "Wolves Of The End", "Pilots With Honor",
                   "Companions And Women", "Knights And Rebels", "Anger Of The Forsaken", "Carnage Of The Day",
                   "Begging In Eternity", "Escaping The World", "Companion Of Next Year", "Woman Without Faith",
                   "Girls With Silver", "Soldiers Without A Conscience", "Invaders And Doctors",
                   "Traitors And Criminals", "Choice Of Desire", "Spire Of The Curse", "Calling The Elements",
                   "Possessed By The Apocalypse", "Heir Without Shame", "Tree Of The Plague",
                   "Wives Of The Solstice", "Criminals Of Destruction", "Turtles And Pirates", "Bandits And Owls",
                   "Rise With A Goal", "Tree Of Eternity", "Healing The Moon", "Raised By The Shadows"]
    for index in range(0, 10):
        title = random.choice(titles_list)
        author = random.choice(authors_list)
        book_service.add_book(title, author)


def populate_client_repository(client_service):
    """
    Populate the client repository with 10 procedurally generated clients at startup.
    :param client_service: The service through which the 10 clients will be added, that is already pointing towards
        a client repository.
    """
    names_list = ["Telma Dildine", "Iola Buettner", "Giselle Midgette", "Oren Fava", "Jannet Newbold", "Ok Macdougall",
                  "Frances Cullum", "Domingo Huggard", "Jackelyn Plum", "Aleisha Yerian", "Tiara Zinn", "Tara Vila",
                  "Loura Marinaro", "Carlos Luttrell", "Shayna Symes", "Pamela Lovejoy", "Al Bridger", "Shawn Lett",
                  "Annamarie Tran", "Renay Tingler", "Lynsey Grahn", "Kayla Denton", "Many Heras", "Hedy Heckard",
                  "Harold Ortman", "Emily Bedsole", "Lore Chia", "Joellen Peete", "Margeret Seda", "Julissa Thornberry",
                  "Crista Meidinger", "Collin He", "Madelyn Drake", "Lolita Hintze", "Mirian Parks", "Tawnya Hintz",
                  "Joyce Moodie", "Kisha Eagle", "Jalisa Eisenmann", "Birdie Spain", "Juliann Taitt", "Lucinda Lunt",
                  "Leoma Bartel", "Coy Mannon", "Georgiann Pascual", "Tilda Causby", "Julietta Buchholtz",
                  "Gus Bartram", "Mammie Most", "Eveline Patridge"]
    for index in range(0, 10):
        name = random.choice(names_list)
        client_service.add_client(name)


def populate_rental_repository(rental_service):
    """
    Populate the rental repository with 10 procedurally generated rentals at startup.
    :param rental_service: The service through which the 10 rentals will be added, that is already pointing towards
        a rental repository.
    """
    unavailable_books = []
    index = 1
    while index <= random.randint(3, 7):
        book_id = random.randint(1, 10)
        if book_id not in unavailable_books:
            unavailable_books.append(book_id)
            client_id = random.randint(1, 10)
            rental_service.add_rental(book_id, client_id)
        else:
            index -= 1
        index += 1
