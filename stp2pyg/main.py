import argparse

from utils.io import read_stp

from builder.base import GraphBuilder
from extr.uvnet import AttrExtrUVNet

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert STEP files to PyG format.")
    parser.add_argument("-i", type=str, default="../../data/test", help="Input directory containing STEP files.")
    parser.add_argument("-o", type=str, default="../../data/pyg", help="Output directory for PyG files.")
    args = parser.parse_args()

    print("Start constructing graph from STEP files...")
    constructor = GraphBuilder(args.i, args.o, AttrExtrUVNet())
    constructor.process()
    print("Finished.")
