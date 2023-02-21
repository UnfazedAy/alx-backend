#!/usr/bin/env python3
"""Task 0 module -> A basic dictionary"""

from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """
    Defines a class for caching information in key-value pairs
    Methods:
        put(key, item) - store a key-value pair
        get(key) - retrieve the value associated with a key
    """
    def __init__(self):
        """initializes the class methods"""
        super().__init__()

    def put(self, key, item):
        """ Stores a key value pair"""
        if key is None or item is None:
            pass
        else:
            self.cache_data[key] = item

    def get(self, key):
        "returns the value in self.cache_data linked to a key"
        if key is None and key not in self.cache_data:
            return None
        else:
            return self.cache_data.get(key)
