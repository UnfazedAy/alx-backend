#!/usr/bin/env python3
"""Task 4 module -> MRU caching"""

from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """class for MRU caching"""
    def __init__(self):
        super().__init__()
        # A list to store the keys so as to easily track and discard using MRU
        self.mru_list = []

    def put(self, key, item):
        """Puts the infos in a fifo cache system and perform fifo algorith"""
        if key is None or item is None:
            return

        if key in self.mru_list:
            self.mru_list.remove(key)

        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            # Gets the most recently used item in the list to discard
            discard = self.mru_list[-1]
            del self.cache_data[discard]
            # deletes the key also in the data
            self.mru_list.pop()
            print("DISCARD: {}".format(discard))

        self.cache_data[key] = item
        self.mru_list.append(key)

    def get(self, key):
        """Retrieves the value of a key"""
        if key is None or key not in self.cache_data:
            return None

        self.mru_list.remove(key)
        self.mru_list.append(key)
        return self.cache_data.get(key)
