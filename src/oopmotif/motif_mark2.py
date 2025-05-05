#!/usr/bin/env python
import itertools
import re
import cairo
import argparse
import logging

from Fasta import FastaReader

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
        self.exons = self.find_exons()
        self.length = len(self.sequence) 
    
    def find_exons(self) -> list[tuple[int,int]]:
        """
        Identify the start and end coordinates of exonic (uppercase) regions.
        
        Inputs:
        -------
        motif: str

        Outputs:
        --------
        matches: list[tuples]
            list of tuples representing start and end of exonic regions
        
        """
        matches = []
        for m in re.finditer(r"[A-Z]+", self.sequence):
            matches.append((m.start(), m.end()))
        return matches

class Plot():
        


def main():
    args = get_args()
    reader = FastaReader.from_filename(args.f)
    for rec in reader:
        print(rec.header, rec.sequence)

if __name__ == "__main__":
    main()

