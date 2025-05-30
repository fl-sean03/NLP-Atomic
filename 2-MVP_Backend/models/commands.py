from pydantic import BaseModel, Field, ConfigDict
from typing import Union, List, Literal, Optional

class BuildStructureParams(BaseModel):
    """
    Parameters to build a new atomic structure from raw file text.
    """
    format: Literal["pdb", "xyz", "sdf", "mol2", "cif"] = Field(..., description="File format of the structure data")
    content: str = Field(..., description="Raw molecular data (PDB/XYZ/etc.) as text")
    options: Optional[dict] = Field(None, description="Optional 3Dmol.js addModel options")

    model_config = ConfigDict(extra="forbid")

class RotateCameraParams(BaseModel):
    """
    Parameters to rotate the camera around an axis.
    """
    axis: Union[Literal["x", "y", "z"], List[float]] = Field(..., description="Principal axis name or custom axis vector [x, y, z]")
    angle: float = Field(..., description="Rotation angle in degrees")

    model_config = ConfigDict(extra="forbid")

class Quaternion(BaseModel):
    x: float
    y: float
    z: float
    w: float

    model_config = ConfigDict(extra="forbid")

class Translation(BaseModel):
    x: float
    y: float
    z: float

    model_config = ConfigDict(extra="forbid")

class ViewObject(BaseModel):
    """
    3Dmol.js view state object.
    """
    quaternion: Quaternion = Field(..., description="Rotation quaternion")
    translation: Translation = Field(..., description="Camera translation vector")
    zoom: float = Field(..., description="Camera zoom level")

    model_config = ConfigDict(extra="forbid")

class SetViewParams(BaseModel):
    """
    Parameters to restore a saved camera view.
    """
    viewObject: ViewObject = Field(..., description="3Dmol.js view state object")

    model_config = ConfigDict(extra="forbid")

class LoadPdbParams(BaseModel):
    """
    Parameters to load a PDB entry by ID.
    """
    pdbId: str = Field(..., description="Four-character PDB identifier", pattern=r"^[A-Za-z0-9]{4}$")

    model_config = ConfigDict(extra="forbid")

class SetRepresentationParams(BaseModel):
    """
    Parameters to change the visual style of the model.
    """
    style: Literal["stick", "line", "sphere", "cartoon", "ballAndStick"] = Field(..., description="Representation style for the model")
    options: Optional[dict] = Field(None, description="Style-specific options (radius, scale, etc.)")
    colorScheme: Optional[str] = Field(None, description="Coloring scheme (Jmol, ssPyMol, element, etc.)")
    opacity: Optional[float] = Field(None, description="Opacity value between 0.0 (transparent) and 1.0 (opaque)", ge=0.0, le=1.0)

    model_config = ConfigDict(extra="forbid")

class SetBackgroundColorParams(BaseModel):
    """
    Parameters to change the viewer background color.
    """
    color: str = Field(..., description="CSS color string or hex code (e.g. 'white', '#FF0000')")

    model_config = ConfigDict(extra="forbid")

class TranslateCameraParams(BaseModel):
    """
    Parameters to pan (translate) the camera.
    """
    vector: List[float] = Field(..., description="Translation vector [dx, dy, dz]", min_length=3, max_length=3)

    model_config = ConfigDict(extra="forbid")

class ZoomParams(BaseModel):
    """
    Parameters to zoom the camera in or out.
    """
    factor: float = Field(..., description="Zoom factor (>1 = zoom in; <1 = zoom out)")
    fixedPath: Optional[bool] = Field(None, description="Zoom along fixed path (true) or relative (false)")

    model_config = ConfigDict(extra="forbid")

class ResetViewParams(BaseModel):
    """
    Parameters to reset the camera to default view.
    """
    model_config = ConfigDict(extra="forbid")

class ToggleAxesParams(BaseModel):
    """
    Parameters to show or hide coordinate axes.
    """
    show: bool = Field(..., description="true to show axes; false to hide")

    model_config = ConfigDict(extra="forbid")

class CrystalData(BaseModel):
    a: float = Field(..., description="Cell length a")
    b: float = Field(..., description="Cell length b")
    c: float = Field(..., description="Cell length c")
    alpha: float = Field(..., description="Angle α in degrees")
    beta: float = Field(..., description="Angle β in degrees")
    gamma: float = Field(..., description="Angle γ in degrees")

    model_config = ConfigDict(extra="forbid")

class ToggleUnitCellParams(BaseModel):
    """
    Parameters to show or hide the crystallographic unit cell.
    """
    show: bool = Field(..., description="true to show unit cell; false to hide")
    crystalData: Optional[CrystalData] = Field(None, description="Optional explicit cell parameters")

    model_config = ConfigDict(extra="forbid")

class DisplayMessageParams(BaseModel):
    """
    Parameters to show a chat message in the frontend.
    """
    message: str = Field(..., description="Text to display in the chat pane")
    type: Literal["info", "success", "warning", "error"] = Field(..., description="Severity or style of the message")

    model_config = ConfigDict(extra="forbid")

class Command(BaseModel):
    """
    A single instruction for the frontend viewer.
    """
    command: Literal[
        "buildStructure",
        "loadPdb",
        "setRepresentation",
        "setBackgroundColor",
        "rotateCamera",
        "translateCamera",
        "zoom",
        "resetView",
        "toggleAxes",
        "toggleUnitCell",
        "setView",
        "displayMessage"
    ] = Field(..., description="Name of the command to execute")
    params: Union[
        BuildStructureParams,
        LoadPdbParams,
        SetRepresentationParams,
        SetBackgroundColorParams,
        RotateCameraParams,
        TranslateCameraParams,
        ZoomParams,
        ResetViewParams,
        ToggleAxesParams,
        ToggleUnitCellParams,
        SetViewParams,
        DisplayMessageParams
    ] = Field(..., description="Parameters for the specific command")

    model_config = ConfigDict(extra="forbid")

def validate_commands(raw: List[dict]) -> List[Command]:
    """
    Validates a list of raw command dictionaries against the Command Pydantic model.

    Args:
        raw (List[dict]): A list of dictionaries, each representing a command.

    Returns:
        List[Command]: A list of validated Command objects.

    Raises:
        ValueError: If any command fails validation.
    """
    validated_commands = []
    for i, cmd_data in enumerate(raw):
        try:
            validated_commands.append(Command(**cmd_data))
        except Exception as e:
            raise ValueError(f"Validation error in command {i}: {e}") from e
    return validated_commands