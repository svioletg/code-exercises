import random
import timeit

unsorted = [*range(100)]
random.shuffle(unsorted)

def simple_sort(to_sort: list) -> list:
    sorted: list = to_sort.copy()
    while True:
        swaps: int = 0
        for n, (a, b) in enumerate(zip(sorted, sorted[1:])):
            if b > a:
                sorted.insert(n+1, sorted.pop(n))
                swaps += 1
        if swaps == 0:
            break
    return sorted
