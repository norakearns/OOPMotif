#!/usr/bin/env python
"""
Classes and functions for reading, writing, and storing records from FASTQ files.
"""
from __future__ import annotations
from dataclasses import dataclass

import gzip
from gzip import GzipFile
from typing import Iterator
from typing import TextIO
from typing import Union

from pysam import FastxFile

def optional_gzip_open(
    path: str, 
    mode: str = 'wt') -> Union[TextIO, GzipFile]:
    """
    Open a file for writing, gzip if the filename ends with .gz.
    """
    if path.endswith('.gz'):
        return gzip.open(path, mode)
    else:
        return open(path, mode)

def write_fasta_record(
    fout: Union[TextIO, GzipFile],
    rec: FastaRecord,
    line_width: int = 60
) -> None:
    """
    Write a single FastaRecord to an open file handle
    """
    fout.write(f">{rec.header}\n")
    seq = rec.sequence
    for i in range(0, len(seq), line_width):
        fout.write(seq[i:i+line_width] + "\n")


@dataclass
class FastaRecord:
    """
    Holds one FASTA record.
    """
    header: str
    sequence: str

class FastaReader(Iterator[FastaRecord]):
    """
    Iterate over records in a FASTA file via pysam.FastxFile.
    """
    def __init__(self, fasta: FastxFile) -> None:
        self._fasta = fasta

    @classmethod
    def from_filename(cls, fasta_path: str) -> 'FastaReader':
        """
        Open a FastaReader from file path.
        """
        return cls(FastxFile(fasta_path))

    def __iter__(self) -> Iterator[FastaRecord]:
        return self
    
    def __next__(self) -> FastaRecord:
        entry = next(self._fasta)
        return FastaRecord(entry.name, entry.sequence)

    def reset(self) -> None:
        """
        Reset fasta parser back to start of file.
        """
        self._fasta = FastxFile(self._fasta.filename)

class FastaWriter:
    def __init__(self, fout: Union[TextIO, GzipFile]) -> None:
        self._fout = fout
        self._closed = False

    @classmethod
    def from_filename(cls, fpath: str) -> 'FastaWriter':
        """
        Open a FastaWriter from file path.
        """
        fout = optional_gzip_open(fpath, mode='wt')
        return cls(fout)

    def write(self, rec: FastaRecord) -> None:
        """
        Write the FastaRecord to a file
        """
        write_fasta_record(self._fout, rec)

    def close(self) -> None:
        """
        Close the file handle.
        """
        self._fout.close()
        self._closed = True

    @property
    def closed(self) -> bool:
        """
        True once `close()` has been called
        """
        return self._closed


reader = FastaReader.from_filename("/Users/norakearns/Demo_Code/OOPMotif/tests/test_sequences.fasta")
for rec in reader:
    print(rec.header, rec.sequence)
# …then if you need to iterate again:
reader.reset()

# records = [
#     FastaRecord("seq1", "ACGT"*30),
#     FastaRecord("seq2", "GGGGCCCCTTTT")
# ]

# writer = FastaWriter.from_filename("out.fa.gz")
# for rec in records:
#     writer.write(rec)
# writer.close()