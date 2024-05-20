import subprocess

def run_combined_kraken2_then_kneaddata(input_1, input_2, output_dir, kraken_db, kneaddata_db, threads):
    temp_output = f"{output_dir}/kraken2_temp"
    run_kraken2(input_1, input_2, temp_output, kraken_db, threads)
    # Assuming Kraken2 filtered output is used as input for KneadData
    filtered_1 = f"{temp_output}/filtered_1.fastq"
    filtered_2 = f"{temp_output}/filtered_2.fastq"
    run_kneaddata(filtered_1, filtered_2, output_dir, kneaddata_db, threads)

def run_combined_kneaddata_then_kraken2(input_1, input_2, output_dir, kneaddata_db, kraken_db, threads):
    temp_output = f"{output_dir}/kneaddata_temp"
    run_kneaddata(input_1, input_2, temp_output, kneaddata_db, threads)
    # Assuming KneadData filtered output is used as input for Kraken2
    filtered_1 = f"{temp_output}/filtered_1.fastq"
    filtered_2 = f"{temp_output}/filtered_2.fastq"
    run_kraken2(filtered_1, filtered_2, output_dir, kraken_db, threads)
