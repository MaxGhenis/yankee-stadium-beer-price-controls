"""
Yankee Stadium Beer Price Controls Economic Analysis

A comprehensive simulation analyzing the economic impacts of beer price controls
on consumer welfare, stadium revenue, attendance, and alcohol-related externalities.
"""

__version__ = "1.0.0"
__author__ = "Economic Policy Analysis"

from .model import StadiumEconomicModel
from .simulation import BeerPriceControlSimulator

__all__ = ["StadiumEconomicModel", "BeerPriceControlSimulator"]
