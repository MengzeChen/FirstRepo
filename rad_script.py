import argparse
import pyfaidx
import vcf
from Bio.Restriction.Restriction_Dictionary import rest_dict

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Perform RAD sequencing simulations on a given genome.")
    parser.add_argument("GenomeFile", type=str, help="Path to the FASTA file containing the genome")
    parser.add_argument("VCFFile", type=str, help="Path to the VCF file containing DNA polymorphisms")
    parser.add_argument("Mode", choices=["SingleRad", "ddRad"], help="Specify whether to run SingleRad or ddRad")
    parser.add_argument("RE1", type=str, help="Name of the first restriction enzyme")
    parser.add_argument("--RE2", type=str, help="Name of the second restriction enzyme (only for ddRad mode)")
    return parser.parse_args()

def read_fasta(path_to_fasta: str, chromosome: str) -> str:
    genome = pyfaidx.Fasta(path_to_fasta)
    try:
        return str(genome[chromosome])
    except KeyError:
        raise ValueError(f"Chromosome {chromosome} not found in FASTA file.")

def find_motifs(dna: str, motif: str) -> list[int]:
    positions = []
    start = 0
    while True:
        idx = dna.find(motif, start)
        if idx == -1:
            break
        positions.append(idx)
        start = idx + len(motif)
    return positions

def run_single_rad(dna: str, re1: str) -> list[tuple[int, int]]:
    assert re1 in rest_dict, f"Restriction enzyme {re1} not found in rest_dict."
    motif = rest_dict[re1]['site']
    cut_sites = find_motifs(dna, motif)
    seq_length = 100
    return [(pos, pos + seq_length) for pos in cut_sites]

def run_ddrad(dna: str, re1: str, re2: str) -> list[tuple[int, int]]:
    assert re1 in rest_dict and re2 in rest_dict, "One or both restriction enzymes not found in rest_dict."
    motif1 = rest_dict[re1]['site']
    motif2 = rest_dict[re2]['site']
    re1_sites = find_motifs(dna, motif1)
    re2_sites = find_motifs(dna, motif2)
    
    min_size, max_size, seq_length = 300, 700, 100
    sequenced_sites = []
    for r1 in re1_sites:
        for r2 in re2_sites:
            if min_size <= abs(r2 - r1) <= max_size and r2 > r1:
                sequenced_sites.append((r1, r1 + seq_length))
                sequenced_sites.append((r2, r2 + seq_length))
    return sequenced_sites

def find_variable_sites(vcf_file_path: str, sequenced_sites: list[tuple[int, int]]):
    vcf_reader = vcf.Reader(open(vcf_file_path, 'r'))
    variable_sites = []
    for record in vcf_reader:
        if any(start <= record.POS <= end for start, end in sequenced_sites):
            variable_sites.append((record.POS, record.REF, record.ALT))
    return variable_sites

def main():
    args = parse_arguments()
    target_chromosome = 'NC_036780.1'
    dna_seq = read_fasta(args.GenomeFile, target_chromosome)
    
    if args.Mode == "SingleRad":
        seq_sites = run_single_rad(dna_seq, args.RE1)
    else:
        seq_sites = run_ddrad(dna_seq, args.RE1, args.RE2)
    
    variable_sites = find_variable_sites(args.VCFFile, seq_sites)
    print(f"Total sequencing sites found: {len(seq_sites)}")
    print(f"Variable sites found: {len(variable_sites)}")
    
if __name__ == "__main__":
    main()