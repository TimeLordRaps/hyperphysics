"""The interface a field must satisfy to borrow an electrical law.

Borrowing the algebraic shape of a physical law to structure a non-physical
domain is a cross-domain inference. It is not automatically illegitimate and it
is not automatically sound. What makes it checkable is that the borrower state,
at the point of borrowing:

1. which law, by name, so the claim has a fixed referent;
2. what form the law takes in the target field;
3. what the borrowing is supposed to transport;
4. what it does NOT transport, concretely enough to name a unit or a mechanism;
5. whether the target field constrains parameters the source leaves free.

Point 5 is the one that is usually missed. A field whose analogue of capacitance
is determined by its analogue of inductance has fewer degrees of freedom than
the circuit does. That is a real structural difference and it must be declared,
not discovered later by a reader who assumed the parameter spaces matched.

Units never transport. `validate` enforces that the disclaimer says so in terms
of the cited law's own quantities rather than in general assurances.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from hyperphysics.electrical import (
    LAWS_BY_NAME,
    PARAMETERS_ARE_INDEPENDENT,
    QUANTITY_INFO,
    SERIES_RLC_CONSTITUENTS,
    Law,
    Quantity,
)


class UnknownLaw(LookupError):
    """Raised when a transport cites a law this package does not state."""


class UndeclaredTransport(ValueError):
    """Raised when a transport omits a declaration the interface requires."""


class Warrant(str, Enum):
    """What kind of claim the borrower is making about the transport."""

    #: The algebraic shape is reused and nothing else is claimed. The weakest
    #: and most honest warrant, and the correct one for an analogy.
    BORROWED_FORM = "BORROWED_FORM"

    #: The target quantities are argued to share the source's dimensional
    #: structure, so the transported relation is claimed to be more than shape.
    DIMENSIONAL = "DIMENSIONAL"

    #: The target relation is derived independently and agrees with the source.
    #: This warrant needs the derivation, not the agreement.
    DERIVED = "DERIVED"


#: Standing rule. No transport may carry an SI unit into a target field, because
#: the unit belongs to the measurement procedure, not to the algebra.
UNITS_DO_NOT_TRANSPORT = (
    "SI units attach to the physical quantity and its measurement procedure. "
    "They do not attach to the algebraic form, so no transport carries them."
)


@dataclass(frozen=True, slots=True)
class Transport:
    """One field's declared borrowing of one named electrical law."""

    law: str
    target_field: str
    target_form: str
    transports: str
    does_not_transport: str
    warrant: Warrant
    #: Source parameters the target field does NOT leave independent. Empty when
    #: the target's parameter space matches the circuit's.
    constrains_parameters: tuple[Quantity, ...] = ()
    #: Required whenever `constrains_parameters` is nonempty.
    constraint_reason: str = ""
    notes: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        for value, label in (
            (self.law, "law"), (self.target_field, "target_field"),
            (self.target_form, "target_form"), (self.transports, "transports"),
            (self.does_not_transport, "does_not_transport"),
        ):
            if type(value) is not str or not value.strip():
                raise UndeclaredTransport(f"transport {label} must be a nonempty string")
        if type(self.warrant) is not Warrant:
            raise TypeError("warrant must be a Warrant member")
        if type(self.constrains_parameters) is not tuple:
            raise TypeError("constrains_parameters must be a tuple")
        for quantity in self.constrains_parameters:
            if type(quantity) is not Quantity:
                raise TypeError("constrains_parameters must hold Quantity members")
            if quantity not in PARAMETERS_ARE_INDEPENDENT:
                raise UndeclaredTransport(
                    f"{quantity.value} is not one of the circuit's free parameters, "
                    "so constraining it is not a departure from the source"
                )
        if self.constrains_parameters and not self.constraint_reason.strip():
            raise UndeclaredTransport(
                "a transport that constrains a free source parameter must say why"
            )


def cited_law(transport: Transport) -> Law:
    """The law a transport cites, or `UnknownLaw` if this package lacks it."""
    try:
        return LAWS_BY_NAME[transport.law]
    except KeyError:
        raise UnknownLaw(
            f"{transport.target_field} cites '{transport.law}', which hyperphysics "
            f"does not state. Known laws: {', '.join(sorted(LAWS_BY_NAME))}"
        ) from None


def inherited_failure_modes(transport: Transport) -> tuple[str, ...]:
    """Every failure mode the transported form inherits from its source.

    A transport of the series form inherits the failure modes of the three
    constitutive relations and of Kirchhoff's voltage law as well, because the
    series form is their composition.
    """
    law = cited_law(transport)
    modes: list[str] = list(law.fails_when)
    if law.name == "series-rlc":
        for constituent in SERIES_RLC_CONSTITUENTS:
            for mode in constituent.fails_when:
                if mode not in modes:
                    modes.append(mode)
    return tuple(modes)


def _disclaimed_units(transport: Transport) -> tuple[str, ...]:
    """SI units of the cited law's quantities that the disclaimer names."""
    law = cited_law(transport)
    text = transport.does_not_transport.lower()
    found: list[str] = []
    for quantity in law.quantities:
        unit = QUANTITY_INFO[quantity].si_unit
        stem = unit.split()[0].rstrip("s")
        if stem in text and unit not in found:
            found.append(unit)
    return tuple(found)


def validate(transport: Transport) -> Transport:
    """Check a transport against the interface, returning it unchanged.

    Raises `UnknownLaw` if the cited law is not stated here, and
    `UndeclaredTransport` if the disclaimer fails to name a unit or mechanism of
    the cited law. Validation checks that the declaration was MADE and is about
    the law it claims to be about. It does not check that the transport is sound,
    and no function in this package can.
    """
    law = cited_law(transport)
    if not _disclaimed_units(transport):
        mechanism_words = ("mechanism", "physical", "material", "field", "flux", "empirical")
        if not any(word in transport.does_not_transport.lower() for word in mechanism_words):
            raise UndeclaredTransport(
                f"{transport.target_field}'s transport of '{law.name}' must disclaim "
                f"a unit or a mechanism of that law. Its quantities carry the units: "
                f"{', '.join(QUANTITY_INFO[q].si_unit for q in law.quantities)}."
            )
    return transport


def audit(transports: tuple[Transport, ...]) -> tuple[str, ...]:
    """Lines describing what a set of transports borrowed and what it disclaimed.

    Intended for a borrowing field's own report, so that the borrowing is
    published rather than buried in a docstring.
    """
    lines: list[str] = [UNITS_DO_NOT_TRANSPORT, ""]
    for transport in transports:
        law = cited_law(transport)
        validate(transport)
        lines.append(f"{transport.target_field} <- {law.name} [{transport.warrant.value}]")
        lines.append(f"  source form:  {law.form}")
        lines.append(f"  target form:  {transport.target_form}")
        lines.append(f"  transports:   {transport.transports}")
        lines.append(f"  disclaims:    {transport.does_not_transport}")
        if transport.constrains_parameters:
            constrained = ", ".join(q.value for q in transport.constrains_parameters)
            lines.append(f"  CONSTRAINS:   {constrained} -- {transport.constraint_reason}")
        lines.append(f"  inherits {len(inherited_failure_modes(transport))} failure modes")
        lines.append("")
    return tuple(lines)
