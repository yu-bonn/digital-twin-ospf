import subprocess
import os

def run_simulation(config_files):
    # 正しい simrouting バイナリの位置
    simrouting_path = os.path.join(
        os.path.dirname(__file__),
        "simrouting", "simrouting"
    )

    if not os.path.isfile(simrouting_path):
        raise FileNotFoundError(f"[ERROR] simrouting not found at {simrouting_path}")

    for f in config_files:
        if not os.path.isfile(f):
            raise FileNotFoundError(f"[ERROR] Input file not found: {f}")

    cmd = [simrouting_path] + config_files
    print(f"[INFO] Running: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("=== Simulation Output ===")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("=== Simulation Error ===")
        print(e.stderr)
        raise

if __name__ == "__main__":
    # 例: config/test1.txt を入力として与える場合
    test_files = [os.path.join("..", "..", "config", "test1.txt")]
    run_simulation(test_files)
