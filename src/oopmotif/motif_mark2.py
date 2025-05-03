#!/usr/bin/env python
import itertools
import re
import cairo
import argparse
import logging

logging.basicConfig(level=logging.INFO)

IUPAC_dict = {
    'A': ['A'], 'C': ['C'], 'G': ['G'], 'T': ['T'], 'U': ['U'], 'W': ['A', 'T'], 'S': ['G', 'C'], 
    'M': ['A', 'C'], 'K': ['G', 'T'], 'R': ['A', 'G'], 'Y': ['C', 'T'], 'B': ['C', 'G', 'T'], 'D': ['A', 'G', 'T'], 'H': ['A', 'C', 'T'], 'V': ['A', 'C', 'G'], 'N': ['A', 'C', 'T', 'G']
}

def get_args():
    parser = argparse.ArgumentParser(description="Visualize motifs on gene sequences")
    parser.add_argument("-f", required=True, help="FASTA file with sequences")
    parser.add_argument("-m", required=True, help="Motifs file")
    return parser.parse_args()

def parse_fasta(filepath):
    sequences = []
    names = []
    with open(filepath, 'r') as f:
        seq = ''
        for line in f:
            if line.startswith(">"):
                if seq:
                    sequences.append(seq)
                    seq = ''
                names.append(line[1:].strip())
            else:
                seq += line.strip()
        if seq:
            sequences.append(seq)
    return names, sequences

class Motif:
    def __init__(self, motif):
        self.motif = motif
        self.length = len(motif)
        self.options = self.expand_motif()

    def return_motif(self) -> str:
        return self.motif
    
    def expand_motif(self) -> list:
        """
        Expand a single ambiguous motif into all possible IUPAC-resolved variants.
        
        Inputs:
        -----------
        motif: str

        Outputs:
        --------
        options: list
            List of all possible iterations of the motif
        """
        try:
            chars = [IUPAC_dict[c] for c in self.motif.upper()]
        except KeyError as e:
            raise ValueError(f"Invalid IUPAC code: {e}")
        return [''.join(p) for p in itertools.product(*chars)]


class Sequence:
    def __init__(self, header, sequence):
        self.sequence = sequence
        self.location = self.get_location(header)

    def get_location(self,header):
        """
        Gets gene coordinates from header line of fasta file

        Inputs:
        ------
        header: str

        Outputs:
        -------
        loc: str
            genomic coordinates (start and end):
        """
        loc = header.split('')[1]
        return loc
    
    def find_exons(self):
        """Identify the start and end coordinates of exonic (uppercase) regions."""
        match = re.search(r'[A-Z]+', self.sequence)
        if not match:
            return (0,0)
        return (match.start(), match.end())
    



