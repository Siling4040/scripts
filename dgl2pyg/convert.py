import argparse
import warnings

from converter import Dgl2PygConverter

if __name__ == "__main__":
    warnings.filterwarnings("ignore")

    parser = argparse.ArgumentParser(description="Convert DGL graph to PyG format")
    parser.add_argument("-i", type=str, default="./dgl", help="Path to the input DGL graph files")
    parser.add_argument("-o", type=str, default="./pyg", help="Path to save the output PyG graph files")
    args = parser.parse_args()

    print("Source (DGL):", args.i)
    print("Destination (PyG):", args.o)
    print("Starting conversion...")
    converter = Dgl2PygConverter(args.i, args.o)
    converter.process()
    print("Conversion completed.")