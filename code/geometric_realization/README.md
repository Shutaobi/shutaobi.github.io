# Computational code for Geometric Realization

These programs reproduce the exact calculations in Section 6 of Shutao Bi's [November 2026 revision of *Geometric Realization*](https://shutaobi.github.io/thesis/Geometric_Realization.pdf?v=0dc853e1179c).

## Run the checks

Use Python 3.10 or later with assertions enabled. From the extracted package directory, run the two standard-library checks first.

```sh
cd tools/numerical_realisation_certificates
python3 verify_cyclic_reductions.py
python3 verify_zero_quartic.py
cd ../..
```

The length-five program requires SymPy and mpmath. From the package directory, install the pinned versions in a virtual environment. `--output` directs the new calculation to `build/` so the supplied reference remains available for comparison.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-certificates.txt
cd tools/numerical_realisation_certificates
python nr_B5_generic_certificate.py --output ../../build/nr_B5_rerun.json
cmp ../../build/nr_B5_rerun.json nr_B5_generic_certificate.json
```

On Windows, activate the environment with `.venv\Scripts\activate` and compare the two JSON files with `fc.exe /b` in place of `cmp`. A matching file gives exit status zero.

## Where the calculations enter the paper

- **Lemma 2.12 and Theorem 2.17.** `verify_cyclic_reductions.py` checks the ten overlaps in the length-three reduction over `Z[T]` and the twelve irreducible words. For length six it computes the ranks of the ordinary and cyclic relation matrices over the rationals. The algebra has dimension 60 and vanishes in degree 15. Its cocenter has dimensions 1, 2, 2, 1, 1 in degrees zero through four and vanishes in higher degrees. The script checks the seven proposed generators.
- **Lemma 3.4.** `nr_B5_generic_certificate.py` computes the two specializations of the auxiliary algebra. Their dimensions at `S=0` and `S=1` are 40 and 25. At `S=1` the regular trace determinant is `298023223876953125 = 5^25`, and the center has dimension one. The accompanying `nr_B5_generic_certificate.json` records the bases, matrices, and exact output.
- **Lemma 4.9.** `verify_zero_quartic.py` reads the adjacent `zero_quartic_certificate.json`. It checks the five ideal identities, the seventeen ambiguities, the eleven critical syzygies and their thirty-one summands. The ten-state automaton gives the Hilbert series `1/((1-t)^2(1-t^3))`.
