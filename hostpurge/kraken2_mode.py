import subprocess

def kraken2(kmer_db, input_1, input_2, threads):
    kraken2_cmd = [
        "kraken2",
        "--db", kmer_db,
        "--paired", input_1, input_2,
        "--threads", str(threads), "--use-names", "--report-zero-counts", 
        "--report", "result.report",
        "--output", "result.output"
    ]
    # Run kraken2
    subprocess.run(kraken2_cmd, check=True)

def extract(input_1, input_2,  filter_1, filter_2, taxid):
    extract_cmd = [
        "extract_kraken_reads.py",
        "-k", "result.output",
        "-r", "result.report",
        "-1", input_1,
        "-2", input_2,
        "-t", str(taxid), "--include-children",
        "--exclude", "--fastq-output",
        "-o", filter_1,
        "-o2", filter_2
    ]

    # Run extract_kraken_reads.py
    subprocess.run(extract_cmd, check=True)
