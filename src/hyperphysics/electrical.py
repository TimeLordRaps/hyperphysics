"""Electrical law, stated once, so that adjacent fields can cite it instead of
paraphrasing it.

WHY THIS MODULE EXISTS
----------------------
Adjacent fields borrow the algebraic shape of electrical law. `hyperethics`
transports the series-RLC form onto a will tensor; other fields will want the
same laws for their own purposes. Left to themselves, each borrower restates the
law in its own words, and the restatements drift. When they drift, the phrase
"this does not transport" loses its referent, because there is no longer a
canonical statement of what was borrowed.

So the laws live here, with their validity conditions and their known failure
modes attached, and borrowers cite them by name. `hyperphysics.transport`
supplies the interface a borrower must satisfy.

WHAT IS AND IS NOT CLAIMED
--------------------------
Everything in this module is textbook classical circuit theory in the lumped-
element approximation. Nothing here is new physics and nothing is presented as
new. The contribution is that each law carries its validity conditions and its
failure modes as data rather than as prose a borrower may skip, which is what
makes a citation checkable.

Numeric functions are exact for the idealized model and are not measurements.
They take dimensionless magnitudes; unit handling is the caller's obligation and
is recorded as an open obligation in `VALIDATION.md`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

# ---------------------------------------------------------------------------
# Quantities.
# ---------------------------------------------------------------------------


class Quantity(str, Enum):
    """The electrical quantities the laws below relate."""

    CHARGE = "charge"
    CURRENT = "current"
    CURRENT_RATE = "current-rate"
    RESISTANCE = "resistance"
    INDUCTANCE = "inductance"
    CAPACITANCE = "capacitance"
    VOLTAGE = "voltage"


@dataclass(frozen=True, slots=True)
class QuantityInfo:
    """A quantity's symbol, SI unit, and role in the state of a circuit."""

    quantity: Quantity
    symbol: str
    si_unit: str
    is_state: bool
    note: str


QUANTITIES: tuple[QuantityInfo, ...] = (
    QuantityInfo(
        Quantity.CHARGE, "Q", "coulomb", True,
        "accumulated charge; the time integral of current",
    ),
    QuantityInfo(
        Quantity.CURRENT, "I", "ampere", True,
        "dQ/dt, the first time derivative of charge",
    ),
    QuantityInfo(
        Quantity.CURRENT_RATE, "dI/dt", "ampere per second", True,
        "d2Q/dt2, the second time derivative of charge; what inductance opposes",
    ),
    QuantityInfo(
        Quantity.RESISTANCE, "R", "ohm", False,
        "the only dissipative element of a series RLC circuit",
    ),
    QuantityInfo(
        Quantity.INDUCTANCE, "L", "henry", False,
        "opposition to change in current; stores energy in a magnetic field",
    ),
    QuantityInfo(
        Quantity.CAPACITANCE, "C", "farad", False,
        "charge stored per unit potential difference, C = Q/V; stores energy in "
        "an electric field",
    ),
    QuantityInfo(
        Quantity.VOLTAGE, "V", "volt", False,
        "potential difference; the driving term of a series circuit",
    ),
)

QUANTITY_INFO: dict[Quantity, QuantityInfo] = {q.quantity: q for q in QUANTITIES}


def derivative_chain() -> tuple[Quantity, ...]:
    """Charge, current, and rate of change of current, in derivative order.

    These are not three independent quantities. They are the zeroth, first, and
    second time derivatives of a single quantity, and that is the entire content
    of the temporal structure of a circuit's state.
    """
    return (Quantity.CHARGE, Quantity.CURRENT, Quantity.CURRENT_RATE)


def derivative_order(quantity: Quantity) -> int:
    """How many times charge is differentiated to reach this quantity."""
    chain = derivative_chain()
    if quantity not in chain:
        raise ValueError(f"{quantity.value} is not on the derivative chain")
    return chain.index(quantity)


# ---------------------------------------------------------------------------
# Laws.
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Law:
    """A named electrical law with its form, validity, and failure modes.

    `validity` and `fails_when` are the parts a borrower needs. A transported
    form inherits the failure modes of its source unless the borrower explicitly
    argues otherwise, and it cannot make that argument against a statement it
    never read.
    """

    name: str
    statement: str
    form: str
    quantities: tuple[Quantity, ...]
    validity: str
    fails_when: tuple[str, ...]

    def __post_init__(self) -> None:
        for field, label in (
            (self.name, "name"), (self.statement, "statement"),
            (self.form, "form"), (self.validity, "validity"),
        ):
            if type(field) is not str or not field.strip():
                raise ValueError(f"law {label} must be a nonempty string")
        if type(self.quantities) is not tuple or not self.quantities:
            raise ValueError("a law must relate at least one quantity")
        for quantity in self.quantities:
            if type(quantity) is not Quantity:
                raise TypeError("law quantities must be Quantity members")
        if type(self.fails_when) is not tuple or not self.fails_when:
            raise ValueError("a law must record at least one failure mode")


