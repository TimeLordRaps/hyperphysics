# Local validation receipt

Date: 2026-09-20. Status: the electrical citation surface and the transport
interface are validated for the bounded claims below. The soundness criterion,
hyperphysics' own ground, and dimensional analysis remain open.

This receipt supersedes an earlier one of the same date. The only change is that
the borrower these laws are cited by is now named correctly throughout: the
electrical reading of the will tensor moved from `hyperethics` to the combination
field `metamathethicology.will_electrophysics`, on a placement declared by the
author. No law, no numeric function, and no part of the transport interface
changed; the 55 checks below are the same 55 and passed again after the rename.

## Coordinates

- Repository `hyperphysics`, branch `main`, private repository
  `TimeLordRaps/hyperphysics`. The validated bytes were committed and pushed
  unchanged. Publication records where they live; it is not an additional check.
- Python 3.12.8 on Windows, pytest 9.1.1, ruff 0.16.8.
- **No runtime dependencies.** The package imports only the standard library, so
  there are no dependency pins to record and no dependency source to trust.
- The tests were executed with the interpreter from the `hyperethics` virtual
  environment on this host, which supplies pytest and ruff. No separate
  environment was created, and nothing from `hyperethics` is imported by this
  package.
- The implementation and tests are byte-bound in
  [`validation/source-manifest.json`](validation/source-manifest.json). The digest
  of its canonical `files` mapping is
  `23250c5caa5a4597642acb7df9ccb6c69c4e1eae593477af4f6f584186160db1`, and was
`5fbc3b9b8ab6e89ddb85569c704b66e8ad908e461a8d65e2ddebb6d50b26df09` before the
borrower was renamed. `electrical.hm`, `src/hyperphysics/electrical.py`, and two
test docstrings are the only files whose bytes changed.
  The manifest identifies tested bytes; it does not sign or certify them.

## Observed checks

```console
python -m pytest tests
python -m ruff check src tests
```

- **55 tests passed with zero skips.** Lint passed with no findings.
- Every law records a nonempty `validity` and at least one failure mode, and the
  `Law` constructor rejects a law that records neither. This is asserted for all
  seven laws, not spot-checked.
- **Composition is checked, not asserted.** Transporting `series-rlc` inherits
  strictly more failure modes than transporting `ohm` and `capacitor` together,
  the constituents' modes are all present, and the result is deduplicated.
- **Resonance is verified against the model rather than quoted.** Net reactance
  is zero at `1/sqrt(LC)` to within 1e-12, and impedance magnitude at resonance
  equals the resistance and is strictly less than at four off-resonance
  frequencies.
- The damping ratio is independently checked to equal half the resistance over
  the characteristic impedance, and the three regime boundaries are checked at
  their exact transitions.
- Dissipated power is a function of current and resistance alone; stored energy
  is carried entirely by the two reactive terms. These are the formal
  counterparts of "only resistance dissipates".
- **The interface rejects what it is meant to reject.** A citation of a
  nonexistent law raises `UnknownLaw` and the error lists the laws that do exist.
  Each of the five required declarations is checked individually for emptiness.
  A disclaimer that names no unit and no mechanism is rejected, and so is one
  naming a unit belonging to a *different* law than the one cited.
- Constraining a free source parameter without a reason is rejected; constraining
  a quantity the source never left free is rejected as a non-departure.
- Negative cases reject nonpositive inductance and capacitance, negative
  resistance, a nonpositive drive frequency, a non-`Quantity` in
  `constrains_parameters`, a non-`Warrant` warrant, and a quantity not on the
  derivative chain.

## What the checks do not establish

- **`validate` is not a soundness check.** It verifies that the required
  declarations were made and are about the cited law. A perfectly declared
  transport may be a bad analogy, and no function here can tell the difference.
  `test_validation_is_not_a_soundness_check` builds a deliberately absurd
  transport and asserts that it passes, so this limit is enforced rather than
  merely documented. `GC-4` records it as the package's principal open problem.
- **No new physics is established, and none is claimed.** The laws are textbook
  classical circuit theory in the lumped-element approximation. The tests check
  that this package states them consistently and computes their exact
  consequences correctly. They do not check them against nature, and no
  measurement of any kind was performed.
