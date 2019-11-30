from kmp import *

from tqdm import trange

import random
import time


def naive_match(text, pattern):
    n = len(text) - 1  # index starts from 1
    m = len(pattern) - 1  # index starts from 1
    pd_T = parent_dist(text)
    pd_P = parent_dist(pattern)
    for i in range(1, n - m + 2):
        match = True
        for j in range(1, m+1):
            if pd_P[j] != sub_parent_dist(pd_T, i, i+m-1, j):
                match = False
                break
        if match:
            yield i


def test_single_correctness(text, pattern):
    naive_matches = list(naive_match(text, pattern))
    kmp_matches = list(kmp_match(text, pattern))
    assert naive_matches == kmp_matches, '{} != {}'.format(naive_matches, kmp_matches)
    # print('{} in {} : {}'.format(pattern, text, naive_matches))


def test_correctness():
    n, m = 100, 10
    for _ in trange(100000):
        # index starts from 1
        text = [None] + [random.randint(1, 10) for _ in range(n)]
        pattern = [None] + [random.randint(1, 10) for _ in range(m)]
        test_single_correctness(text, pattern)


def test_single_time(n, m, repeat=10):
    total_time = 0
    for _ in range(repeat):
        text = [None] + [random.randint(1, 10) for _ in range(n)]
        pattern = [None] + [random.randint(1, 10) for _ in range(m)]
        start = time.time()
        matches = list(kmp_match(text, pattern))
        total_time += time.time() - start
    return total_time / repeat


def test_time():
    # ns = [10, 100, 1000, 10000, 100000, 1000000, 10000000]
    # ms = [10, 100, 1000, 10000]
    ns = [1000000 * (i+1) for i in range(5)]
    ms = [10000 * (i+1) for i in range(5)]

    for n in ns:
        for m in ms:
            print('{} {} {:.2f}secs'.format(n, m, test_single_time(n, m, 3)))

if __name__ == "__main__":
    # test_correctness()
    test_time()