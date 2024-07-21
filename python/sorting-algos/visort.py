"""Exercises on writing different sorting algorithms in Python.
For simplicity's sake, all sorting algorithms have the same goal of sorting a list from lowest to highest,
as determined by the outcome of calling `__gt__()` for the applicable items.

No third-party libraries may be used.
"""

import random
import time
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
def swap_sort(to_sort: list, swap_call: Callable = lambda l: None) -> list:
    """Iterate over a list in pairs of the current (A) and next (B) item.
    If A is evaluated as *greater than* B, swap their places in the list. Move to the next pair.

    If the entire list has been iterated over and no swaps were performed, sorting has completed.
    """
    sorted_list: list = to_sort.copy()
    passes: int = 0
    while True:
        passes += 1
        swaps: int = 0
        for n, (a, b) in enumerate(zip(sorted_list, sorted_list[1:])):
            if a > b:
                sorted_list.insert(n+1, sorted_list.pop(n))
                swaps += 1
                swap_call(sorted_list)
        if swaps == 0:
            break
    return sorted_list
#endregion SORTING

if __name__ == '__main__':
    unsorted: list[int] = [*range(1000)]
    random.shuffle(unsorted)

    threads: list[dict[Thread, list]] = [Thread(target=task, args=(i,)) for i in range(2)]
    unsorted_chunks = cutlist(len(threads))

    th_results: dict[int, list] = {}

    def task(n: int):
        

    for i in range(5):
        threads[i] = Thread(target=task, args=(i,))

    for n, t in threads.items():
        t.start()

    for n, t in threads.items():
        t.join()

    print(th_results)
    exit()
    ta = time.perf_counter()
    result = swap_sort(unsorted)
    tb = time.perf_counter()

    print(f'- Sorted {len(unsorted)} items in {tb - ta:.5f}s')
