import dgl
from dgl.data.utils import load_graphs
import os
import torch
from torch_geometric.data import Data
from tqdm import tqdm

class Dgl2PygConverter:
    def __init__(self, dgl_dir, pyg_dir):
        self.dgl_dir = dgl_dir
        self.pyg_dir = pyg_dir
        os.makedirs(self.pyg_dir, exist_ok=True)

    def process(self):
        filenames = [filename for filename in os.listdir(self.dgl_dir) if filename.endswith('.bin')]
        for filename in tqdm(filenames):
            dgl_path = os.path.join(self.dgl_dir, filename)
            pyg_path = os.path.join(self.pyg_dir, filename.replace('.bin', '.pyg'))
            self.process_one_graph(dgl_path, pyg_path)

    def process_one_graph(self, dgl_path, pyg_path):
        # Convert DGL graph to PyG graph
        graph_pyg = self.dgl2pyg(dgl_path)
        assert self.dgl_stats(graph_dgl) == self.pyg_stats(graph_pyg), "Graph statistics do not match after conversion!"
        
        # Save PyG graph
        torch.save(graph_pyg, pyg_path)

    @staticmethod
    def dgl2pyg(dgl_path):
         # Load DGL graph
        graph = load_graphs(dgl_path)
        graph_dgl = graph[0][0]
        
        # Convert to PyG format
        graph_pyg = Data()
        # Nodes
        graph_pyg.x = graph_dgl.ndata['x']
        # Edges
        src, dst = graph_dgl.edges()
        graph_pyg.edge_index = torch.stack([src, dst], dim=0)
        graph_pyg.edge_attr = graph_dgl.edata['x']

        return graph_pyg

    @staticmethod
    def dgl_stats(graph_dgl):
        num_nodes = graph_dgl.num_nodes()
        num_edges = graph_dgl.num_edges()
        dim_node_features = graph_dgl.ndata['x'].shape[1:] if 'x' in graph_dgl.ndata else None
        dim_edge_features = graph_dgl.edata['x'].shape[1:] if 'x' in graph_dgl.edata else None

        return {
            "num_nodes": num_nodes,
            "num_edges": num_edges,
            "dim_node_features": dim_node_features,
            "dim_edge_features": dim_edge_features
        }

    @staticmethod
    def pyg_stats(graph_pyg):
        num_nodes = graph_pyg.num_nodes
        num_edges = graph_pyg.num_edges
        dim_node_features = graph_pyg.x.shape[1:] if graph_pyg.x is not None else None
        dim_edge_features = graph_pyg.edge_attr.shape[1:] if graph_pyg.edge_attr is not None else None

        return {
            "num_nodes": num_nodes,
            "num_edges": num_edges,
            "dim_node_features": dim_node_features,
            "dim_edge_features": dim_edge_features
        }
        