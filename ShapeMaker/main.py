import argparse
import os

from maker import ShapeMaker

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Make and save a simple shape.")
    parser.add_argument("-o", type=str, default="./out", help="Output directory for the shape STEP file.")
    args = parser.parse_args()
    os.makedirs(args.o, exist_ok=True)

    shapes = [
        ["box", [10, 20, 30]],
        ["sphere", [15]],
        ["cylinder", [10, 25]],
        ["cone", [10, 20]],
        ["torus", [10, 3]],
    ]

    for shape in shapes:
        shape_type = shape[0]
        make_args = shape[1]
        print(f"Making a {shape_type} shape...")
        shape = ShapeMaker.make(shape_type, *make_args)
        ShapeMaker.save_shape(shape, os.path.join(args.o, f"{shape_type}.stp"))
        print("Done.")