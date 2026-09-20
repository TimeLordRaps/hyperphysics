"""Tests for the stated laws and their exact consequences."""

from __future__ import annotations

import pytest

from hyperphysics.electrical import (
    CAPACITOR,
    LAWS,
    LAWS_BY_NAME,
    PARAMETERS_ARE_INDEPENDENT,
    QUANTITIES,
    QUANTITY_INFO,
    SERIES_RLC,
    SERIES_RLC_CONSTITUENTS,
    Law,
    Quantity,
    characteristic_impedance,
    damping_ratio,
    derivative_chain,
    derivative_order,
    dissipated_power,
    impedance_magnitude,
    reactance,
    regime,
    resonant_angular_frequency,
    stored_energy,
)

# --- quantities -------------------------------------------------------------


def test_every_quantity_has_exactly_one_info_record():
    assert len(QUANTITIES) == len(Quantity)
    assert set(QUANTITY_INFO) == set(Quantity)


def test_every_quantity_carries_an_si_unit():
    """A transport must be able to name the unit it declines to carry."""
    for info in QUANTITIES:
        assert info.si_unit.strip()


def test_the_state_quantities_are_exactly_the_derivative_chain():
    state = {info.quantity for info in QUANTITIES if info.is_state}
    assert state == set(derivative_chain())


def test_the_derivative_chain_is_ordered_by_differentiation():
    assert derivative_order(Quantity.CHARGE) == 0
    assert derivative_order(Quantity.CURRENT) == 1
    assert derivative_order(Quantity.CURRENT_RATE) == 2


def test_a_parameter_is_not_on_the_derivative_chain():
    with pytest.raises(ValueError, match="not on the derivative chain"):
        derivative_order(Quantity.INDUCTANCE)


# --- laws -------------------------------------------------------------------


@pytest.mark.parametrize("law", LAWS, ids=lambda law: law.name)
def test_every_law_records_validity_and_failure_modes(law):
    """The failure modes are what a borrower inherits, so none may be empty."""
    assert law.validity.strip()
    assert law.fails_when
    assert all(mode.strip() for mode in law.fails_when)


def test_law_names_are_unique():
    names = [law.name for law in LAWS]
    assert len(set(names)) == len(names)
    assert set(LAWS_BY_NAME) == set(names)


def test_a_law_must_record_a_failure_mode():
    with pytest.raises(ValueError, match="at least one failure mode"):
        Law("x", "statement", "form", (Quantity.CHARGE,), "validity", ())


def test_a_law_must_relate_a_quantity():
    with pytest.raises(ValueError, match="at least one quantity"):
        Law("x", "statement", "form", (), "validity", ("fails",))


def test_the_series_form_is_the_composition_of_its_constituents():
    """series-rlc is not a fifth independent law."""
    assert {law.name for law in SERIES_RLC_CONSTITUENTS} == {
        "faraday-lenz", "ohm", "capacitor", "kirchhoff-voltage",
    }
    assert SERIES_RLC.form == "L * d2Q/dt2 + R * dQ/dt + (1/C) * Q = V"


def test_the_series_form_relates_every_free_parameter():
    assert set(PARAMETERS_ARE_INDEPENDENT) <= set(SERIES_RLC.quantities)


def test_capacitance_is_stated_as_charge_per_unit_potential():
    """C = Q/V is the reading the will transport's constant will depends on."""
    assert "charge stored per unit potential" in CAPACITOR.statement


def test_self_and_mutual_inductance_share_a_form_and_differ_in_source():
    """The distinction is entirely about whose current does the inducing."""
    self_law = LAWS_BY_NAME["self-inductance"]
    mutual = LAWS_BY_NAME["mutual-inductance"]
    assert "-L * dI/dt" in self_law.form
    assert "-M * dI_1/dt" in mutual.form
    assert "own changing current" in self_law.statement
    assert "second circuit" in mutual.statement


def test_the_free_parameters_are_r_l_and_c():
    """Stated explicitly because it is where a borrower may depart."""
    assert set(PARAMETERS_ARE_INDEPENDENT) == {
        Quantity.RESISTANCE, Quantity.INDUCTANCE, Quantity.CAPACITANCE,
    }


# --- exact consequences -----------------------------------------------------


def test_resonance_is_where_net_reactance_vanishes():
    inductance, capacitance = 2.0, 8.0
    omega = resonant_angular_frequency(inductance, capacitance)
    assert reactance(omega, inductance, capacitance) == pytest.approx(0.0, abs=1e-12)


def test_impedance_is_minimal_at_resonance():
    resistance, inductance, capacitance = 3.0, 2.0, 8.0
    omega = resonant_angular_frequency(inductance, capacitance)
    at_resonance = impedance_magnitude(resistance, omega, inductance, capacitance)
    assert at_resonance == pytest.approx(resistance)
    for offset in (0.5, 1.5, 2.0):
        other = impedance_magnitude(resistance, omega * offset, inductance, capacitance)
        assert other > at_resonance


def test_damping_ratio_is_half_the_resistance_over_characteristic_impedance():
    resistance, inductance, capacitance = 3.0, 2.0, 8.0
    expected = resistance / (2.0 * characteristic_impedance(inductance, capacitance))
    assert damping_ratio(resistance, inductance, capacitance) == pytest.approx(expected)


def test_damping_regimes_are_named_at_the_right_boundaries():
    assert regime(1.0, 1.0, 1.0) == "underdamped"
    assert regime(2.0, 1.0, 1.0) == "critically-damped"
    assert regime(3.0, 1.0, 1.0) == "overdamped"


def test_zero_resistance_is_undamped():
    assert damping_ratio(0.0, 1.0, 1.0) == 0.0
    assert regime(0.0, 1.0, 1.0) == "underdamped"


def test_only_resistance_dissipates():
    """Dissipated power names no inductance and no capacitance."""
    assert dissipated_power(3.0, 2.0) == pytest.approx(18.0)
    assert dissipated_power(3.0, 0.0) == 0.0


def test_stored_energy_is_carried_by_the_reactive_elements():
    magnetic_only = stored_energy(2.0, 3.0, 1.0, 0.0)
    assert magnetic_only == pytest.approx(9.0)
    electric_only = stored_energy(1.0, 0.0, 2.0, 4.0)
    assert electric_only == pytest.approx(4.0)


def test_numeric_functions_reject_nonpositive_parameters():
    for bad in ((0.0, 1.0), (1.0, 0.0), (-1.0, 1.0), (1.0, -1.0)):
        with pytest.raises(ValueError, match="must be positive"):
            resonant_angular_frequency(*bad)
        with pytest.raises(ValueError, match="must be positive"):
            characteristic_impedance(*bad)


def test_numeric_functions_reject_negative_resistance():
    with pytest.raises(ValueError, match="must not be negative"):
        damping_ratio(-1.0, 1.0, 1.0)
    with pytest.raises(ValueError, match="must not be negative"):
        dissipated_power(1.0, -1.0)
    with pytest.raises(ValueError, match="must not be negative"):
        impedance_magnitude(-1.0, 1.0, 1.0, 1.0)


def test_reactance_rejects_a_nonpositive_drive_frequency():
    with pytest.raises(ValueError, match="must be positive"):
        reactance(0.0, 1.0, 1.0)
