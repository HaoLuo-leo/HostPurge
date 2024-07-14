import subprocess
import os

def qc(input_1, input_2, output_1, output_2, threads):

    cmd = [
        "fastp",
        "-i", input_1,
        "-I", input_2,
        "-o", output_1,
        "-O", output_2,
        "-w", str(threads),
    ]
    subprocess.run(cmd, check=True)

