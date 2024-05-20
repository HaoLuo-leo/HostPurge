import argparse
from hostpurge.kneaddata_mode import run_kneaddata
from hostpurge.kraken2_mode import run_kraken2
from hostpurge.combined_mode import run_combined_kraken2_then_kneaddata, run_combined_kneaddata_then_kraken2
from hostpurge.build_db import build_kraken2_db, build_kneaddata_db

def main():
    parser = argparse.ArgumentParser(
        description="HostPurge: Host contamination removal tool",
        epilog="""
        Example usage:
            hostpurge run input_1.fastq input_2.fastq output_dir --mode a --kneaddata_db path_to_kneaddata_db --threads 8
            hostpurge build-db --db-type kraken2 --db-dir path_to_kraken_db --threads 8
            hostpurge build-db --db-type kneaddata --db-dir path_to_kneaddata_db --input-fasta genome.fasta --threads 8
        """
    )

    subparsers = parser.add_subparsers(dest='command')

    # Subparser for the "run" command
    run_parser = subparsers.add_parser('run', help='Run HostPurge with specified mode')
    run_parser.add_argument("input_1", help="Input read file 1 (FASTQ format)")
    run_parser.add_argument("input_2", help="Input read file 2 (FASTQ format)")
    run_parser.add_argument("output_dir", help="Output directory where results will be saved")
    run_parser.add_argument("--mode", choices=['a', 'b', 'c', 'd'], required=True, help="Mode of operation: a, b, c, or d")
    run_parser.add_argument("--kraken_db", help="Path to the Kraken2 database")
    run_parser.add_argument("--kneaddata_db", help="Path to the KneadData database")
    run_parser.add_argument("--threads", type=int, default=1, help="Number of threads to use (default: 1)")

    # Subparser for the "build-db" command
    build_db_parser = subparsers.add_parser('build-db', help='Build database for Kraken2 or Kneaddata')
    build_db_parser.add_argument("--db-type", choices=['kraken2', 'kneaddata'], required=True, help="Type of database to build: kraken2 or kneaddata")
    build_db_parser.add_argument("--db-dir", required=True, help="Directory to store the database")
    build_db_parser.add_argument("--input-fasta", help="Input genome FASTA file (required for kneaddata)")
    build_db_parser.add_argument("--threads", type=int, default=1, help="Number of threads to use (default: 1)")

    args = parser.parse_args()

    if args.command == 'run':
        if args.mode == 'a':
            if not args.kneaddata_db:
                run_parser.error("Mode a requires --kneaddata_db")
            run_kneaddata(args.input_1, args.input_2, args.output_dir, args.kneaddata_db, args.threads)

        elif args.mode == 'b':
            if not args.kraken_db:
                run_parser.error("Mode b requires --kraken_db")
            run_kraken2(args.input_1, args.input_2, args.output_dir, args.kraken_db, args.threads)

        elif args.mode == 'c':
            if not args.kraken_db or not args.kneaddata_db:
                run_parser.error("Mode c requires --kraken_db and --kneaddata_db")
            run_combined_kraken2_then_kneaddata(args.input_1, args.input_2, args.output_dir, args.kraken_db, args.kneaddata_db, args.threads)

        elif args.mode == 'd':
            if not args.kneaddata_db or not args.kraken_db:
                run_parser.error("Mode d requires --kneaddata_db and --kraken_db")
            run_combined_kneaddata_then_kraken2(args.input_1, args.input_2, args.output_dir, args.kneaddata_db, args.kraken_db, args.threads)

    elif args.command == 'build-db':
        if args.db_type == 'kraken2':
            build_kraken2_db(args.db_dir, args.threads)
        elif args.db_type == 'kneaddata':
            if not args.input_fasta:
                build_db_parser.error("Building Kneaddata database requires --input-fasta")
            build_kneaddata_db(args.db_dir, args.input_fasta, args.threads)

if __name__ == "__main__":
    main()
