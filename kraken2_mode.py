import subprocess

def run_kraken2(input_1, input_2, output_dir, db_path, threads):
    output_report = f"{output_dir}/kraken2.report"
    output_result = f"{output_dir}/kraken2.output"
    cmd = [
        "kraken2",
        "--db", db_path,
        "-1", input_1,
        "-2", input_2,
        "--threads", str(threads),
        "--report", output_report,
        "--output", output_result
    ]
    subprocess.run(cmd, check=True)
