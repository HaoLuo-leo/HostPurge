import subprocess

def bowtie2(bowtie2_db, input_1, input_2, output_sam, threads=1):
    
    cmd = [
        "bowtie2",
        "-x", bowtie2_db,
        "-1", input_1,
        "-2", input_2,
        "-S", output_sam,
        "--threads", str(threads)
    ]
    subprocess.run(cmd, check=True)
