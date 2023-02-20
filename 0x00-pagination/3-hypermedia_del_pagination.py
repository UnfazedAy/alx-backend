#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """A function that ensures that the proper data are returned
        when queried even if some rows of the dataset are deleted.

        Args:
            index (int): _description_. Defaults to None and refers
                to a page of the dataset with page_size e.g. if index is 1
                and default page size is 10, then index should be 0 - 9
            page_size (int):  Defaults to 10.

        Returns:
            Dict: _description_
        """
        result = {}
        data = []
        indexed_data = self.indexed_dataset()
        assert index >= 0 and index <= max(indexed_data.keys())

        if index is not None:
            current_index = index
        else:
            current_index = 0

        track = 0
        while track < page_size and current_index <= max(indexed_data.keys()):
            if indexed_data.get(current_index):
                data.append(indexed_data.get(current_index))
            else:
                # If a data is not in the index,
                # we still have to maintain the return page_size
                page_size += 1
            current_index += 1
            track += 1

        result['index'] = index
        result['data'] = data
        result['page_size'] = len(data)
        result['next_index'] = current_index

        return result
