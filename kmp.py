from collections import deque


def parent_dist(s, debug=False):  # O(n)
    # we assume s starts from index 1. we ignore the first character
    if debug:
      print('****parent_dist****')
    stack = deque()
    pd = [None for _ in s]  # index starts from 1
    for i, v in enumerate(s):
        if i == 0:
            continue  # ignore first character
        while len(stack) > 0:
            value, index = stack[-1]
            if value <= v:
                break
            stack.pop()

        if len(stack) == 0:
            pd[i] = 0
        else:
            pd[i] = i - index
        stack.append((v, i))

        if debug:
          print('stack: {}, parent_dist: {}'.format(stack, [x for x in pd if x is not None]))
          input()

    return pd


def sub_parent_dist(pd, left, right, k):  # O(1)
    if pd[left + k - 1] >= k:
        return 0
    return pd[left + k - 1]


def failure_func(pattern, debug=False):  # O(n)
    # we assume pattern starts from index 1. we ignore the first character
    if debug:
      print('****failure_func****')
    pd = parent_dist(pattern)
    length = 0
    fail = [None for _ in pattern]
    fail[1] = 0
    for i in range(2, len(pattern)):
        while length != 0:
            if sub_parent_dist(pd, i-length, i, length+1) == sub_parent_dist(pd, 1, length+1, length+1):
                break
            else:
                length = fail[length]

        length += 1
        fail[i] = length
        if debug:
          print('fail:', [x for x in fail if x is not None])
          input()
    return fail


def kmp_match(text, pattern):
    # we assume text and pattern begins from index 1. we ignore the first character
    debug=True
    n = len(text) - 1
    m = len(pattern) - 1

    pd = parent_dist(pattern, debug=debug)  # O(m)
    fail = failure_func(pattern, debug=debug)  # O(m)
    if debug:
      print('****kmp_match****')
    length = 0
    dq = deque()
    for i in range(1, n+1):  # O(n)
        # pop (value, index) from dq such that value > T[i]
        while len(dq) > 0 and dq[-1][0] > text[i]:
            dq.pop()

        while length != 0:
            sub_T = 0 if len(dq) == 0 else i - dq[-1][1]
            if sub_T == pd[length+1]:
                break
            else:
                length = fail[length]
                # pop (value, index) from dq (front) such that index < i - len
                while len(dq) > 0 and dq[0][1] < i - length:
                    dq.popleft()

        length += 1
        dq.append((text[i], i))
        if length == m:
            #print('Match at {}'.format(i - len(pattern) + 1))
            if debug:
              print('match at ', i - m + 1)
              input()
            yield i - m + 1
            length = fail[length]

            # pop (value, index) from dq (front) such that index <= i - len
            while len(dq) > 0 and dq[0][1] <= i - length:
                dq.popleft()

        if debug:
          print('dq:', dq)
          input()
