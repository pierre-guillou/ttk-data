import argparse
import multiprocessing
import os
import pathlib
import time

from paraview import simple


def gen_screenshot(state):
    for i, view in enumerate(simple.GetViews()):
        simple.SaveScreenshot(f"tests/{state.stem}_{i}.png", view)
        print(f"{state}: view #{i} saved")
    simple.ResetSession()


def process_pvsm(state):
    simple.LoadState(str(state))
    gen_screenshot(state)


def process_py(state):
    with open(state, "r") as st:
        exec(st.read())
    gen_screenshot(state)


def run_all():
    p = pathlib.Path(os.path.realpath(__file__)).parents[1]
    os.chdir(p)
    p = p / "states"
    patterns = {"*.pvsm": process_pvsm, "*.py": process_py}
    for k, v in patterns.items():
        for state in sorted(p.glob(k)):
            print(f"Processing {state.name}")
            start_time = time.time()

            # keep instances isolated (fix segfaults)
            proc = multiprocessing.Process(target=v, args=(state,))
            proc.start()
            proc.join()

            duration = time.time() - start_time
            print(f"Processed {state.name} (took {duration:.2f}s)")


def run_one(state_file):
    if not state_file.exists():
        raise FileNotFoundError

    patterns = {".pvsm": process_pvsm, ".py": process_py}
    patterns[state_file.suffix](state_file)


def main():
    parser = argparse.ArgumentParser(
        description="Run either one or all state files, generate a screenshot per view"
    )
    parser.add_argument(
        "-i", "--input_state", type=pathlib.Path, help="State file to process"
    )
    args = parser.parse_args()

    if args.input_state:
        run_one(args.input_state)
    else:
        run_all()


if __name__ == "__main__":
    main()
