def read_stp(stp_path):
    from OCC.Core.STEPControl import STEPControl_Reader
    from OCC.Core.IFSelect import IFSelect_RetDone
    reader = STEPControl_Reader()
    status = reader.ReadFile(stp_path)
    if status != IFSelect_RetDone:
        print(f"[ERROR] Cannot read file {stp_path}")
        return None
    reader.TransferRoots()
    shape = reader.OneShape()
    return shape