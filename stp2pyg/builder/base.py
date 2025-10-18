import os
import torch
from torch_geometric.data import Data

from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_EDGE
from OCC.Core.TopTools import TopTools_IndexedMapOfShape
from OCC.Core.TopTools import TopTools_IndexedDataMapOfShapeListOfShape
from OCC.Core.TopExp import topexp
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
from OCC.Extend.TopologyUtils import TopologyExplorer

import concurrent.futures
import threading

from tqdm import tqdm

from utils.io import read_stp
from utils.geom import is_3d_curve, is_seam

class GraphBuilder:
    def __init__(self, stp_dir, pyg_dir, worker_num, extr, self_loop=False):
        self.stp_dir = stp_dir
        self.pyg_dir = pyg_dir
        self.worker_num = worker_num
        self.extr = extr
        self.self_loop = False

        os.makedirs(self.pyg_dir, exist_ok=True)

    def process(self):
        thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=self.worker_num)
        submit_semaphore = threading.Semaphore(self.worker_num)
        print("Thread pool created with {} workers.".format(self.worker_num))

        filenames = [filename for filename in os.listdir(self.stp_dir) if filename.endswith(".stp") or filename.endswith(".step")]
        for filename in tqdm(filenames):
            stp_path = os.path.join(self.stp_dir, filename)
            pyg_path = os.path.join(self.pyg_dir, filename.replace(".stp", ".pyg").replace(".step", ".pyg"))

            # Submit tasks with semaphore control
            submit_semaphore.acquire()
            future = thread_pool.submit(self.process_one_stp, stp_path, pyg_path)
            future.add_done_callback(lambda p: submit_semaphore.release())

        thread_pool.shutdown(wait=True)

    def process_one_stp(self, stp_path, pyg_path):
        shape = read_stp(stp_path)
        if shape.IsNull():
            tqdm.write(f"[ERROR] Empty shape for {stp_path}, skipping...")
            return
        
        graph = Data()
        # Construct edge_index
        topExp = TopologyExplorer(shape)
        face_mapper = {face: idx for idx, face in enumerate(topExp.faces())}
        graph.edge_index = self.get_edge_index(shape, face_mapper)
        # Construct node and edge attributes
        graph.x = self.get_node_attrs(shape)
        graph.edge_attr = self.get_edge_attr(shape)

        if graph.validate():
            torch.save(graph, pyg_path)
            tqdm.write(f"[INFO] {graph} saved to {pyg_path}")
        else:
            tqdm.write(f"[ERROR] Invalid graph for {stp_path}, skipping...")
        
    def get_edge_index(self, shape, face_mapper):
        src = []
        dst = []

        topExp = TopologyExplorer(shape)
        edges = topExp.edges()
        for edge in edges:
            # Skip non-curves
            if not is_3d_curve(edge):
                continue

            # Get adjacent faces
            adj_faces = list(topExp.faces_from_edge(edge))
            if len(adj_faces) == 1:
                if is_seam(edge, adj_faces[0]) and self.self_loop:
                    face_idx = face_mapper[adj_faces[0]]
                    src.append(face_idx)
                    dst.append(face_idx)
            elif len(adj_faces) == 2:
                src_face_idx = face_mapper[adj_faces[0]]
                dst_face_idx = face_mapper[adj_faces[1]]
                src.append(src_face_idx); dst.append(dst_face_idx)
                src.append(dst_face_idx); dst.append(src_face_idx)
            else: # Non-manifold
                tqdm.write("[WARNING] Non-manifold edge detected")

        src = torch.tensor(src, dtype=torch.long)
        dst = torch.tensor(dst, dtype=torch.long)
        edge_index = torch.stack([src, dst], dim=0)
        return edge_index

    def get_node_attrs(self, shape):
        node_attrs = []

        topExp = TopologyExplorer(shape)
        faces = topExp.faces()
        for face in faces:
            node_attrs.append(self.extr.face(face))

        return torch.tensor(node_attrs)

    def get_edge_attr(self, shape):
        edge_attr = []

        topExp = TopologyExplorer(shape)
        edges = topExp.edges()
        for edge in edges:
            # Skip non-curves
            if not is_3d_curve(edge):
                continue
            
            adj_faces = list(topExp.faces_from_edge(edge))
            if len(adj_faces) == 1:
                if is_seam(edge, adj_faces[0]) and self.self_loop:
                    edge_attr.append(self.extr.edge(edge))
            elif len(adj_faces) == 2:
                edge_attr.append(self.extr.edge(edge))
                edge_attr.append(self.extr.edge(edge))

        return torch.tensor(edge_attr)