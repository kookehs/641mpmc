import subprocess

if __name__ ==  "__main__":
    subprocess.call(["sh", "./shortcut-solver.sh", "-c width=7 level*.lp"])
    subprocess.call(["python", "./p7_visualize.py", "example_noshortcut.json"])
