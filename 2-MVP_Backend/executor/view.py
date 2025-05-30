from typing import Union, Tuple
import numpy as np
from scipy.spatial.transform import Rotation as R

from utils.error_handlers import ExecutionError

def compute_set_view(face: str) -> dict:
    """
    Computes camera/view parameters for viewer commands based on a specified face.

    Args:
        face (str): One of "100", "010", "001", "110", "111".

    Returns:
        dict: A viewObject dict matching 3Dmol.js viewer.getView() shape,
              containing 'quaternion', 'translation', and 'zoom'.

    Raises:
        ExecutionError: If an invalid face is provided.
    """
    # Define view directions and up vectors for common faces
    # These are normalized vectors representing the camera's look direction
    # and the 'up' direction in the scene.
    view_presets = {
        "100": {"direction": np.array([1, 0, 0]), "up": np.array([0, 1, 0])},
        "010": {"direction": np.array([0, 1, 0]), "up": np.array([0, 0, 1])},
        "001": {"direction": np.array([0, 0, 1]), "up": np.array([0, 1, 0])},
        "110": {"direction": np.array([1, 1, 0]), "up": np.array([0, 0, 1])},
        "111": {"direction": np.array([1, 1, 1]), "up": np.array([0, 1, 0])},
    }

    if face not in view_presets:
        raise ExecutionError(f"Invalid face provided: {face}. Must be one of {list(view_presets.keys())}")

    direction = view_presets[face]["direction"]
    up_vector = view_presets[face]["up"]

    # Calculate the rotation to align the camera with the desired direction
    # The camera typically looks down its negative Z-axis.
    # We need a rotation that transforms [0,0,-1] (camera's default look) to 'direction'.
    # This can be done by finding the rotation from the default camera orientation to the target.
    # A common approach is to use the cross product to find the axis of rotation
    # and the dot product for the angle.

    # Default camera look direction (negative Z-axis)
    default_look = np.array([0, 0, -1])

    # Normalize the target direction
    direction = direction / np.linalg.norm(direction)

    # Calculate rotation axis and angle
    axis = np.cross(default_look, direction)
    angle = np.arccos(np.dot(default_look, direction))

    # Handle the case where default_look and direction are collinear (axis is zero vector)
    if np.linalg.norm(axis) < 1e-6:
        if np.dot(default_look, direction) > 0.999: # Same direction
            rotation = R.from_quat([0, 0, 0, 1]) # No rotation
        else: # Opposite direction (180 degree rotation around Y-axis)
            rotation = R.from_euler('y', 180, degrees=True)
    else:
        axis = axis / np.linalg.norm(axis)
        rotation = R.from_rotvec(angle * axis)

    # Convert to quaternion (x, y, z, w)
    quat = rotation.as_quat()

    # 3Dmol.js quaternion format is [x, y, z, w]
    # The translation and zoom values are typically handled by the frontend or are default.
    # For simplicity, we'll return a default translation and zoom.
    return {
        "quaternion": quat.tolist(),
        "translation": [0.0, 0.0, 0.0],
        "zoom": 1.0
    }

def compute_rotate_camera(
    prev_view: dict,
    axis: Union[str, Tuple[float, float, float]],
    angle: float
) -> dict:
    """
    Applies a rotation to an existing viewObject.

    Args:
        prev_view (dict): The existing viewObject from 3Dmol.js, containing
                          at least a 'quaternion' list [x, y, z, w].
        axis (Union[str, Tuple[float, float, float]]): The axis of rotation.
                                                        Can be "x", "y", "z" or a 3-tuple (x, y, z).
        angle (float): The angle of rotation in degrees.

    Returns:
        dict: A new viewObject dict with the updated quaternion.

    Raises:
        ExecutionError: If the prev_view is malformed or axis is invalid.
    """
    if "quaternion" not in prev_view or not isinstance(prev_view["quaternion"], list) or len(prev_view["quaternion"]) != 4:
        raise ExecutionError("Invalid 'prev_view' format. Missing or malformed 'quaternion'.")

    # Convert previous quaternion to a scipy Rotation object
    # scipy.spatial.transform.Rotation.from_quat expects [x, y, z, w]
    prev_quat = np.array(prev_view["quaternion"])
    prev_rotation = R.from_quat(prev_quat)

    # Determine the rotation axis vector
    if isinstance(axis, str):
        if axis.lower() == "x":
            rot_axis = np.array([1, 0, 0])
        elif axis.lower() == "y":
            rot_axis = np.array([0, 1, 0])
        elif axis.lower() == "z":
            rot_axis = np.array([0, 0, 1])
        else:
            raise ExecutionError(f"Invalid axis string: {axis}. Must be 'x', 'y', or 'z'.")
    elif isinstance(axis, tuple) and len(axis) == 3:
        rot_axis = np.array(axis)
        if np.linalg.norm(rot_axis) < 1e-6:
            raise ExecutionError("Rotation axis cannot be a zero vector.")
        rot_axis = rot_axis / np.linalg.norm(rot_axis) # Normalize
    else:
        raise ExecutionError(f"Invalid axis format: {axis}. Must be 'x', 'y', 'z' or a 3-tuple of floats.")

    # Create a new rotation from axis and angle
    # scipy.spatial.transform.Rotation.from_rotvec expects angle in radians
    rotation_to_apply = R.from_rotvec(np.radians(angle) * rot_axis)

    # Combine the rotations: new_rotation = rotation_to_apply * prev_rotation
    # Note: Quaternion multiplication order matters. If applying rotation relative to current camera frame,
    # it's `new_rotation = prev_rotation * rotation_to_apply`.
    # If applying rotation relative to the world frame, it's `new_rotation = rotation_to_apply * prev_rotation`.
    # Assuming rotation relative to the world frame for simplicity, as is common for camera controls.
    new_rotation = rotation_to_apply * prev_rotation

    # Convert the new rotation back to a quaternion
    new_quat = new_rotation.as_quat()

    # Create the new viewObject, preserving other properties if they exist
    new_view = prev_view.copy()
    new_view["quaternion"] = new_quat.tolist()

    return new_view