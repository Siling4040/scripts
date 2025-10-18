import torch

from OCC.Core.BRepTools import breptools
from OCC.Core.BRep import BRep_Tool

from extr.base import AttrExtrBase

from utils.geom import get_coord_from_uv, get_normal_from_uv, get_visibility_from_uv
from utils.geom import get_coord_from_t, get_tangent_from_t

class AttrExtrUVNet(AttrExtrBase):
    def __init__(self, num_u=10, num_v=10, num_t=10):
        super().__init__()
        # Number of points for face sampling
        self.num_u = 10
        self.num_v = 10

        # Number of points for edge sampling
        self.num_t = 10

    def face(self, face):
        fattr = []

        # Sample UV points on the face
        umin, umax, vmin, vmax = breptools.UVBounds(face)
        u_samples = torch.linspace(umin, umax, self.num_u)
        v_samples = torch.linspace(vmin, vmax, self.num_v)

        # Extract attributes at each UV sample point
        for u in u_samples:
            fattr.append([])
            for v in v_samples:
                coord = get_coord_from_uv(face, u.item(), v.item())
                normal = get_normal_from_uv(face, u.item(), v.item())
                visibility = get_visibility_from_uv(face, u.item(), v.item())

                fattr[-1].append([*coord, *normal, visibility])

        return fattr

    def edge(self, edge):
        eattr = []

        _, tmin, tmax = BRep_Tool.Curve(edge)
        t_samples = torch.linspace(tmin, tmax, self.num_t)

        for t in t_samples:
            coord = get_coord_from_t(edge, t.item())
            tangent = get_tangent_from_t(edge, t.item())

            eattr.append([*coord, *tangent])
        return eattr