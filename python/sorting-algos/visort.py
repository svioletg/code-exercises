"""Exercises on writing different sorting algorithms in Python.
For simplicity's sake, all sorting algorithms have the same goal of sorting a list from lowest to highest,
as determined by the outcome of calling `__gt__()` for the applicable items.

No third-party libraries may be used.
"""

import random
import time
import sys
from copy import deepcopy
from threading import Thread
from typing import Callable


#region UTILITY FUNCTIONS
def cutlist(arr: list, parts: int) -> list[list]:
    """Divides a list into the number of parts given as similarly-sized as possible.

    Raises a `ValueError` if `parts` is greater than the length of `arr`.
    """
    if parts > len(arr):
        raise ValueError('Cannot separate list into more parts than it has items')

    chunk = len(arr) // parts
    start = 0
    stop = chunk
    cuts = []
    for p in range(1, parts+1):
        if (p == parts) and (len(arr) % p > 0):
            stop = len(arr)
        cuts.append(arr[start:stop])
        start += chunk
        stop += chunk
    return cuts
#endregion UTILITY FUNCTIONS

#region SORTING
def bubble(to_sort: list) -> list:
    """Iterate over a list in pairs of the current (A) and next (B) item.
    If A is evaluated as *greater than* B, swap their places in the list. Move to the next pair.

    If the entire list has been iterated over and no swaps were performed, sorting has completed.
    """
    sorted_list: list = to_sort.copy()
    passes: int = 0
    while True:
        passes += 1
        swaps: int = 0
        for n, i in enumerate(sorted_list): # pylint: disable=unused-variable
            if n + 1 == len(sorted_list):
                break
            if sorted_list[n] > sorted_list[n + 1]:
                sorted_list.insert(n + 1, sorted_list.pop(n))
                swaps += 1
        if swaps == 0:
            break
    return sorted_list
#endregion SORTING

def main(to_sort: list[int], sorter: Callable):
    print()
    print(sorter.__doc__.replace('    ', '  ') or sorter.__name__)
    ta = time.perf_counter()
    result = sorter(to_sort)
    tb = time.perf_counter()
    print(f'- Sorted {len(to_sort)} items in {tb - ta:.5f}s')
    print('- Comparing between the sorted list and the output of `sorted()`, '+
        f'they {"DO" if result == sorted(to_sort) else "DO NOT"} match.\n'
    )

if __name__ == '__main__':
    length: int = 50
    if len(sys.argv) > 1:
        length = int(sys.argv[1])
    unsorted: list[int] = [*range(length)]
    random.shuffle(unsorted)

    main(unsorted, bubble)
