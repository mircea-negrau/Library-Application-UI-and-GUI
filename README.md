# Assignment 06 - 08
## Requirements
- You will solve one of the problems below using simple feature-driven development
- Your program must provide a menu-driven console-based user interface. Implementation details are up to you
- Implementation must employ layered architecture and classes

### For week 8 (25% of grade)
- Implement features 1 and 2
- Have at least 10 procedurally generated items in your application at startup
- Provide specification and tests for all non-UI classes and methods for the first functionality
- Implement and use your own exception classes.

### For week 9 (25% of grade)
- Implement features 3 and 4
- Implement **PyUnit test cases**

### For week 10 (50% of grade)
- All features must be implemented

## For week 11
1. You must implement two additional repository sets: one using text files for storage, and one using binary files (e.g. using object serialization with [Pickle](https://docs.python.org/3.8/library/pickle.html)).
2. The program must work the same way using in-memory repositories, text-file repositories and binary file repositories.
3. The decision of which repositories are employed, as well as the location of the repository input files will be made in the program’s `settings.properties` file. An example is below:

    a. `settings.properties` for loading from memory (input files are not required):
    ```
    repository = inmemory
    cars = “”
    clients = “”
    rentals = “”
    ```
    b. `settings.properties` for loading from binary files, for someone who also created a GUI:
    ```
    repository = binaryfiles
    cars = “cars.pickle”
    clients = “clients.pickle”
    rentals = “rentals.pickle”
    ui = “GUI”
    ```

## Bonus possibility (0.1p, deadline week 10)
- 95% unit test code coverage for all modules except the UI 

## Bonus possibility (0.2p, deadline week 10)
- Implement a graphical user interface, in addition to the required menu-driven UI. Program can be started with either UI, without changes to source code.

## Bonus possibility (0.1p, deadline week 11)
- In addition to the file-based implementations above, implement the repository layer to use JSON or XML files for storage (at your choice).
- Create a `Settings` class into which you load the data from the `settings.properties` file. Then, the application start module decides which modules are started by examining the `settings` object. This further decouples the properties input file from the application.

## Bonus possibility (0.1p, deadline week 12)
- Implement a database-backed (SQL or NoSQL) repository. Use the database system’s update functionalities properly (don’t rewrite the entire database at each operation).

---
### Library
Write an application for a book library. The application will store:
- **Book**: `book_id`, `title`, `author`
- **Client**: `client_id`, `name`
- **Rental**: `rental_id`, `book_id`, `client_id`, `rented_date`, `returned_date`

Create an application to:
1. Manage clients and books. The user can add, remove, update, and list both clients and books.
2. Rent or return a book. A client can rent an available book. A client can return a rented book at any time. Only available books can be rented.
3. Search for clients or books using any one of their fields (e.g. books can be searched for using id, title or author). The search must work using case-insensitive, partial string matching, and must return all matching items.
4. Create statistics:
    - Most rented books. This will provide the list of books, sorted in descending order of the number of times they were rented.
    - Most active clients. This will provide the list of clients, sorted in descending order of the number of book rental days they have (e.g. having 2 rented books for 3 days each counts as 2 x 3 = 6 days).
    - Most rented author. This provides the list of books authored, sorted in descending order of the number of rentals their books have.
5. Unlimited undo/redo functionality. Each step will undo/redo the previous operation performed by the user. Undo/redo operations must cascade and have a memory-efficient implementation (no superfluous list copying).# Assignment 09