OHM = Law(
    name="ohm",
    statement="The potential difference across a resistor is proportional to the "
              "current through it, with resistance as the constant.",
    form="V = I * R",
    quantities=(Quantity.VOLTAGE, Quantity.CURRENT, Quantity.RESISTANCE),
    validity="Ohmic materials at constant temperature, in the lumped-element "
             "approximation.",
    fails_when=(
        "the element is non-ohmic, as with a diode or a plasma",
        "resistance varies with temperature under self-heating",
        "the element is not small compared with the signal wavelength",
    ),
)

FARADAY_LENZ = Law(
    name="faraday-lenz",
    statement="The voltage across an inductor is proportional to the rate of "
              "change of current through it; the induced effect opposes the "
              "change that produced it.",
    form="V = L * dI/dt",
    quantities=(Quantity.VOLTAGE, Quantity.INDUCTANCE, Quantity.CURRENT_RATE),
    validity="Constant inductance, in the lumped-element approximation.",
    fails_when=(
        "the core saturates, so inductance depends on current",
        "geometry changes, so inductance is not constant",
        "radiation is not negligible",
    ),
)

CAPACITOR = Law(
    name="capacitor",
    statement="The potential difference across a capacitor is the stored charge "
              "divided by the capacitance. Equivalently, capacitance is the "
              "charge stored per unit potential difference.",
    form="V = Q / C",
    quantities=(Quantity.VOLTAGE, Quantity.CHARGE, Quantity.CAPACITANCE),
    validity="Constant capacitance, below the dielectric breakdown voltage.",
    fails_when=(
        "the dielectric breaks down",
        "capacitance is voltage dependent, as in a varactor or a ferroelectric",
        "leakage current is not negligible over the timescale of interest",
    ),
)

SELF_INDUCTANCE = Law(
    name="self-inductance",
    statement="A circuit's own changing current induces an electromotive force "
              "in that same circuit, directed so as to oppose the change in "
              "current that induced it.",
    form="emf = -L * dI/dt",
    quantities=(Quantity.INDUCTANCE, Quantity.CURRENT_RATE),
    validity="Constant self-inductance; sign follows Lenz's law, which follows "
             "from conservation of energy.",
    fails_when=(
        "the core saturates",
        "mutual coupling to another circuit is not negligible, in which case the "
        "induced emf is not self-induced alone",
    ),
)

MUTUAL_INDUCTANCE = Law(
    name="mutual-inductance",
    statement="A changing current in one circuit induces an electromotive force "
              "in a second circuit through their shared flux.",
    form="emf_2 = -M * dI_1/dt",
    quantities=(Quantity.INDUCTANCE, Quantity.CURRENT_RATE),
    validity="Constant mutual inductance M, with M bounded by the geometric "
             "mean of the two self-inductances.",
    fails_when=(
        "the coupling geometry changes",
        "either core saturates",
    ),
)

KIRCHHOFF_VOLTAGE = Law(
    name="kirchhoff-voltage",
    statement="Around any closed loop, the sum of potential differences is zero, "
              "so the element drops balance the applied source.",
    form="sum of drops = applied",
    quantities=(Quantity.VOLTAGE,),
    validity="Lumped-element approximation, where the loop is small compared "
             "with the signal wavelength and no changing flux threads the loop "
             "other than through the elements named.",
    fails_when=(
        "changing magnetic flux threads the loop itself, so the loop integral of "
        "the electric field is not zero",
        "the circuit is comparable in size to the signal wavelength",
    ),
)

SERIES_RLC = Law(
    name="series-rlc",
    statement="In a series RLC circuit the inductive, resistive, and capacitive "
              "drops sum to the applied voltage, giving a second-order linear "
              "differential equation in the charge.",
    form="L * d2Q/dt2 + R * dQ/dt + (1/C) * Q = V",
    quantities=(
        Quantity.INDUCTANCE, Quantity.CHARGE, Quantity.RESISTANCE,
        Quantity.CAPACITANCE, Quantity.VOLTAGE,
    ),
    validity="Linear, time-invariant, lumped elements. Obtained by applying "
             "Kirchhoff's voltage law to the three constitutive relations.",
    fails_when=(
        "any constituent law fails",
        "an element is nonlinear, so superposition does not hold",
        "component values vary in time",
    ),
)

LAWS: tuple[Law, ...] = (
    OHM, FARADAY_LENZ, CAPACITOR, SELF_INDUCTANCE, MUTUAL_INDUCTANCE,
    KIRCHHOFF_VOLTAGE, SERIES_RLC,
)

LAWS_BY_NAME: dict[str, Law] = {law.name: law for law in LAWS}

