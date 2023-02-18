#!/usr/bin/env python3
"""Task 0 module"""

from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Args:
        page: int,   page_size: int

    return
        A tuple containing a start index and end index corresponding
        to the range of indexes to return a list for those particular
        pagination parameter.
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return (start_index, end_index)
