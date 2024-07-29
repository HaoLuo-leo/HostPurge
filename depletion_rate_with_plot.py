import gzip
import argparse
import os
import matplotlib.pyplot as plt

def count_reads(file_path):
    """Count the number of reads in a FASTQ file."""
    count = 0
    is_gzipped = file_path.endswith('.gz')
    open_func = gzip.open if is_gzipped else open

    with open_func(file_path, 'rt') as file:
        for line in file:
            if line.startswith('@'):
                count += 1
    return count

def extract_sample_name(file_path):
    """Extract sample name from the file path."""
    return os.path.basename(file_path).split('_')[0]

def calculate_host_depletion_rate(original_files, filtered_files):
    """Calculate host depletion rate and generate TSV output."""
    original_reads = sum(count_reads(file) for file in original_files)
    filtered_reads = sum(count_reads(file) for file in filtered_files)

    removed_reads = original_reads - filtered_reads
    removal_rate = (removed_reads / original_reads) * 100

    sample_name = extract_sample_name(original_files[0])

    print(f"Original reads: {original_reads}")
    print(f"Filtered reads: {filtered_reads}")
    print(f"Removed reads: {removed_reads}")
    print(f"Host depletion rate: {removal_rate:.2f}%")

    return sample_name, original_reads, filtered_reads, removal_rate

def plot_depletion_rate(sample_name, original_reads, filtered_reads, output_path):
    """Plot the original and filtered reads as a bar chart."""
    labels = ['Original Reads', 'Filtered Reads']
    counts = [original_reads, filtered_reads]

    plt.bar(labels, counts, color=['blue', 'green'])
    plt.title(f'Reads Before and After Filtering for {sample_name}')
    plt.xlabel('Reads Type')
    plt.ylabel('Number of Reads')
    plt.savefig(output_path)
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate host depletion rate for paired-end reads and output as TSV.")
    parser.add_argument('-i1', '--input1', required=True, help="Path to the original reads FASTQ file for read 1 (can be .gz)")
    parser.add_argument('-i2', '--input2', required=True, help="Path to the original reads FASTQ file for read 2 (can be .gz)")
    parser.add_argument('-f1', '--filtered1', required=True, help="Path to the filtered reads FASTQ file for read 1 (can be .gz)")
    parser.add_argument('-f2', '--filtered2', required=True, help="Path to the filtered reads FASTQ file for read 2 (can be .gz)")
    parser.add_argument('-t', '--tsv', required=True, help="Output path for the TSV file.")
    parser.add_argument('-p', '--plot', required=True, help="Output path for the bar plot image.")

    args = parser.parse_args()
    original_files = [args.input1, args.input2]
    filtered_files = [args.filtered1, args.filtered2]
    tsv_path = args.tsv
    plot_path = args.plot

    for file in original_files + filtered_files:
        if not os.path.exists(file):
            print(f"Error: File '{file}' does not exist.")
            exit(1)

    sample_name, original_reads, filtered_reads, removal_rate = calculate_host_depletion_rate(original_files, filtered_files)

    with open(tsv_path, 'w') as tsv_file:
        tsv_file.write("Sample\tOriginal_Reads\tFiltered_Reads\tRemoved_Reads\tHost_Depletion_Rate(%)\n")
        tsv_file.write(f"{sample_name}\t{original_reads}\t{filtered_reads}\t{original_reads - filtered_reads}\t{removal_rate:.2f}\n")

    plot_depletion_rate(sample_name, original_reads, filtered_reads, plot_path)

    print(f"Results saved to {tsv_path}")
    print(f"Plot saved to {plot_path}")
