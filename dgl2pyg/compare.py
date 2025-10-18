import argparse
import warnings

from comparator import DglPygComparator

if __name__ == "__main__":
    warnings.filterwarnings("ignore")

    parser = argparse.ArgumentParser(description="Compare Dgl and PyG")
    parser.add_argument("-i", type=str, default="./dgl", help="Path to the input DGL graph files")
    parser.add_argument("-o", type=str, default="./pyg", help="Path to the input PyG graph files")
    args = parser.parse_args()

    print("Starting comparison...")
    cmp = DglPygComparator(args.i, args.o)
    cmp.compare()
    print("Comparison completed.")
