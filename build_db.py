import os
import subprocess


def build_kraken2_db(db_dir, threads):
    os.makedirs(db_dir, exist_ok=True)
    cmd = [
        'kraken2-build', '--download-taxonomy', '--db', db_dir, '--threads', str(threads)
    ]
    subprocess.run(cmd, check=True)

    # Add any specific genome sequences to the library
    # Example: subprocess.run(['kraken2-build', '--db', db_dir, '--add-to-library', 'genome.fasta'], check=True)

    cmd = [
        'kraken2-build', '--build', '--db', db_dir, '--threads', str(threads)
    ]
    subprocess.run(cmd, check=True)


def build_kneaddata_db(db_dir, input_fasta, threads):
    os.makedirs(db_dir, exist_ok=True)
    cmd = [
        'kneaddata_database', '--download', 'human_genome', 'bowtie2', db_dir
    ]
    subprocess.run(cmd, check=True)

    cmd = [
        'bowtie2-build', input_fasta, os.path.join(db_dir, 'kneaddata_db'), '--threads', str(threads)
    ]
    subprocess.run(cmd, check=True)
