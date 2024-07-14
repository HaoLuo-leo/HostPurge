import argparse
import os
from .bowtie2_mode import bowtie2, parse_sam
from .kraken2_mode import kraken2, extract
from .fastp import qc
from .build_db import download_taxonomy, add_to_library, build_kraken2_db, build_bowtie2_db

def main():
    parser = argparse.ArgumentParser(
        prog="hostpurge",
        usage="%(prog)s [options] ..."
    )

    subparsers = parser.add_subparsers(dest='command')

    # Subparser for the "run" command
    run_parser = subparsers.add_parser('run', help='Run HostPurge with specified mode')
    run_parser.add_argument("--mode", choices=['a', 'b', 'c', 'd'], default='c', help="Mode of operation: a, b, c, or d")
    run_parser.add_argument("--bowtie2_db", dest="bowtie2_db", help="Path to the bowtie2 database")
    run_parser.add_argument("--kmer_db", dest="kmer_db", help="Path to the kmer database")
    run_parser.add_argument("-i1", dest="input_1", help="Input read file 1 (FASTQ format)")
    run_parser.add_argument("-i2", dest="input_2", help="Input read file 2 (FASTQ format)")
    run_parser.add_argument("-o1", dest="filter_1", help="output read file 2 (FASTQ format)")
    run_parser.add_argument("-o2", dest="filter_2", help="output read file 2 (FASTQ format)")
    run_parser.add_argument("--taxid", dest="taxid", help="Taxonomy ID[s] of reads to extract (space-delimited)")
    run_parser.add_argument("-t", dest="threads", type=int, default=1, help="Number of threads to use (default: 1)")

    # Subparser for the "build-db" command
    build_db_parser = subparsers.add_parser('build-db', help='Build database for Kraken2 or bowtie2')
    build_db_parser.add_argument("--db-type", choices=['kraken2', 'bowtie2'], help="Type of database to build: kraken2 or bowtie2")
    build_db_parser.add_argument("-t", dest="threads", type=int, default=1, help="Number of threads to use (default: 1)")
    build_db_parser.add_argument("--db-name", dest="db_name", help="DB name")
    build_db_parser.add_argument("--add-to-library", dest="fasta_file", help="Add FILE to library")
    build_db_parser.add_argument("--input-fasta", dest="reference_genome", help="Input reference genome FASTA file (required for bowtie2)")
    build_db_parser.add_argument("-o", dest="output_prefix", help="Prefix for the output index files(required for bowtie2)")
    build_db_parser.add_argument("-s", dest="seed", help="seed for random number generator(required for bowtie2)")

    # Subparser for the "qc" command
    qc_parser = subparsers.add_parser('qc', help='Run qc on input files')
    qc_parser.add_argument("-i1", dest="input_1", help="Input read file 1 (FASTQ format)")
    qc_parser.add_argument("-i2", dest="input_2", help="Input read file 2 (FASTQ format)")
    qc_parser.add_argument("-o1", dest="output_1", help="Output read file 1 (FASTQ format)")
    qc_parser.add_argument("-o2", dest="output_2", help="Output read file 2 (FASTQ format)")
    qc_parser.add_argument("-t", dest="threads", type=int, default=1, help="Number of threads to use (default: 1)")


    args = parser.parse_args()

    if args.command == 'run':
        if args.mode == 'a':
            if not args.bowtie2_db:
                run_parser.error("Mode a requires --bowtie2_db")
            output_sam = "output.sam"
            bowtie2(args.bowtie2_db, args.input_1, args.input_2, output_sam, args.threads)
            parse_sam(output_sam, args.filter_1, args.filter_2)
            os.remove("output.sam")
        elif args.mode == 'b':
            if not args.kmer_db:
                run_parser.error("Mode b requires --kmer_db")
            kraken2(args.kmer_db, args.input_1, args.input_2, args.threads)
            extract(args.input_1, args.input_2, args.filter_1, args.filter_2, args.taxid)
            os.remove("result.report")
            os.remove("result.output")
        elif args.mode == 'c':
            kraken2(args.kmer_db, args.input_1, args.input_2, args.threads)
            filter_1 = "temp1.fq"
            filter_2 = "temp2.fq"
            extract(args.input_1, args.input_2, filter_1, filter_2, args.taxid)
            filtered_input_1 = filter_1
            filtered_input_2 = filter_2
            output_sam = "output.sam"
            bowtie2(args.bowtie2_db, filtered_input_1, filtered_input_2, output_sam, args.threads)
            parse_sam(output_sam, args.filter_1, args.filter_2)
            os.remove("temp1.fq")
            os.remove("temp2.fq")
            os.remove("output.sam")
        elif args.mode == 'd':
            output_sam = "output.sam"
            bowtie2(args.bowtie2_db, args.input_1, args.input_2, output_sam, args.threads)
            filter_1 = "temp1.fq"
            filter_2 = "temp2.fq"
            parse_sam(output_sam, filter_1, filter_2)
            filtered_input_1 = filter_1
            filtered_input_2 = filter_2
            kraken2(args.kmer_db, filtered_input_1, filtered_input_2, args.threads)
            extract(filtered_input_1, filtered_input_2, args.filter_1, args.filter_2, args.taxid)
            os.remove("temp1.fq")
            os.remove("temp2.fq")
            os.remove("output.sam")

    elif args.command == 'build-db':
        if args.db_type == 'kraken2':
            download_taxonomy(args.db_name, args.threads)
            # Additional command to add FASTA file to the Kraken2 library if provided
            add_to_library(args.db_name, args.fasta_file, args.threads)
            build_kraken2_db(args.db_name, args.threads)
        elif args.db_type == 'bowtie2':
            build_bowtie2_db(args.reference_genome, args.output_prefix, args.seed)

    elif args.command == 'qc':
        qc(args.input_1, args.input_2, args.output_1, args.output_2, args.threads)


if __name__ == "__main__":
    main()
