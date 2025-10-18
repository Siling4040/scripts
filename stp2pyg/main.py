import argparse

from builder.base import GraphBuilder
from extr.uvnet import AttrExtrUVNet
from utils.io import read_stp

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert STEP files to PyG format.")
    parser.add_argument("-i", type=str, default="./stp", help="Input directory containing STEP files.")
    parser.add_argument("-o", type=str, default="./pyg", help="Output directory for PyG files.")
    parser.add_argument("-w", type=int, default=4, help="Number of worker threads for processing.")
    args = parser.parse_args()

    print("Start building graph from STEP files...")
    constructor = GraphBuilder(args.i, args.o, args.w, AttrExtrUVNet())
    constructor.process()
    print("Finished.")
