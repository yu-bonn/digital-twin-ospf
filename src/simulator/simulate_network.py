import subprocess
import os

def run_simulation(config_files):
    simrouting_path = os.path.join(os.path.dirname(__file__), "simrouting")

    if not os.path.isfile(simrouting_path):
        raise FileNotFoundError(f"simrouting not found at {simrouting_path}")

    # コマンド構築
    cmd = [simrouting_path] + config_files
    print(f"Running: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("=== Simulation Output ===")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("=== Simulation Error ===")
        print(e.stderr)

if __name__ == "__main__":
    # 仮の設定ファイル。必要に応じて置き換えてください。
    test_files = ["sample/test1.txt"]
    run_simulation(test_files)
