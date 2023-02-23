#!/usr/bin/env python3
"""Task 5 module -> LFU caching"""

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """class for lifo caching"""
    def __init__(self):
        super().__init__()
        # A dict to store and monitor the freq of the inputs
        self.lfu_dict = {}

    def put(self, key, item):
        """Puts the infos in a fifo cache system and perform fifo algorith"""
        if key is None or item is None:
            return
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # get the key with the minimal frequency
                min_key = min(self.lfu_dict, key=self.lfu_dict.get)
                discard = min_key
                del self.cache_data[discard]
                del self.lfu_dict[discard]
                print("DISCARD: {}".format(min_key))

            self.lfu_dict[key] = self.lfu_dict.get(key, 0) + 1
            self.cache_data[key] = item

    def get(self, key):
        """Retrieves the value of a key"""
        if key is None or key not in self.cache_data:
            return None

        self.lfu_dict[key] = self.lfu_dict.get(key, 0) + 1
        return self.cache_data.get(key)
