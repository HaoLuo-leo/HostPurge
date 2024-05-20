import subprocess

def run_kneaddata(input_1, input_2, output_dir, db_path, threads):
    cmd = [
        "kneaddata",
        "-i", input_1,
        "-i", input_2,
        "-o", output_dir,
        "-db", db_path,
        "--threads", str(threads)
    ]
    subprocess.run(cmd, check=True)
