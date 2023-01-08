from collections import deque

# Queue (FIFO)
class Queue:
    def __init__(self):
        self.elements = deque()

    def enqueue(self, element):
        self.elements.append(element)

    def dequeue(self):
        return self.elements.popleft()

    def re_enqueue(self, element):
        self.elements.appendleft(element)

# Stack (LIFO)
class Stack:
    def __init__(self):
        self.elements = deque()

    def enqueue(self, element):
        self.elements.append(element)

    def dequeue(self):
        return self.elements.pop()

    def re_enqueue(self, element):
        self.elements.append(element)