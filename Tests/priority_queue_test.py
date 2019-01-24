import unittest

from ..Utilities.priority_queue import PriorityQueue
from ..Utilities.constants import Priorities

class TestPriorityQueue(unittest.TestCase):
    def test_insertion(self):
        """Test that items are able to be inserted an removed."""
        queue = PriorityQueue()
        sample_item = 5
        queue.push(Priorities.MEDIUM, sample_item)
        returned_item = queue.pop()
        self.assertEqual(sample_item, returned_item, "Not inserting and \
        removing items correctly.")

    def test_proper_order(self):
        """Test that a mixed-bag of priorities comes out in the right order.""" 
        queue = PriorityQueue()
        items = [1, 2, 3]
        priorities = [Priorities.LOW, Priorities.MEDIUM, Priorities.HIGH]
        for x in range(0, 3):
            queue.push(priorities[x], items[x])

        items.reverse()
        for x in range(0, 3):
            self.assertEqual(items[x], queue.pop(), "Not returning items with \
            higher priority first.")

    def test_empty_queue(self):
        """Test that popping an empty queue does not throw error."""
        queue = PriorityQueue()
        item = queue.pop()

        self.assertEqual(item, None)

if __name__ == '__main__':
    unittest.main()