#: The three constitutive relations Kirchhoff's voltage law composes into
#: `SERIES_RLC`. A borrower transporting the series form is transporting all
#: four, and inherits every one of their failure modes.
SERIES_RLC_CONSTITUENTS: tuple[Law, ...] = (
    FARADAY_LENZ, OHM, CAPACITOR, KIRCHHOFF_VOLTAGE,
)


# ---------------------------------------------------------------------------
# Parameter independence.
# ---------------------------------------------------------------------------

#: In a series RLC circuit, R, L, and C are INDEPENDENT parameters. An inductor
#: and a capacitor are physically distinct components and either may be varied
#: while the others are held fixed.
#:
#: This is stated explicitly because it is exactly the point at which a borrower
#: may depart. A field that constrains its analogue of C to be a function of its
#: analogue of L has a smaller parameter space than the circuit does, so the
#: transport is not onto: not every circuit corresponds to a state of that field.
#: `hyperphysics.transport.Transport.constrains_parameters` is where a borrower
#: declares such a departure instead of leaving it implicit.
PARAMETERS_ARE_INDEPENDENT: tuple[Quantity, ...] = (
    Quantity.RESISTANCE, Quantity.INDUCTANCE, Quantity.CAPACITANCE,
)


# ---------------------------------------------------------------------------
# Exact consequences of the idealized series RLC model.
# ---------------------------------------------------------------------------


def _require_positive(**values: float) -> None:
    for label, value in values.items():
        if value <= 0:
            raise ValueError(f"{label} must be positive, got {value}")


def resonant_angular_frequency(inductance: float, capacitance: float) -> float:
    """Undamped resonant angular frequency, 1 / sqrt(L * C).

    At this drive frequency the inductive and capacitive reactances cancel and
    only the resistance opposes the drive.
    """
    _require_positive(inductance=inductance, capacitance=capacitance)
    return 1.0 / ((inductance * capacitance) ** 0.5)


def characteristic_impedance(inductance: float, capacitance: float) -> float:
    """Characteristic impedance, sqrt(L / C).

    The scale against which resistance is compared to decide the damping regime.
    """
    _require_positive(inductance=inductance, capacitance=capacitance)
    return (inductance / capacitance) ** 0.5


def damping_ratio(resistance: float, inductance: float, capacitance: float) -> float:
    """Damping ratio of the series RLC circuit, (R/2) * sqrt(C / L).

    Equivalently, half the ratio of resistance to characteristic impedance.
    """
    _require_positive(inductance=inductance, capacitance=capacitance)
    if resistance < 0:
        raise ValueError(f"resistance must not be negative, got {resistance}")
    return (resistance / 2.0) * ((capacitance / inductance) ** 0.5)


def regime(resistance: float, inductance: float, capacitance: float) -> str:
    """Name the damping regime: underdamped, critically damped, or overdamped."""
    ratio = damping_ratio(resistance, inductance, capacitance)
    if ratio < 1.0:
        return "underdamped"
    if ratio == 1.0:
        return "critically-damped"
    return "overdamped"


def reactance(angular_frequency: float, inductance: float, capacitance: float) -> float:
    """Net reactance at a drive frequency, (w * L) - 1 / (w * C).

    Zero exactly at resonance, which is what makes resonance the frequency of
    least total opposition.
    """
    _require_positive(
        angular_frequency=angular_frequency, inductance=inductance, capacitance=capacitance,
    )
    return (angular_frequency * inductance) - 1.0 / (angular_frequency * capacitance)


def impedance_magnitude(
    resistance: float, angular_frequency: float, inductance: float, capacitance: float,
) -> float:
    """Magnitude of the series impedance, sqrt(R^2 + X^2)."""
    if resistance < 0:
        raise ValueError(f"resistance must not be negative, got {resistance}")
    net = reactance(angular_frequency, inductance, capacitance)
    return ((resistance * resistance) + (net * net)) ** 0.5


def dissipated_power(current: float, resistance: float) -> float:
    """Power dissipated in the resistance, I^2 * R.

    The resistance is the only element that dissipates. Inductive and capacitive
    energy is stored and returned over a cycle, which is why this expression
    names no L and no C.
    """
    if resistance < 0:
        raise ValueError(f"resistance must not be negative, got {resistance}")
    return current * current * resistance


def stored_energy(inductance: float, current: float, capacitance: float, charge: float) -> float:
    """Total stored energy, (1/2) L I^2 + Q^2 / (2C).

    Both terms are recoverable, which is the formal counterpart of the claim
    that only resistance dissipates.
    """
    _require_positive(inductance=inductance, capacitance=capacitance)
    magnetic = 0.5 * inductance * current * current
    electric = (charge * charge) / (2.0 * capacitance)
    return magnetic + electric
