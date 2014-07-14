"""
Stack class
"""

class Stack:
    """
    A simple implementation of a FILO stack.
    """

    def __init__(self):
        """ 
        Initialize the stack.
        """
        self._items = []

    def __len__(self):
        """
        Return number of items in the stack.
        """
        return len(self._items)

    def __str__(self):
        """
        Returns a string representation of the stack.
        """
        return str(self._items)

    def push(self, item):
        """
        Push item onto the stack.
        """        
        self._items.append(item)

    def pop(self):
        """
        Pop an item off of the stack
        """
        return self._items.pop(-1)

    def clear(self):
        """
        Remove all items from the stack.
        """
        self._items = []
