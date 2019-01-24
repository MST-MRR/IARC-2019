import heapq

class PriorityQueue():
    """Custom priority queue implementation.

    This purpose of this class is to simplify the insertion and removal of
    items from the priority queue.

    Attributes
    ----------
    _queue: heapq
        The priority queue.
    """

    def __init__(self):
        self._queue = []

    def push(self, priority, item):
        """Insert an item onto the priority queue.

        Parameters
        ----------
        priority : Priority.{LOW, MEDIUM, HIGH}
            The priority of the task, with higher priority causes the item to
            "cut ahead" of items of lower priority.
        item : Any
            The data being inserted into the queue.

        """
        heapq.heappush(self._queue, (priority.value, item))

    def pop(self):
        """Remove the next item from the priortiy queue.

        Returns
        -------
        An item, or None if the priority queue is empty.
        """
        if (self.size > 0):
            # Index 0 is priority, index 1 is the item.
            return heapq.heappop(self._queue)[1]
        else:
            return None

    @property
    def size(self):
        """Get the size of the priority queue.
        """
        return len(self._queue)

    def clear(self):
        """Empty out the priority queue, deleting all the items.
        """
        self.queue = []
