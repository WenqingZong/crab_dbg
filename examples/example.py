from sys import stderr

from crab_dbg import dbg


class Node:
    def __init__(self, val=0, next_=None):
        self.val = val
        self.next = next_


class LinkedList:
    def __init__(self, start=None):
        self.start = start

    @staticmethod
    def create(n: int) -> "LinkedList":
        """
        Create a LinkedList of n elements, value ranges from 0 to n - 1.
        """
        if n <= 0:
            raise ValueError("A linked list with %d element is meaningless", n)

        start = Node(0)
        linked_list = LinkedList(start)

        cur = start
        for i in range(1, n):
            new_node = Node(i)
            cur.next = new_node
            cur = cur.next

        return linked_list


class Phone:
    def __init__(self, brand, color, price):
        self.brand = brand
        self.color = color
        self.price = price

    def __repr__(self):
        return "A %s phone made by %s, official price: %s." % (
            self.color,
            self.brand,
            self.price,
        )


class Stack:
    def __init__(self):
        self.data = []

    def push(self, item):
        self.data.append(item)

    def pop(self):
        return self.data.pop()


if __name__ == "__main__":
    pi = 3.14
    ultimate_answer = 42
    flag = True
    stock_price = [100, 99, 101, 1]
    fruits = {"apple", "peach", "watermelon"}
    country_to_capital_cities = {
        "China": "Beijing",
        "United Kingdom": "London",
        "Liyue": "Liyue Harbor",
    }

    # You can use dbg to inspect a lot of variables.
    dbg(
        pi,
        1 + 1,
        sorted(stock_price),
        "This string contains (, ' and ,",
        ultimate_answer,
        flag,  # You can leave a comment here as well, dbg() won't show this comment.
        stock_price,
        fruits,
        country_to_capital_cities,
    )

    # Or, you can use dbg to inspect one. Note that you can pass any keyword arguments originally supported by print()
    dbg(country_to_capital_cities, file=stderr)

    # You can also use dbg to inspect expressions.
    dbg(1 + 1)

    # When used with objects, it will show all fields contained by that object.
    linked_list = LinkedList.create(2)
    dbg(linked_list)

    # dbg() works with lists, tuples, and dictionaries.
    dbg(
        [linked_list, linked_list],
        (linked_list, linked_list),
        {"a": 1, "b": linked_list},
        [
            1,
            2,
            3,
            4,
        ],
    )

    # For even more complex structures, it works as well.
    stack = Stack()
    stack.push(linked_list)
    stack.push(linked_list)
    dbg(stack)

    dbg("What if my input is a string?")

    # If your type has its own __repr__ or __str__ implementation, no worries, crab_dbg will jut use it.
    phone = Phone("Apple", "white", 1099)
    dbg(phone)

    # If invoked without arguments, then it will just print the filename and line number.
    dbg()

    # import numpy as np
    # import torch
    # # This library can also be used with your favorite data science libraries if you enabled our optional features.
    # numpy_array = np.zeros(shape=(2, 3))
    # dbg(numpy_array)
    #
    # torch_tensor = torch.from_numpy(numpy_array)
    # dbg(torch_tensor)
