import os
import torch
from dgl.data import load_graphs
from tqdm import tqdm
from converter import Dgl2PygConverter

class DglPygComparator:
    def __init__(self, dgl_dir, pyg_dir):
        self.dgl_dir = dgl_dir
        self.pyg_dir = pyg_dir

    def compare(self):
        filenames = [filename for filename in os.listdir(self.dgl_dir) if filename.endswith('.bin')]
        for filename in tqdm(filenames):
            dgl_path = os.path.join(self.dgl_dir, filename)
            pyg_path = os.path.join(self.pyg_dir, filename).replace("bin", "pyg")

            if self.compare_one_graph(dgl_path, pyg_path):
                tqdm.write(f"[Graphs {filename} match.")
            else:
                tqdm.write(f"Graphs {filename} do NOT match!")

    def compare_one_graph(self, dgl_path, pyg_path):
        graph_pyg_raw = torch.load(pyg_path, weights_only=False)
        graph_pyg_dgl = Dgl2PygConverter.dgl2pyg(dgl_path)
        print(graph_pyg_raw)
        print(graph_pyg_dgl)

        match = True
        if not torch.equal(graph_pyg_raw.x, graph_pyg_dgl.x):
            tqdm.write("Node features do not match.")
            match = False

        if not torch.equal(graph_pyg_raw.edge_index, graph_pyg_dgl.edge_index):
            tqdm.write("Edge indices do not match.")
            match = False

        if not torch.equal(graph_pyg_raw.edge_attr, graph_pyg_dgl.edge_attr):
            tqdm.write("Edge attributes do not match.")
            match = False

        return match
