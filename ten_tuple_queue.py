"""
A special queue that can only store 10 elements
Made so I can keep track of the last ten points and then
print them
"""

from collections import deque

class TenTuplesQueue:

    def __init__(self):
        self._q = deque()

    def add(self, tup):
        # while here just in case more than 10 elements got in somehow
        while len(self._q) >= 10:
            self._q.pop()
        self._q.appendleft(tup)

    def __str__(self):
        out = str(self._q)
        # do stuff, add extra vertical line space
        out = out[7:-2]
        out = out.replace("), ", ")\n")
        return out
