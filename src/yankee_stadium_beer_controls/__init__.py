"""Public package interface for the Yankee Stadium beer pricing model."""

__version__ = "0.1.0"

from .model import ConsumerType, StadiumEconomicModel
from .paper import build_paper_artifacts, compute_report_context
from .simulation import BeerPriceControlSimulator

__all__ = [
    "BeerPriceControlSimulator",
    "ConsumerType",
    "StadiumEconomicModel",
    "build_paper_artifacts",
    "compute_report_context",
]
