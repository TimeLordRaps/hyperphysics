"""hyperphysics: physical law as an explicit, citable transport surface.

hypermath takes one operation and derives formal structure. hyperethics takes
one operation and derives normative structure. hyperphysics is the physics
member of the same family, and its first implemented piece is the part adjacent
fields already need: electrical law stated once, with validity conditions and
failure modes attached, plus the interface a borrowing field must satisfy.

The field's own ground is not written. Nothing in this package claims to be
hyperphysics' L0, and `electrical.hm` says so in its header rather than quietly
taking a layer index it has not earned.
"""

from hyperphysics.electrical import (
    CAPACITOR,
    FARADAY_LENZ,
    KIRCHHOFF_VOLTAGE,
    LAWS,
    LAWS_BY_NAME,
    MUTUAL_INDUCTANCE,
    OHM,
    PARAMETERS_ARE_INDEPENDENT,
    QUANTITIES,
    QUANTITY_INFO,
    SELF_INDUCTANCE,
    SERIES_RLC,
    SERIES_RLC_CONSTITUENTS,
    Law,
    Quantity,
    QuantityInfo,
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

__all__ = [
    "CAPACITOR",
    "FARADAY_LENZ",
    "KIRCHHOFF_VOLTAGE",
    "LAWS",
    "LAWS_BY_NAME",
    "MUTUAL_INDUCTANCE",
    "OHM",
    "PARAMETERS_ARE_INDEPENDENT",
    "QUANTITIES",
    "QUANTITY_INFO",
    "SELF_INDUCTANCE",
    "SERIES_RLC",
    "SERIES_RLC_CONSTITUENTS",
    "UNITS_DO_NOT_TRANSPORT",
    "Law",
    "Quantity",
    "QuantityInfo",
    "Transport",
    "UndeclaredTransport",
    "UnknownLaw",
    "Warrant",
    "audit",
    "characteristic_impedance",
    "cited_law",
    "damping_ratio",
    "derivative_chain",
    "derivative_order",
    "dissipated_power",
    "impedance_magnitude",
    "inherited_failure_modes",
    "reactance",
    "regime",
    "resonant_angular_frequency",
    "stored_energy",
    "validate",
]

__version__ = "0.1.0.dev0"
