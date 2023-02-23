#!/usr/bin/env python3
"""Task 3 module -> LRU caching"""

from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """class for LRU caching"""
    def __init__(self):
        super().__init__()
        # A list to store the keys so as to easily track and discard using lRU
        self.lru_list = []

    def put(self, key, item):
        """Puts the infos in a fifo cache system and perform fifo algorith"""
        if key is None or item is None:
            return

        if key in self.lru_list:
            self.lru_list.remove(key)

        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            # Gets the least recently used item in the list to discard
            discard = self.lru_list[0]
            del self.cache_data[discard]
            # deletes the key also in the data
            self.lru_list.pop(0)
            print("DISCARD: {}".format(discard))

        self.cache_data[key] = item
        self.lru_list.append(key)

    def get(self, key):
        """Retrieves the value of a key"""
        if key is None or key not in self.cache_data:
            return None

        self.lru_list.remove(key)
        self.lru_list.append(key)
        return self.cache_data.get(key)
