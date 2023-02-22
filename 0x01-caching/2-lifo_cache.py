#!/usr/bin/env python3
"""Task 2 module -> LIFO caching"""

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """class for lifo caching"""
    def __init__(self):
        super().__init__()
        # A list to store the keys so as to easily discard using LIFO
        self.keys = []

    def put(self, key, item):
        """Puts the infos in a fifo cache system and perform fifo algorith"""
        if key is None or item is None:
            pass
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # Gets the last item in the list to discard
                discard = self.keys[-1]
                del self.cache_data[discard]
                # deletes the last key also in the data
                self.keys.pop()
                print("DISCARD: {}".format(discard))
            self.cache_data[key] = item
            self.keys.append(key)

    def get(self, key):
        """Retrieves the value of a key"""
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data.get(key)
