from crab_dbg import dbg

class Node:
    def __init__(self, val=0, next_=None):
        self._val = 0
        self._next = next_

class LinkedList:
    def __init__(self, start=None):
        self.start = start
    
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
            cur.next_ = new_node
            cur = cur.next_

        return linked_list


if __name__ == '__main__':
    pai = 3.14
    ultimate_answer = 42
    flag = True
    fruits = ['apple', 'peach', 'watermelon']
    country_to_capital_cities = {
        'China': "Beijing",
        'United Kindom': 'London',
        'Liyue': 'Liyue Habour',
    }

    # You can use dbg to inspect a lot of variables.
    dbg(
        pai, ultimate_answer,
        flag,
        fruits,
        country_to_capital_cities,
    )

    # Or, you can ust dbg to inspect one.
    dbg(country_to_capital_cities)

    # You can also use dbg to inspect expressions.
    dbg(1 + 1)

    # When used with objects, it will show all fields contained by that object.
    linked_list = LinkedList.create(3)
    dbg(linked_list)