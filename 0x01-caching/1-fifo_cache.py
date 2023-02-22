#!/usr/bin/env python3
"""Task 1 module -> FIFO caching"""

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """class for fifo caching"""
    def __init__(self):
        super().__init__()
        # A list to store the keys so as to easily discard using FIFO
        self.keys = []

    def put(self, key, item):
        """Puts the infos in a fifo cache system and perform fifo algorith"""
        if key is None or item is None:
            pass
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # Gets the first item in the list to discard
                discard = self.keys[0]
                del self.cache_data[discard]
                # deletes the first key also in the data
                self.keys.pop(0)
                print("DISCARD: {}".format(discard))
            self.cache_data[key] = item
            self.keys.append(key)

    def get(self, key):
        """Retrieves the value of a key"""
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data.get(key)
