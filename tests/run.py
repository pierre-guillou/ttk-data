import argparse
import faulthandler
import json
import multiprocessing
import os
import pathlib
import time

from paraview import simple

faulthandler.enable()


def gen_screenshot(state):
    for i, view in enumerate(simple.GetViews()):
        print(f"Generating view #{i}")
        simple.SaveScreenshot(f"tests/{state.stem}_{i}.png", view)
        print(f"{state}: view #{i} saved")
    simple.ResetSession()


def process_pvsm(state):
    print(f"Loading {state}...")
    print(json.dumps(dict(os.environ), indent=4))
    simple.LoadState(str(state))
    print("Generating screenshot...")
    gen_screenshot(state)
    print("Screenshot generated...")


def process_py(state):
    with open(state, "r") as st:
        # pylint: disable=W0122
        exec(st.read())
    gen_screenshot(state)


def run_one(state_file):
    if not state_file.exists():
        raise FileNotFoundError

    print(f"Processing {state_file.name}")
    start_time = time.time()

    {".pvsm": process_pvsm, ".py": process_py}[state_file.suffix](state_file)

    duration = round(time.time() - start_time, 3)
    print(f"Processed {state_file.name} (took {duration}s)")


def run_all():
    p = pathlib.Path(os.path.realpath(__file__)).parents[1]
    os.chdir(p)
    p = p / "states"
    for gl in ["*.pvsm", "*.py"]:
        for state in sorted(p.glob(gl)):
            # keep instances isolated (fix segfaults)
            proc = multiprocessing.Process(target=run_one, args=(state,))
            proc.start()
            proc.join()


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
