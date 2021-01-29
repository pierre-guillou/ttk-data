import multiprocessing
import pathlib

from paraview import simple


def gen_screenshot(state):
    print(f"Processing {state}")
    for i, view in enumerate(simple.GetViews()):
        simple.SaveScreenshot(f"{state}_{i}.png", view)
        print(f"{state}: view #{i} saved")
    simple.ResetSession()


def process_psvm(state):
    simple.LoadState(str(state))
    gen_screenshot(state)


def process_py(state):
    with open(state, "r") as st:
        exec(st.read())
    gen_screenshot(state)


def main():
    p = pathlib.Path(".") / "states"
    patterns = {"*.pvsm": process_psvm, "*.py": process_py}
    for k, v in patterns.items():
        for state in sorted(p.glob(k)):
            # keep instances isolated (fix segfaults)
            proc = multiprocessing.Process(target=v, args=(state,))
            proc.start()
            proc.join()


if __name__ == "__main__":
    main()
