#!/usr/bin/env python3
"""Exact independent checks for W00-T1; finite checks are not general proofs.

Run: python3 Audit/corpus-six-lines/check.py --output /tmp/w00-checks.json
Requires SymPy for symbolic coefficient comparison. All finite calculations
use Python integers and fractions, never approximate complex coordinates.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import platform
import sys
import sympy as sp


def mul(x, y):
    a, b = x
    c, d = y
    return a*c - b*d, a*d + b*c + b*d


def norm(z):
    a, b = z
    return a*a + a*b + b*b


def cube(z):
    return mul(mul(z, z), z)


def sixth(z):
    return mul(cube(z), cube(z))


def factors(z):
    a, b = z
    return 3*a*b*(a+b), (a-b)*(2*a+b)*(a+2*b)


def remainder(z):
    c, d = sixth(z)
    return c - norm(z)**3, d


def det(x, y):
    return x[0]*y[1] - x[1]*y[0]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    a, b, u, v, c, d = sp.symbols('a b u v c d')
    z, w = (a, b), (u, v)
    B, T = factors(z)
    C, D = sixth(z)
    expressions = {
        'cube_first': cube(z)[0] - (a**3 - 3*a*b*b - b**3),
        'cube_second': cube(z)[1] - B,
        'cube_twice_real': 2*cube(z)[0] + cube(z)[1] - T,
        'cube_norm': T*T + 3*B*B - 4*norm(z)**3,
        'sixth_second': D - B*T,
        'charter_product': D + 3*(b*(2*a+b))*(a*a-b*b)*(-a*(a+2*b)),
        'real_shift': 2*C + D - 2*norm(z)**3 + 3*B*B,
        'norm_multiplication': norm(mul(z, w)) - norm(z)*norm(w),
        'detector_determinant': norm(remainder(z)) - 3*norm(z)**3*B*B,
        'same_operator_cyclicity': det(w, mul(sixth(z), w)) - B*T*norm(w),
        'fixed_auxiliary': det(w, mul(sixth((2, 1)), w)) - 360*norm(w),
        'repaired_pair': det(mul(remainder(z), w),
            mul(sixth((2, 1)), mul(remainder(z), w)))
            - 1080*norm(z)**3*B*B*norm(w),
    }
    symbolic = {}
    for name, expr in expressions.items():
        zero = sp.Poly(sp.expand(expr), a, b, u, v, c, d).is_zero
        symbolic[name] = bool(zero)
        if not zero:
            raise AssertionError((name, sp.expand(expr)))

    counts = dict(parameters=0, blind=0, detecting_scalar=0, same_operator_cyclic=0,
                  vector_cases=0, repaired_reconstructions=0)
    vectors = [(u, v) for u in range(-2, 3) for v in range(-2, 3) if (u, v) != (0, 0)]
    for a in range(-12, 13):
        for b in range(-12, 13):
            if (a, b) == (0, 0):
                continue
            z = a, b
            B, T = factors(z)
            F, r = sixth(z), remainder(z)
            counts['parameters'] += 1
            category = 'blind' if B == 0 else ('detecting_scalar' if T == 0 else 'same_operator_cyclic')
            counts[category] += 1
            assert norm(z) > 0
            assert (F[1] == 0) == (B*T == 0)
            assert (norm(r) != 0) == (B != 0)
            if B == 0:
                assert r == (0, 0)
            if T == 0 and B != 0:
                assert F == (-norm(z)**3, 0)
            for w in vectors:
                counts['vector_cases'] += 1
                assert (det(w, mul(F, w)) != 0) == (B*T != 0)
                x = mul(r, w)
                y = mul(sixth((2, 1)), x)
                determinant = det(x, y)
                assert determinant == 1080*norm(z)**3*B*B*norm(w)
                assert (determinant != 0) == (B != 0)
                if determinant:
                    target = (7, -11)
                    s = Fraction(det(target, y), determinant)
                    t = Fraction(det(x, target), determinant)
                    assert (s*x[0] + t*y[0], s*x[1] + t*y[1]) == target
                    counts['repaired_reconstructions'] += 1

    # Load-bearing negative controls, not failed attempts presented as proofs.
    controls = {
        'scalar_detector': {
            'parameter': [1, 1], 'sixth': sixth((1, 1)),
            'remainder': remainder((1, 1)), 'detector_det': norm(remainder((1, 1))),
            'same_operator_det_at_one': det((1, 0), mul(sixth((1, 1)), (1, 0))),
            'repaired_det_at_one': det(mul(remainder((1, 1)), (1, 0)),
                mul(sixth((2, 1)), mul(remainder((1, 1)), (1, 0)))),
        },
        'unit_is_not_auxiliary_rotation': {'parameter': [0, 1], 'sixth': sixth((0, 1))},
        'fixed_auxiliary': {'parameter': [2, 1], 'norm': 7, 'sixth': sixth((2, 1))},
        'zero_seed': {'w': [0, 0], 'repaired_det': 0},
    }
    assert controls['scalar_detector']['detector_det'] == 2916
    assert controls['scalar_detector']['repaired_det_at_one'] == 1049760
    assert sixth((0, 1)) == (1, 0)
    assert sixth((2, 1)) == (-323, 360)
    result = {
        'scope': 'Fresh exact symbolic identities and bounded integer-plane sanity checks; not a Lean or Hodge check',
        'python': sys.version.split()[0], 'sympy': sp.__version__, 'platform': platform.platform(),
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'symbolic_identities': symbolic, 'finite_bounds': {'parameter_abs_max': 12, 'vector_abs_max': 2},
        'finite_counts': counts, 'controls': controls, 'all_checks_passed': True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
