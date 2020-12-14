class ActionRepository:
    def __init__(self):
        self.__undo_list = []
        self.__redo_list = []
        self.__action_id = 0

    def push_undo(self, action):
        self.__undo_list.append(action)

    def pop_undo(self):
        self.__undo_list.pop()

    def push_redo(self, action):
        self.__redo_list.append(action)

    def pop_redo(self):
        self.__redo_list.pop()

    def get_undo(self):
        return self.__undo_list[-1]

    def get_redo(self):
        return self.__redo_list[-1]

    def get_all_actions(self):
        return self.__undo_list

    def get_all_actions_redo(self):
        return self.__redo_list

    def get_next_action_id(self):
        self.__action_id += 1
        return self.__action_id

    def get_last_action_id(self):
        return self.__action_id

    def clear_redo_list(self):
        self.__redo_list.clear()