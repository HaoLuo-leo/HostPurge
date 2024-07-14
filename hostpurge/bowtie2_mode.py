import subprocess

def bowtie2(reference_genome, input_1, input_2, output_sam, threads=1):
    """
    Run bowtie2 with default options.

    :param reference_genome: Path to the reference genome index prefix.
    :param input_1: Path to the first input fastq file.
    :param input_2: Path to the second input fastq file.
    :param output_sam: Path to the output SAM file.
    :param threads: Number of threads to use (default is 1).
    """
    cmd = [
        "bowtie2",
        "-x", reference_genome,
        "-1", input_1,
        "-2", input_2,
        "-S", output_sam,
        "--threads", str(threads)
    ]
    subprocess.run(cmd, check=True)

def parse_sam(sam_file, filter_1, filter_2):

    with open(sam_file, 'r') as sam, \
         open(filter_1, 'w') as not_aligned1, \
         open(filter_2, 'w') as not_aligned2:

        read_buffer = []

        for line in sam:
            if line.startswith('@'):
                continue

            parts = line.strip().split('\t')
            flag = int(parts[1])
            seq = parts[9]
            qual = parts[10]
            read_id = parts[0]
            is_unmapped = (flag & 4) != 0

            fq_entry = f"@{read_id}\n{seq}\n+\n{qual}\n"

            read_buffer.append((fq_entry, is_unmapped))

            if len(read_buffer) == 2:
                (fq_entry1, is_unmapped1), (fq_entry2, is_unmapped2) = read_buffer
                if is_unmapped1 and is_unmapped2:
                    not_aligned1.write(fq_entry1)
                    not_aligned2.write(fq_entry2)
                else:
                    # Handle mixed cases if necessary
                    pass
                read_buffer = []


