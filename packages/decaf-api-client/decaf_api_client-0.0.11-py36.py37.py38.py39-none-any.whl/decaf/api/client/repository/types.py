__all__ = [
    "AccountId",
    "AccountMngtFeeSchemeId",
    "ActionId",
    "AgentId",
    "AnalyticalTypeId",
    "ArtifactId",
    "AssetClassId",
    "Currency",
    "GUID",
    "InstitutionId",
    "PortfolioId",
    "QuantId",
    "RiskProfileId",
    "StrategyId",
    "Tags",
    "_LaterI",
    "_LaterS",
]

from typing import NewType, Set

#: Defines a type alias for globally unique resource identifiers.
GUID = NewType("GUID", str)

#: Defines a new-type for currency codes.
Currency = NewType("Currency", str)

#: Defines a type alias for standard set of tags.
Tags = Set[str]

#: Defines a new-type for DECAF quant resource identifier.
QuantId = NewType("QuantId", int)

#: Defines a new-type for DECAF artifact resource identifier.
ArtifactId = NewType("ArtifactId", int)

#: Defines a new-type for DECAF action resource identifier.
ActionId = NewType("ActionId", int)

#: Defines a new-type for DECAF account resource identifier.
AccountId = NewType("AccountId", int)

#: Defines a new-type for DECAF agent resource identifier.
AgentId = NewType("AgentId", int)

#: Defines a new-type for DECAF institution resource identifier.
InstitutionId = NewType("InstitutionId", int)

#: Defines a new-type for DECAF strategy resource identifier.
StrategyId = NewType("StrategyId", int)

#: Defines a new-type for DECAF risk profile resource identifier.
RiskProfileId = NewType("RiskProfileId", int)

#: Defines a new-type for DECAF asset class resource identifier.
AssetClassId = NewType("AssetClassId", int)

#: Defines a new-type for DECAF portfolio resource identifier.
PortfolioId = NewType("PortfolioId", int)

#: Defines a new-type for DECAF account management fee scheme resource identifier.
AccountMngtFeeSchemeId = NewType("AccountMngtFeeSchemeId", int)

#: Defines a new-type for DECAF analytical type resource identifier.
AnalyticalTypeId = NewType("AnalyticalTypeId", int)

#: Defines a new-type for DECAF resource identifiers which are yet to be declared (of :py:class:`int` type).
_LaterI = NewType("_LaterI", int)

#: Defines a new-type for DECAF resource identifiers which are yet to be declared (of :py:class:`str` type).
_LaterS = NewType("_LaterS", int)
