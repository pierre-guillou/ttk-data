import argparse

import cv2
import numpy as np


def main(f0, f1):
    # load the two input images
    im0 = cv2.imread(f0)
    im1 = cv2.imread(f1)
    # convert the images to grayscale
    gray0 = cv2.cvtColor(im0, cv2.COLOR_BGR2GRAY)
    gray1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
    # make sure the two images have the same dimensions
    assert gray0.shape == gray1.shape
    # compute the Mean Square Error between the two images
    err = np.sum((gray0.astype("float") - gray1.astype("float")) ** 2)
    err /= float(gray0.shape[0] * gray0.shape[1])
    print(f"MSE: {err}")


if __name__ == "__main__":
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("ref", help="reference image")
    ap.add_argument("test", help="test image")
    args = ap.parse_args()
    main(args.ref, args.test)
