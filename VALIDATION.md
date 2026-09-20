# Local validation receipt

Date: 2026-09-20. Status: the electrical citation surface and the transport
interface are validated for the bounded claims below. The soundness criterion,
hyperphysics' own ground, and dimensional analysis remain open.

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
  `5fbc3b9b8ab6e89ddb85569c704b66e8ad908e461a8d65e2ddebb6d50b26df09`.
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
