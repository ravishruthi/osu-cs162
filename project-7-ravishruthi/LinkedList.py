# Author: Shruthi Ravi
# Date: 02/16/2021
# Description: A linked list implementation with methods that use recursion.
#


class Node:
    def __init__(self, data):
        self._data = data
        self._next = None

    def get_data(self):
        """returns the data."""
        return self._data

    def set_data(self, val):
        """sets the data to the value passed in."""
        self._data = val

    def get_next(self):
        """returns the next node."""
        return self._next

    def set_next(self, a_node):
        """sets next to the node passed in."""
        self._next = a_node


class LinkedList:
    def __init__(self):
        self._head = None

    def get_head(self):
        """returns node object at head of linked list"""
        return self._head

    def rec_add(self, val, a_node):
        """
            recursive add method
            adds a new node with val passed in at the end of the linked list
        """
        if self._head is None:  # if list is empty, create head node
            self._head = Node(val)
        elif a_node.get_next() is not None:  # recurse till last node in list
            self.rec_add(val, a_node.get_next())
        else:
            a_node.set_next(Node(val))

    def add(self, val):
        """recursive add helper method"""
        self.rec_add(val, self._head)

    def rec_remove(self, val, previous, current):
        """
            recursive remove method
            removes node with specified val, if found
        """
        if self._head is None:  # if list is empty, return
            return
        if self._head.get_data() == val:  # if val is at head, set next node to head
            self._head = self._head.get_next()
        else:
            if current is not None and current.get_data() != val:  # recurse till found
                self.rec_remove(val, current, current.get_next())
            elif current is not None:  # if found, set the next of previous node to the node after current node
                previous.set_next(current.get_next())

    def remove(self, val):
        """recursive remove helper method"""
        self.rec_remove(val, None, self._head)

    def rec_contains(self, val, a_node):
        """
            recursive contains method
            returns True if val passed in is in linked list, False otherwise
        """
        if a_node is None:
            return False
        if a_node.get_data() == val:
            return True
        return self.rec_contains(val, a_node.get_next())

    def contains(self, val):
        """recursive contains helper method"""
        return self.rec_contains(val, self._head)

    def rec_insert(self, val, pos, index, current):
        """
            recursive insert helper method
            inserts node with val passed in, at position passed in
        """
        if self._head is None:  # if list is empty, insert node at head
            self._head = Node(val)
        elif pos == 0:  # assign head to new node and set next to initial head node
            self._head = Node(val)
            self._head.set_next(current)
        elif index+1 == pos:  # if pos found, place new node in between current node and current's next node
            new_node = Node(val)
            next_node = current.get_next()  # store current node's 'next' node
            current.set_next(new_node)  # set current node's 'next' member to new node
            new_node.set_next(next_node)  # set new node's 'next' member to current node's initial 'next' node
        elif current.get_next() is None:  # if pos >= list length, place new node at end
            current.set_next(Node(val))
        else:
            self.rec_insert(val, pos, index+1, current.get_next())

    def insert(self, val, pos):
        """recursive insert method"""
        self.rec_insert(val, pos, 0, self._head)

    def rec_reverse(self, previous, current):
        """
            recursive reverse helper method
            reverse the order of nodes in linked list
        """
        if self._head is None:  # if list is empty, return
            return
        elif current.get_next() is None:  # if on last node in list
            self._head = current  # make this the head node
            current.set_next(previous)  # set 'next' member to the node before it
        else:
            next_node = current.get_next()  # store current node's 'next' node
            current.set_next(previous)  # set current node's 'next' member to previous node
            self.rec_reverse(current, next_node)  # recurse, go to next node in list

    def reverse(self):
        """recursive reverse method"""
        self.rec_reverse(None, self._head)

    def rec_to_plain_list(self, current, result_list):
        """
            recursive to_plain_list helper method
            returns regular list that has same values, in same order has the
            Nodes in the linked list
        """
        if current is not None:
            result_list.append(current.get_data())
            self.rec_to_plain_list(current.get_next(), result_list)
        return result_list

    def to_plain_list(self):
        """recursive to_plain_list method"""
        return self.rec_to_plain_list(self._head, [])

    # rec_display taken directly from README
    def rec_display(self, a_node):
        """recursive display method"""
        if a_node is None:
            print("\n")  # added for new line
            return
        print(a_node.get_data(), end=" ")
        self.rec_display(a_node.get_next())

    # display taken directly from README
    def display(self):
        """recursive display helper method"""
        self.rec_display(self.get_head())

    # is_empty taken directly from module
    def is_empty(self):
        """
        Returns True if the linked list is empty, False otherwise
        """
        return self._head is None
