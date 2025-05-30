import io
from ase.build import bulk
from ase.io import write
from models.commands import BuildStructureParams
from utils.error_handlers import ExecutionError

def build_structure(params: BuildStructureParams) -> str:
    """
    Builds an atomic structure using ASE based on the provided parameters.

    Args:
        params (BuildStructureParams): Parameters for building the structure,
                                       including element, lattice, and supercell dimensions,
                                       plus the desired output format ("pdb", "xyz", etc.).

    Returns:
        str: The atomic structure in the specified format as a string.

    Raises:
        ExecutionError: If there is an error during the structure building process using ASE.
    """
    try:
        # 1. Build *conventional* cubic cell (so fcc gives 4 atoms, bcc gives 2)
        a_val = params.a if params.a is not None else None
        cell = bulk(params.element, params.lattice, a=a_val, cubic=True)

        # 2. Tile into supercell
        supercell = cell * (params.nx, params.ny, params.nz)

        # 3. Determine ASE format name
        fmt = params.format.lower()
        if fmt == "pdb":
            ase_fmt = "proteindatabank"
        else:
            ase_fmt = fmt

        # 4. Write into a string buffer
        buffer = io.StringIO()
        write(buffer, supercell, format=ase_fmt, write_arrays=True)
        return buffer.getvalue()

    except Exception as e:
        # Wrap any ASE/IO errors in our ExecutionError
        raise ExecutionError(f"Failed to build structure: {e}")