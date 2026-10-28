#!/usr/bin/env python3
"""Verify the finite rational certificate for the zero-quartic PBW lemma.

Python 3.10+; standard library only. No modular or floating-point arithmetic,
no degree cutoff, no guessed Hilbert recurrence, and no Gröbner-basis search.
The supplied five-element basis, every ambiguity, and every syzygy identity
are checked. Run next to zero_quartic_certificate.json.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction
from pathlib import Path
import json

Q = Fraction
Polynomial = dict[str, Q]
Module = dict[tuple[str, int, str], Q]


def add(target: dict, source: dict, scalar: Q = Q(1)) -> dict:
    for key, value in source.items():
        value = target.get(key, Q(0)) + scalar * value
        if value:
            target[key] = value
        else:
            target.pop(key, None)
    return target


def poly(rows: list) -> Polynomial:
    return {word: Q(value) for word, value in rows}


def module(rows: list) -> Module:
    return {(left, i, right): Q(value) for left, i, right, value in rows}


def sandwich(p: Polynomial, left: str = '', right: str = '') -> Polynomial:
    return {left + word + right: value for word, value in p.items()}


def msandwich(p: Module, left: str = '', right: str = '') -> Module:
    return {(left + a, i, b + right): value for (a, i, b), value in p.items()}


def evaluate(p: Module, relations: list[Polynomial]) -> Polynomial:
    answer: Polynomial = {}
    for (left, i, right), value in p.items():
        add(answer, sandwich(relations[i], left, right), value)
    return answer


def key(word: str) -> tuple[int, str]:
    return len(word), word


def trim(p: list[int]) -> list[int]:
    while p and p[-1] == 0:
        p.pop()
    return p


def padd(a: list[int], b: list[int]) -> list[int]:
    answer = [0] * max(len(a), len(b))
    for i, value in enumerate(a):
        answer[i] += value
    for i, value in enumerate(b):
        answer[i] += value
    return trim(answer)


def pmult(a: list[int], b: list[int]) -> list[int]:
    answer = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            answer[i + j] += x * y
    return trim(answer)


def main() -> None:
    path = Path(__file__).with_name('zero_quartic_certificate.json')
    data = json.loads(path.read_text())
    relations = [poly(p) for p in data['relations']]
    assert relations == [
        {'xx': Q(1)},
        {'yyyy': Q(1), 'xyyx': Q(1), 'yxyx': Q(1), 'xyxy': Q(1)},
    ]
    basis = [poly(row['polynomial']) for row in data['groebner_basis']]
    expressions = [module(row['in_original_relations'])
                   for row in data['groebner_basis']]
    leading = [max(p, key=key) for p in basis]
    assert len(basis) == 5
    for p, expression, lm in zip(basis, expressions, leading):
        assert p[lm] == 1
        assert all(len(word) == len(lm) for word in p)
        assert evaluate(expression, relations) == p
        assert all(word == lm or key(word) < key(lm) for word in p)

    def normal_form(p: Polynomial) -> tuple[Polynomial, Module]:
        p = dict(p)
        remainder: Polynomial = {}
        history: Module = {}
        while p:
            word = max(p, key=key)
            coefficient = p.pop(word)
            for lm, rule, expression in zip(leading, basis, expressions):
                position = word.find(lm)
                if position < 0:
                    continue
                left, right = word[:position], word[position + len(lm):]
                tail = {w: c for w, c in rule.items() if w != lm}
                add(p, sandwich(tail, left, right), -coefficient)
                add(history, msandwich(expression, left, right), coefficient)
                break
            else:
                remainder[word] = coefficient
        return remainder, history

    for relation in relations:
        assert not normal_form(relation)[0]
    # Enumerate ALL overlaps and inclusions, not merely the pairs in a log.
    pairs: set[tuple] = set()

    def record(i: int, left: str, right: str,
               j: int, left2: str, right2: str) -> None:
        a, b = (i, left, right), (j, left2, right2)
        if a != b:
            pairs.add(tuple(sorted((a, b))))

    for i, u in enumerate(leading):
        for j, v in enumerate(leading):
            for position in range(len(u) - len(v) + 1):
                if u[position:position + len(v)] == v:
                    record(i, '', '', j, u[:position], u[position + len(v):])
            for overlap in range(1, min(len(u), len(v))):
                if u[-overlap:] == v[:overlap]:
                    record(i, '', v[overlap:], j, u[:-overlap], '')

    critical_cycles: list[Module] = []
    for a, b in sorted(pairs):
        p: Polynomial = {}
        expression: Module = {}
        for sign, (i, left, right) in ((1, a), (-1, b)):
            add(p, sandwich(basis[i], left, right), Q(sign))
            add(expression, msandwich(expressions[i], left, right), Q(sign))
        remainder, history = normal_form(p)
        assert not remainder
        cycle = add(expression, history, Q(-1))
        assert not evaluate(cycle, relations)
        if cycle:
            critical_cycles.append(cycle)
    assert len(pairs) == 17 and len(critical_cycles) == 11

    s1 = {('x', 0, ''): Q(1), ('', 0, 'x'): Q(-1)}
    U = {'yxyy': Q(1), 'yyxy': Q(1)}
    sigma = {('xy', 1, ''): Q(1), ('x', 1, 'y'): Q(-1),
             ('y', 1, 'x'): Q(1), ('', 1, 'yx'): Q(-1)}
    add(sigma, {(word, 0, ''): -c for word, c in U.items()})
    add(sigma, {('', 0, word): c for word, c in U.items()})
    assert s1 == module(data['s1']) and sigma == module(data['sigma'])
    assert not evaluate(s1, relations) and not evaluate(sigma, relations)

    def identity(description: list) -> Module:
        kind, *args = description
        if kind in ('s1', 'sigma'):
            left, right = args
            return msandwich(s1 if kind == 's1' else sigma, left, right)
        assert kind == 'peiffer'
        left, i, middle, j, right = args
        answer = {(left + word + middle, j, right): coefficient
                  for word, coefficient in relations[i].items()}
        add(answer, {(left, i, middle + word + right): -coefficient
                     for word, coefficient in relations[j].items()})
        return answer

    certified_cycles: list[Module] = []
    summands = 0
    for row in data['syzygies']:
        target = module(row['cycle'])
        answer: Module = {}
        for coefficient, description in row['decomposition']:
            add(answer, identity(description), Q(coefficient))
            summands += 1
        assert answer == target
        certified_cycles.append(target)
    canonical = lambda p: tuple(sorted(p.items()))
    assert Counter(map(canonical, critical_cycles)) == Counter(map(canonical, certified_cycles))
    assert summands == 31

    forbidden = [lm for lm in leading
                 if not any(other != lm and other in lm for other in leading)]
    assert set(forbidden) == set(data['minimal_forbidden_words'])
    hc = data['hilbert_certificate']
    states = sorted({word[:n] for word in forbidden for n in range(len(word))},
                    key=key)
    assert states == hc['states']
    denominator, numerators = hc['denominator'], hc['numerators']
    for i, state in enumerate(states):
        rhs = list(denominator)
        for letter in 'xy':
            word = state + letter
            if any(bad in word for bad in forbidden):
                continue
            next_state = max((v for v in states if word.endswith(v)), key=len)
            rhs = padd(rhs, [0] + numerators[states.index(next_state)])
        assert trim(rhs) == trim(list(numerators[i]))
    assert denominator == pmult(pmult([1, 1], [1, -2, 1]), [1, 0, 0, -1])
    assert numerators[states.index('')] == [1, 1]
    print('PASS: five homogeneous Gröbner relations lie in the original ideal.')
    print('PASS: all 17 overlaps/inclusions reduce to zero.')
    print('PASS: all 11 critical syzygies have exact free-bimodule identities.')
    print('      Only 31 multiples of s1, sigma, and Peiffer identities are used.')
    print('PASS: the 10-state automaton gives H_B(t)=1/((1-t)^2(1-t^3)).')
    print('All checks use exact integer/rational arithmetic; no truncation or primes.')


if __name__ == '__main__':
    main()
