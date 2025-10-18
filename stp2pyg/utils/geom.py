def is_3d_curve(edge):
    from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
    curve = BRepAdaptor_Curve(edge)
    return curve.Is3DCurve()

def is_seam(edge, face):
    from OCC.Core.ShapeAnalysis import ShapeAnalysis_Edge
    return ShapeAnalysis_Edge().IsSeam(edge, face)

# Face attrs
def get_coord_from_uv(face, u, v):
    from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
    from OCC.Core.gp import gp_Pnt

    surface = BRepAdaptor_Surface(face)
    pnt = gp_Pnt()
    surface.D0(u, v, pnt)
    return [pnt.X(), pnt.Y(), pnt.Z()]

def get_normal_from_uv(face, u, v):
    from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
    from OCC.Core.TopAbs import TopAbs_REVERSED
    from OCC.Core.gp import gp_Vec, gp_Pnt
    from OCC.Core.Precision import precision

    surface = BRepAdaptor_Surface(face)
    tangent_u = gp_Vec()
    tangent_v = gp_Vec()
    surface.D1(u, v, gp_Pnt(), tangent_u, tangent_v)
    normal = tangent_u.Crossed(tangent_v)
    if normal.Magnitude() < precision.Confusion():
        return [0.0, 0.0, 0.0]
    normal.Normalize()
    if face.Orientation() == TopAbs_REVERSED:
        normal.Reverse()
    return [normal.X(), normal.Y(), normal.Z()]

def get_visibility_from_uv(face, u, v):
    from OCC.Core.BRepTopAdaptor import BRepTopAdaptor_FClass2d
    from OCC.Core.gp import gp_Pnt2d
    trimmed = BRepTopAdaptor_FClass2d(face, 1e-9)
    return trimmed.Perform(gp_Pnt2d(u, v))

# Edge attrs
def get_coord_from_t(edge, t):
    from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
    from OCC.Core.gp import gp_Pnt

    curve = BRepAdaptor_Curve(edge)
    pnt = gp_Pnt()
    curve.D0(t, pnt)
    return [pnt.X(), pnt.Y(), pnt.Z()]

def get_tangent_from_t(edge, t):
    from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
    from OCC.Core.gp import gp_Vec, gp_Pnt
    from OCC.Core.Precision import precision

    curve = BRepAdaptor_Curve(edge)
    tangent = gp_Vec()
    curve.D1(t, gp_Pnt(), tangent)
    if tangent.Magnitude() < precision.Confusion():
        return [0.0, 0.0, 0.0]
    tangent.Normalize()
    return [tangent.X(), tangent.Y(), tangent.Z()]