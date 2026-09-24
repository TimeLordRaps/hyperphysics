# Design

Status: one implemented piece — electrical law as a citation surface — plus the
interface a borrowing field must satisfy. Date: 2026-09-20. The field's ground is
not written and nothing here claims to be it.

## Why a physics repository contains no new physics

Everything in `electrical.py` is classical circuit theory in the lumped-element
approximation, and every reader of an undergraduate text already has it. The
package exists for a different reason.

Adjacent fields in this family borrow the *shape* of physical law.
`metamathethicology.will_electrophysics` transports the series-RLC form onto the
will tensor `hyperethics` declares: resistance becomes relational will,
inductance becomes invariant will, voltage becomes variable will. That
borrowing is a cross-domain inference. It is not automatically illegitimate and
it is not automatically sound, and the only thing that makes it *checkable* is
that the borrower says exactly what it took and exactly what it left.

A borrower cannot say what it left behind unless the thing it borrowed from is
fixed. If each borrower restates Ohm's law in its own words, then two years later
there are four slightly different Ohm's laws in four repositories, and the
sentence "this does not transport ohms" no longer refers to anything in
particular. So the laws are stated once, here, and borrowers cite them.

## Failure modes are the payload

Each `Law` carries `validity` and `fails_when` as structured data rather than
prose. That is deliberate: prose gets skimmed, and a borrower who skims the
validity conditions inherits them anyway.

`SERIES_RLC` is the case that makes this concrete. It is not a fifth independent
law — it is Kirchhoff's voltage law applied to three constitutive relations. A
field transporting the series form inherits fourteen failure modes, not three, and
`inherited_failure_modes` computes the closure rather than trusting the borrower
to remember the decomposition.

## Parameter independence is stated so it can be departed from

`PARAMETERS_ARE_INDEPENDENT` records that R, L, and C are independent parameters
of a series RLC circuit. This looks like a triviality worth no line of code.

It is there because it is the single most likely place for a silent
disagreement. A field may perfectly reasonably constrain its analogue of C to be
a function of its analogue of L — `metamathethicology.will_electrophysics` does
exactly this, on the declaration that capacitance is invariant will's constant of
charge. The
consequence is that its parameter space is a *proper subset* of the circuit's, so
the transport is not onto and no circuit intuition about tuning the two
independently survives.

That is a real structural difference. Left undeclared, a reader imports the
circuit's freedom along with its algebra and reasons about a space the target
field does not have. So `Transport.constrains_parameters` makes the departure a
required declaration with a required reason, and constraining something the
source never left free is rejected as a non-departure.

## What validation buys, and what it does not

`validate` checks that the required declarations were made and that they are
about the law they claim to be about. Specifically it rejects a disclaimer
naming neither a unit nor a mechanism of the cited law, so a borrower cannot
discharge the obligation with a general assurance.

It does **not** check that the transport is sound, and no function in this
package can. `test_validation_is_not_a_soundness_check` builds a deliberately
absurd transport and asserts that it validates, because a limit that is only
mentioned in a docstring is a limit nobody enforces. Passing validation must
never be mistaken for having earned the borrowing.

This is the package's real open problem, recorded as `GC-4`: a criterion for
soundness rather than mere declaration. Nothing here supplies one.

## Why the file carries no layer index

`electrical.hm`, not `L0_electrical.hm`.

hypermath's L0 is ground and apply. hyperethics' L0 is creation under immanence.
Both earned their index by being the thing everything above them is derived from.
Circuit theory is not that for physics — it is a long way up from any plausible
ground, and this package does not have the ground to place it against.

Taking the index anyway would be the same kind of error the rest of this family
is built to avoid: asserting a structural claim because it makes the file naming
tidy. The file gets re-indexed when there is a ground to index it against.

## Dependencies

None. The package imports only the standard library, as `hyperethics` does, and
for the same reason: a surface other fields cite should not drag a dependency
graph into every field that cites it.

The borrower does not import this package at runtime either.
`metamathethicology.will_electrophysics` cites law names as strings and quotes
the forms, and that package's `tests/test_citations.py` cross-checks every
citation whenever `hyperphysics` happens to be importable, skipping loudly when
it is not. That keeps the citation verifiable without making either cited field
depend on the other, and a skip there is recorded as a skip rather than counted
as a pass.

## Open, in order

1. **A soundness criterion for transports** (`GC-4`). The interface makes
   borrowings explicit and comparable. It does not rank them. Some notion of
   structural adequacy — perhaps that the target independently reproduces a
   relation the source predicts, as the will transport's `d-self-simulation`
   reproduces `hyperethics`' independently derived `d-no-exterior` — is the
   obvious candidate and is not worked out.
2. **hyperphysics' ground** (`GC-5`), of which circuit theory would be a
   consequence rather than a starting point.
3. **Units and dimensional analysis** (`GC-6`). The numeric functions take
   dimensionless magnitudes and unit handling is the caller's obligation. A
   package about physical law that cannot check a dimension is incomplete, and
   this is the honest name for that gap.
4. **More law families.** Mechanics, thermodynamics, and wave equations are the
   obvious next borrowing surfaces. None is implemented, and adding one means
   adding its failure modes, not just its algebra.
