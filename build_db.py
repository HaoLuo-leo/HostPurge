import subprocess


def download_taxonomy(db_name, threads):
    """
    Download taxonomy data for Kraken2 database.
    """
    cmd = [
        "kraken2-build",
        "--download-taxonomy",
        "--threads", str(threads),
        "--db", db_name,
        "--use-ftp"
    ]
    subprocess.run(cmd, check=True)


def add_to_library(db_name, fasta_file, threads):
    """
    Add a FASTA file to the Kraken2 library.
    """
    cmd = [
        "kraken2-build",
        "--db", db_name,
        "--threads", str(threads),
        "--add-to-library", fasta_file
    ]
    subprocess.run(cmd, check=True)


def build_kraken2_db(db_name, threads):
    """
    Build the Kraken2 database.
    """
    cmd = [
        "kraken2-build",
        "--build",
        "--db", db_name,
        "--threads", str(threads)
    ]
    subprocess.run(cmd, check=True)


def build_bowtie2_db(reference_genome, output_prefix, seed):
    """
    Build a bowtie2 index from a reference genome.

    :param reference_genome: Path to the reference genome FASTA file.
    :param output_prefix: Prefix for the output index files.
    """
    cmd = [
        "bowtie2-build",
        "-f", reference_genome,
        output_prefix, 
        "--seed", str(seed)
    ]
    subprocess.run(cmd, check=True)
