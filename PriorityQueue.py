

class PriorityQueue:
    def __init__(self, init_list=[], sort_fn=False):
        self.queue = init_list
        if sort_fn:
            self.queue.sort(key=sort_fn)
    
    def is_empty(self):
        return len(self.queue) == 0

    def pop(self):
        return self.queue.pop()
    
    def insert(self, element, priority=0):
        self.queue.insert(priority, element)