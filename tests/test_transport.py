"""Tests for the transport interface: what a borrowing field must declare."""

from __future__ import annotations

import pytest

from hyperphysics.electrical import Quantity
from hyperphysics.transport import (
    UNITS_DO_NOT_TRANSPORT,
    Transport,
    UndeclaredTransport,
    UnknownLaw,
    Warrant,
    audit,
    cited_law,
    inherited_failure_modes,
    validate,
)


def a_transport(**overrides) -> Transport:
    """A well-formed transport, with fields overridable per test."""
    defaults = dict(
        law="ohm",
        target_field="example",
        target_form="relational * present",
        transports="that the coefficient opposes the flow in direct proportion",
        does_not_transport="ohms, volts, amperes, or linearity in fact",
        warrant=Warrant.BORROWED_FORM,
    )
    defaults.update(overrides)
    return Transport(**defaults)


# --- citation ---------------------------------------------------------------


def test_a_transport_resolves_to_the_law_it_cites():
    assert cited_law(a_transport()).form == "V = I * R"


def test_citing_a_law_this_package_does_not_state_is_an_error():
    """A citation with no referent is the failure mode this interface exists for."""
    with pytest.raises(UnknownLaw, match="does not state"):
        cited_law(a_transport(law="conservation-of-vibes"))


def test_the_unknown_law_error_lists_the_laws_that_do_exist():
    with pytest.raises(UnknownLaw, match="series-rlc"):
        cited_law(a_transport(law="nope"))


# --- required declarations --------------------------------------------------


@pytest.mark.parametrize(
    "missing",
    ["law", "target_field", "target_form", "transports", "does_not_transport"],
)
def test_every_required_declaration_must_be_nonempty(missing):
    with pytest.raises(UndeclaredTransport, match=missing):
        a_transport(**{missing: "   "})


def test_the_warrant_must_be_a_warrant():
    with pytest.raises(TypeError, match="Warrant"):
        a_transport(warrant="BORROWED_FORM")


def test_validation_requires_disclaiming_a_unit_of_the_cited_law():
    """A general assurance does not satisfy the interface."""
    with pytest.raises(UndeclaredTransport, match="must disclaim"):
        validate(a_transport(does_not_transport="anything not intended"))


def test_naming_a_mechanism_satisfies_the_disclaimer_instead_of_a_unit():
    validated = validate(
        a_transport(does_not_transport="any physical mechanism of conduction")
    )
    assert validated.warrant is Warrant.BORROWED_FORM


def test_disclaiming_a_unit_of_a_different_law_does_not_satisfy_the_interface():
    """Farads are not a quantity of Ohm's law, so disclaiming them is off-target."""
    with pytest.raises(UndeclaredTransport, match="must disclaim"):
        validate(a_transport(law="ohm", does_not_transport="farads"))


def test_validation_returns_the_transport_unchanged():
    transport = a_transport()
    assert validate(transport) is transport


# --- inherited failure modes ------------------------------------------------


def test_a_transport_inherits_its_law_s_failure_modes():
    modes = inherited_failure_modes(a_transport(law="ohm"))
    assert any("non-ohmic" in mode for mode in modes)


def test_transporting_the_series_form_inherits_all_four_constituents():
    """The series form is a composition, so the borrower inherits the composition."""
    series = inherited_failure_modes(a_transport(law="series-rlc"))
    ohm = inherited_failure_modes(a_transport(law="ohm"))
    capacitor = inherited_failure_modes(a_transport(law="capacitor"))
    assert set(ohm) <= set(series)
    assert set(capacitor) <= set(series)
    assert len(series) > len(ohm) + len(capacitor)


def test_inherited_failure_modes_are_deduplicated():
    modes = inherited_failure_modes(a_transport(law="series-rlc"))
    assert len(set(modes)) == len(modes)


# --- declared departures from the source's parameter space ------------------


def test_constraining_a_free_parameter_requires_a_reason():
    """The departure hyperethics makes: capacitance bound rather than free."""
    with pytest.raises(UndeclaredTransport, match="must say why"):
        a_transport(
            law="series-rlc",
            constrains_parameters=(Quantity.CAPACITANCE,),
        )


def test_a_declared_constraint_is_accepted_with_its_reason():
    transport = a_transport(
        law="series-rlc",
        does_not_transport="farads, henries, ohms, or volts",
        constrains_parameters=(Quantity.CAPACITANCE,),
        constraint_reason="capacitance is the invariant's constant of charge, "
                          "so it is not independently variable",
    )
    assert validate(transport).constrains_parameters == (Quantity.CAPACITANCE,)


def test_constraining_something_the_source_never_left_free_is_rejected():
    """Charge is a state variable, not a free parameter, so binding it is no departure."""
    with pytest.raises(UndeclaredTransport, match="not one of the circuit's free parameters"):
        a_transport(
            constrains_parameters=(Quantity.CHARGE,),
            constraint_reason="a reason",
        )


def test_constrains_parameters_must_hold_quantities():
    with pytest.raises(TypeError, match="Quantity"):
        a_transport(constrains_parameters=("capacitance",), constraint_reason="r")


# --- audit ------------------------------------------------------------------


def test_the_audit_leads_with_the_standing_rule_about_units():
    lines = audit((a_transport(),))
    assert lines[0] == UNITS_DO_NOT_TRANSPORT
    assert "unit" in UNITS_DO_NOT_TRANSPORT.lower()


def test_the_audit_publishes_both_sides_of_every_borrowing():
    lines = "\n".join(audit((a_transport(),)))
    assert "source form:  V = I * R" in lines
    assert "target form:  relational * present" in lines
    assert "disclaims:" in lines
    assert "inherits 3 failure modes" in lines


def test_the_audit_publishes_a_declared_constraint():
    transport = a_transport(
        law="series-rlc",
        does_not_transport="farads and henries",
        constrains_parameters=(Quantity.CAPACITANCE,),
        constraint_reason="bound to the invariant",
    )
    lines = "\n".join(audit((transport,)))
    assert "CONSTRAINS:   capacitance -- bound to the invariant" in lines


def test_the_audit_validates_what_it_publishes():
    with pytest.raises(UndeclaredTransport):
        audit((a_transport(does_not_transport="nothing in particular"),))


def test_validation_is_not_a_soundness_check():
    """A perfectly declared transport may still be a bad analogy.

    Nothing in this package can tell the difference, and the docstring says so.
    """
    absurd = a_transport(
        target_field="tuesday",
        target_form="tuesday = mood * ohms-of-the-week",
        transports="that tuesdays resist proportionally",
        does_not_transport="ohms",
    )
    assert validate(absurd) is absurd
    assert "does not check that the transport is sound" in validate.__doc__
