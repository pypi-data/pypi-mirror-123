import ase.io
import os
import cavd.Structure
import cavd.BVAnalysis


def bv_calculation(filename, moveion='Li',valenceofmoveion=1,resolution=0.1 ):
    atoms = ase.io.read(filename, store_tags=True)
    struc = cavd.Structure.Structure()
    struc.GetAseStructure(atoms)
    bvs = cavd.BVAnalysis.BVAnalysis()
    bvs.SetStructure(struc)
    bvs.SetMoveIon(moveion)
    bvs.ValenceOfMoveIon = valenceofmoveion
    bvs.SetLengthResolution(resolution)
    bvs.CaluBVSE(None)
    bv_data = bvs.get_data()
    bvs.SaveBVSEData(os.path.splitext(filename)[0])
    return bvs.Ea['BVSE']

