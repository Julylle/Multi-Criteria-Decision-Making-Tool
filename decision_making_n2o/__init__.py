"""
decision_making_n2o
===================

A multi-criteria decision-making tool for evaluating liquid-based and 
gas-based N2O monitoring systems.

This package provides:

- Quotes: Quantitative cost scoring (equipment & consumables)
- QualitativeScores: Qualitative scoring (commissioning, maintenance, complexity)
- A full TOPSIS-based evaluation workflow


"""

# Package version
__version__ = "1.0.0"

# Public API exports
from .quotes import Quotes
from .qualitative_scores import QualitativeScores

__all__ = [
    "Quotes",
    "QualitativeScores",
    "__version__",
]
