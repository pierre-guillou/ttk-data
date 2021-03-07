import argparse

import topologytoolkit as ttk
import vtk


def main(f0, f1):
    # load the two input images
    im0 = vtk.vtkPNGReader()
    im0.SetFileName(f0)
    im1 = vtk.vtkPNGReader()
    im1.SetFileName(f1)
    im1.Update()
    # convert the images to grayscale
    calc0 = vtk.vtkArrayCalculator()
    calc0.AddVectorArrayName("PNGImage")
    calc0.SetFunction("mag(PNGImage)")
    calc0.SetInputConnection(im0.GetOutputPort())
    calc1 = vtk.vtkArrayCalculator()
    calc1.AddVectorArrayName("PNGImage")
    calc1.SetFunction("mag(PNGImage)")
    calc1.SetInputConnection(im1.GetOutputPort())
    # merge the two arrays with "Append Attributes"
    ma = vtk.vtkMergeArrays()
    ma.AddInputConnection(calc0.GetOutputPort())
    ma.AddInputConnection(calc1.GetOutputPort())
    ma.Update()
    data = ma.GetOutput()
    na = data.GetPointData().GetNumberOfArrays()
    if na == 2:
        # not enough arrays
        print("Images have not the same dimension")
        return
    # compute the L2 distance between the two images
    ldist = ttk.ttkLDistance()
    ldist.SetInputConnection(ma.GetOutputPort())
    ldist.SetInputArrayToProcess(
        0, 0, 0, vtk.vtkDataObject.FIELD_ASSOCIATION_POINTS, "resultArray"
    )
    ldist.SetInputArrayToProcess(
        1, 0, 0, vtk.vtkDataObject.FIELD_ASSOCIATION_POINTS, "resultArray_input_1"
    )
    ldist.Update()
    print(ldist.GetErrorCode())
    print(f"MSE: {ldist.Getresult()}")


if __name__ == "__main__":
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("ref", help="reference image")
    ap.add_argument("test", help="test image")
    args = ap.parse_args()
    main(args.ref, args.test)
