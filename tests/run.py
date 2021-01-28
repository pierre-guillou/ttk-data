import multiprocessing
import pathlib

from paraview import simple


def gen_screenshot(state):
    print(f"Processing {state}")
    simple.LoadState(str(state))
    for i, view in enumerate(simple.GetViews()):
        simple.SaveScreenshot(f"{state}_{i}.png", view)
        print(f"{state}: view #{i} saved")
    simple.ResetSession()


def main():
    p = pathlib.Path(".") / "states"
    for state in sorted(p.glob("*.pvsm")):
        # keep instances isolated (fix segfaults)
        p = multiprocessing.Process(target=gen_screenshot, args=(state,))
        p.start()
        p.join()


if __name__ == "__main__":
    main()
