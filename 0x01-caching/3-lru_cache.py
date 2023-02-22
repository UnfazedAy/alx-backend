#!/usr/bin/env python3
"""Task 3 module -> LRU caching"""

from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """class for lifo caching"""
    def __init__(self):
        super().__init__()
        # A list to store the keys so as to easily discard using FIFO
        self.lifo_cache = []

    def put(self, key, item):
        """Puts the infos in a fifo cache system and perform fifo algorith"""
        if key is None or item is None:
            pass
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # Gets the least recently used item in the list to discard
                discard = self.lifo_cache[0]
                del self.cache_data[discard]
                # deletes the key also in the data
                self.lifo_cache.pop(0)
                print("DISCARD: {}".format(discard))

            if key in self.lifo_cache:
                del self.lifo_cache[self.lifo_cache.index(key)]

            self.cache_data[key] = item
            self.lifo_cache.append(key)
            print(self.lifo_cache)

    def get(self, key):
        """Retrieves the value of a key"""
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data.get(key)