- **`GC-6`, units and dimensional analysis, is not discharged.** The numeric
  functions take dimensionless magnitudes. A caller may pass inconsistent units
  and nothing here will notice. For a package about physical law this is a real
  gap, not a simplification.
- **`GC-5`, hyperphysics' own ground, is not written.** `electrical.hm`
  deliberately carries no layer index rather than a wrong one.
- **Nothing here checks the live borrower.** The cross-check that holds
  `metamathethicology.will_electrophysics` to these exact bytes runs in *that*
  repository and is recorded in its receipt. This suite never imports it, so a
  borrower drifting from a law stated here would be caught there and not here.
- The failure modes recorded per law are those the author judged load-bearing
  for a borrower. They are not claimed to be exhaustive, and no source is cited
  for their completeness.

## Exclusions

- `OS_CAPABILITY_GUARD`: Linux and macOS execution and cross-platform build
  comparison were not run on this Windows host.
- `PERFORMANCE_OR_DURATION_EXCLUSION`: no numerical stability analysis, no
  property-based testing over parameter ranges, and no floating-point error
  bounds were established. The numeric checks use hand-chosen values with
  `pytest.approx` tolerances. Other Python versions were not exercised.
- `EXTERNAL_SERVICE_BOUNDARY`: no continuous integration, release publication,
  or package-index installation was performed. A wheel and source distribution
  were not built.
- The host checker trusts Python and ordinary in-process object integrity.
- **No preprint exists for this repository**, and no check here bears on one.
  `FIELD_STACK.md` records the declared subject matter of hyperphysics and of
  the two fields declared above it; it is an author declaration, not a result,
  and nothing in this package entails it or checks it. It does not discharge
  GC-5.

## Addendum, 2026-10-03: `hyperphysics.limits`

This addendum adds one module and its tests. It changes nothing above: no byte of
a file named in `validation/source-manifest.json` was altered (`__init__.py` does
not re-export the new module), so the digest recorded above still describes the
bytes it names. **`src/hyperphysics/limits.py` and `tests/test_limits.py` are not
in that manifest** and are not covered by that digest.

- Coordinates: branch `claude/order-of-limits`, Linux, Python 3.11 and 3.10, pytest
  with `--timeout=30`, ruff with the repository configuration.
- **73 tests passed with zero skips** (the 55 above plus 18 new). Lint passed.
  Windows and Python 3.12 or 3.13 were not exercised on this host.
- The estimator refuses what it cannot certify: slow algebraic convergence, a drift
  below the tolerance, divergence, and an inner limit that has not settled are each
  tested to be reported `UNSETTLED` or `DIVERGED`, never as a limit.
- The decision rule is tested at its edges: two answers closer than their own
  uncertainty are `UNKNOWN`, not `COMMUTE`.
- **Mutation checks, each of which made at least one test fail:** a contraction test
  that accepts anything, a decision rule that always returns `COMMUTE`, ignoring an
  unsettled inner limit, swapping inner and outer, and disabling divergence
  detection. An earlier version of the suite let the first of these survive; a test
  for drifting sequences was added.
- Physical case: the Curie--Weiss ferromagnet at `beta = 2`, exact finite-`N` sums.
  `lim[h→0+] lim[N→∞]` gave `0.95773` certified to about `8e-4`, against the
  mean-field fixed point `m = tanh(2m) = 0.9575` computed independently by
  iteration; `lim[N→∞] lim[h→0+]` gave about `4e-15`. At `beta = 0.5` the two orders
  agree. A schedule that does not reach `N h beta m >> 1` at its smallest `h` is
  reported unsettled.

What this does not establish:

- The error bound assumes contraction continues beyond the sampled range. It is an
  assumption, stated in the module, not a check.
- The loop-quantum-gravity instance (large spin, then refinement) is not
  implemented; no claim about gravity follows.
- A tolerance of `1e-3` was chosen, and stated in the test, for the `N`-limit,
  because corrections fall like `1/N` and the schedule stops at `N = 12800`; the
  default `1e-6` is asserted to refuse it.
- Units: every quantity is dimensionless, as elsewhere in this package (GC-6).

