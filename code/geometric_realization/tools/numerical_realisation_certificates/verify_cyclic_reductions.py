"""Exact finite checks for the cyclic reductions in Section 2.

Run with Python 3.10+ (standard library). Matrices have integer entries;
elimination is over Q. No result in a later section is used.
"""
from collections import Counter
from fractions import Fraction
from functools import lru_cache


@lru_cache(None)
def words(n):
    """Basis of the monomial quotient by xx and yyy in degree n."""
    if n == 0:
        return ('',)
    return tuple(w + a for w in words(n - 1) for a in 'xy'
                 if 'xx' not in w + a and 'yyy' not in w + a)


def necklace(word):
    if not word:
        return ''
    rotations = [word[i:] + word[:i] for i in range(len(word))]
    if any('xx' in w or 'yyy' in w for w in rotations):
        return None
    return min(rotations)


def matrix_row(terms, cyclic):
    coeff = Counter()
    for word, scalar in terms:
        if 'xx' in word or 'yyy' in word:
            continue
        column = necklace(word) if cyclic else word
        if column is not None:
            coeff[column] += scalar
    return coeff


def rank(rows):
    pivots = {}
    for row in rows:
        v = {w: Fraction(c) for w, c in row.items() if c}
        while v:
            lead = min(v)
            scale = v[lead]
            if lead not in pivots:
                pivots[lead] = {w: c / scale for w, c in v.items()}
                break
            for w, c in pivots[lead].items():
                value = v.get(w, 0) - scale * c
                if value:
                    v[w] = value
                else:
                    v.pop(w, None)
    return len(pivots)


def power(n):
    """Terms of (y-x)^n surviving the monomial relations."""
    return [(w, (-1) ** w.count('x')) for w in words(n)]


def relations(n, cyclic):
    if n < 5:
        return []
    # In the cocenter the left-hand multiplier can be rotated to the right.
    splits = (0,) if cyclic else range(n - 4)
    return [matrix_row(((u + w + v, c) for w, c in power(5)), cyclic)
            for i in splits for u in words(i) for v in words(n - 5 - i)]


def check_length_six():
    dims = []
    trace_dims = []
    for n in range(16):
        dims.append(len(words(n)) - rank(relations(n, False)))
        columns = {necklace(w) for w in words(n)} - {None}
        rows = relations(n, True)
        trace_dims.append(len(columns) - rank(rows))
        if n <= 4:
            rows.append(matrix_row(power(n), True))
        if n in (1, 2):
            rows.append(matrix_row([('y' * n, 1)], True))
        assert rank(rows) == len(columns), ('missing cyclic generator', n)
    assert dims == [1, 2, 3, 4, 5, 6, 6, 6, 6, 6, 5, 4, 3, 2, 1, 0]
    assert trace_dims == [1, 2, 2, 1, 1] + [0] * 11
    print('Length six: dim(B) =', sum(dims), 'and degree 15 is zero.')
    print('Cocenter dimensions by degree:', trace_dims)


# Rules over Z[T]; each term is (coefficient, power of T, word).
RULES = {
    'xx': [(1, 1, '')],
    'yyy': [(-3, 1, '')],
    'yyx': [(-1, 0, 'xyy'), (-1, 0, 'yxy')],
    'yxyx': [(1, 0, 'xyxy')],
}


def reduce_at(word, pos, lhs):
    out = Counter()
    for a, t, v in RULES[lhs]:
        for (j, w), c in normal(word[:pos] + v + word[pos + len(lhs):]).items():
            out[t + j, w] += a * c
    return {k: c for k, c in out.items() if c}


@lru_cache(None)
def normal(word):
    for lhs in RULES:
        pos = word.find(lhs)
        if pos != -1:
            return reduce_at(word, pos, lhs)
    return {(0, word): 1}


def check_e6():
    count = 0
    for u in RULES:
        for v in RULES:
            for j in range(1, min(len(u), len(v))):
                if u[-j:] == v[:j]:
                    w = u + v[j:]
                    assert reduce_at(w, 0, u) == reduce_at(w, len(u) - j, v), w
                    count += 1
            assert u == v or u not in v
    front = {''}
    basis = set()
    while front:
        basis.update(front)
        front = {u + a for u in front for a in 'xy'
                 if all(lhs not in u + a for lhs in RULES)}
    expected = {'', 'y', 'yy', 'x', 'xy', 'xyy', 'xyx', 'xyxy',
                'xyxyy', 'yx', 'yxy', 'yxyy'}
    assert count == 10 and basis == expected
    print('E6: all ten critical overlaps agree; twelve irreducible words.')


if __name__ == '__main__':
    check_e6()
    check_length_six()
