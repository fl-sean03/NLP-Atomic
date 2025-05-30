import pytest
import io
from unittest.mock import patch
from ase.build import bulk
from ase.io import write
from executor.structure import build_structure
from models.commands import BuildStructureParams

def count_atom_records(pdb_content: str) -> int:
    """Counts the number of ATOM records in a PDB string."""
    return pdb_content.count("ATOM")

@pytest.fixture
def mock_ase_write():
    """Fixture to mock ase.io.write to capture output."""
    with patch('ase.io.write') as mock_write:
        yield mock_write

def test_build_structure_atom_count_fcc_al():
    """
    Test that build_structure returns PDB content with the correct number of ATOM records
    for a face-centered cubic (FCC) aluminum structure.
    """
    params = BuildStructureParams(element="Al", lattice="fcc", nx=2, ny=2, nz=2)
    
    # FCC unit cell has 4 atoms. A 2x2x2 supercell should have 4 * 2*2*2 = 32 atoms.
    expected_atom_count = 4 * params.nx * params.ny * params.nz

    pdb_content = build_structure(params)

    assert isinstance(pdb_content, str)
    assert count_atom_records(pdb_content) == expected_atom_count

def test_build_structure_atom_count_bcc_fe():
    """
    Test that build_structure returns PDB content with the correct number of ATOM records
    for a body-centered cubic (BCC) iron structure.
    """
    params = BuildStructureParams(element="Fe", lattice="bcc", nx=3, ny=1, nz=1)
    
    # BCC unit cell has 2 atoms. A 3x1x1 supercell should have 2 * 3*1*1 = 6 atoms.
    expected_atom_count = 2 * params.nx * params.ny * params.nz

    pdb_content = build_structure(params)

    assert isinstance(pdb_content, str)
    assert count_atom_records(pdb_content) == expected_atom_count