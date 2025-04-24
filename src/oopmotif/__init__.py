# src/oopmotif/__init__.py

"""
oopmotif
~~~~~~~~

A small package to visualize motif locations on gene sequences.
"""

__version__ = "0.1.0"

# Expose the public API at the package level
from .motif_mark import (
    main,
    get_args,
    parse_fasta,
    read_motifs,
    expand_motif,
    Sequence,
    Plot,
)

__all__ = [
    "main",
    "get_args",
    "parse_fasta",
    "read_motifs",
    "expand_motif",
    "Sequence",
    "Plot",
]