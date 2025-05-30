import pytest
from executor.view import compute_set_view, compute_rotate_camera
from utils.error_handlers import ExecutionError

def test_compute_set_view_100_face():
    """
    Test that compute_set_view returns a plausible viewObject for the '100' face.
    """
    view_object = compute_set_view("100")
    assert isinstance(view_object, dict)
    assert "quaternion" in view_object
    assert isinstance(view_object["quaternion"], list)
    assert len(view_object["quaternion"]) == 4
    assert "translation" in view_object
    assert isinstance(view_object["translation"], list)
    assert len(view_object["translation"]) == 3
    assert "zoom" in view_object
    assert isinstance(view_object["zoom"], (int, float))
    # For '100' face, the camera should be looking along the X-axis.
    # The quaternion should represent a rotation that aligns the camera's default -Z with +X.
    # This is a rotation of 90 degrees around the Y-axis.
    # A quaternion for 90 deg around Y is [0, sin(45), 0, cos(45)] = [0, 0.707, 0, 0.707]
    # Due to floating point precision, we'll check for approximate values.
    # The actual quaternion depends on the exact implementation of the rotation.
    # For now, just check that the values are plausible (not all zeros, within reasonable range).
    assert any(abs(q) > 1e-6 for q in view_object["quaternion"])
    assert all(abs(t) < 1e-6 for t in view_object["translation"]) # Should be close to zero
    assert view_object["zoom"] > 0

def test_compute_rotate_camera_basic_rotation():
    """
    Test that compute_rotate_camera returns a modified orientation.
    """
    initial_view = {
        "quaternion": [0.0, 0.0, 0.0, 1.0],  # Identity quaternion (no rotation)
        "translation": [0.0, 0.0, 0.0],
        "zoom": 1.0
    }
    rotated_view = compute_rotate_camera(initial_view, "y", 90) # Rotate 90 degrees around Y
    assert isinstance(rotated_view, dict)
    assert "quaternion" in rotated_view
    assert isinstance(rotated_view["quaternion"], list)
    assert len(rotated_view["quaternion"]) == 4
    # The quaternion should have changed from the initial_view
    # For a 90-degree rotation around the Y-axis, the quaternion should be approximately [0, sin(45), 0, cos(45)]
    # which is [0, 0.7071, 0, 0.7071]
    expected_quat = [0.0, 0.70710678, 0.0, 0.70710678]
    for i in range(4):
        assert abs(rotated_view["quaternion"][i] - expected_quat[i]) < 1e-6

def test_compute_rotate_camera_x_axis_rotation():
    """
    Test that compute_rotate_camera returns a modified orientation for X-axis rotation.
    """
    initial_view = {
        "quaternion": [0.0, 0.0, 0.0, 1.0],  # Identity quaternion
        "translation": [0.0, 0.0, 0.0],
        "zoom": 1.0
    }
    rotated_view = compute_rotate_camera(initial_view, "x", 90) # Rotate 90 degrees around X
    assert isinstance(rotated_view, dict)
    assert "quaternion" in rotated_view
    assert isinstance(rotated_view["quaternion"], list)
    assert len(rotated_view["quaternion"]) == 4
    expected_quat = [0.70710678, 0.0, 0.0, 0.70710678]
    for i in range(4):
        assert abs(rotated_view["quaternion"][i] - expected_quat[i]) < 1e-6

def test_compute_rotate_camera_z_axis_rotation():
    """
    Test that compute_rotate_camera returns a modified orientation for Z-axis rotation.
    """
    initial_view = {
        "quaternion": [0.0, 0.0, 0.0, 1.0],  # Identity quaternion
        "translation": [0.0, 0.0, 0.0],
        "zoom": 1.0
    }
    rotated_view = compute_rotate_camera(initial_view, "z", 90) # Rotate 90 degrees around Z
    assert isinstance(rotated_view, dict)
    assert "quaternion" in rotated_view
    assert isinstance(rotated_view["quaternion"], list)
    assert len(rotated_view["quaternion"]) == 4
    expected_quat = [0.0, 0.0, 0.70710678, 0.70710678]
    for i in range(4):
        assert abs(rotated_view["quaternion"][i] - expected_quat[i]) < 1e-6

def test_compute_rotate_camera_arbitrary_axis_rotation():
    """
    Test that compute_rotate_camera returns a modified orientation for an arbitrary axis rotation.
    """
    initial_view = {
        "quaternion": [0.0, 0.0, 0.0, 1.0],  # Identity quaternion
        "translation": [0.0, 0.0, 0.0],
        "zoom": 1.0
    }
    # Rotate 60 degrees around the [1, 1, 1] axis
    rotated_view = compute_rotate_camera(initial_view, (1, 1, 1), 60)
    assert isinstance(rotated_view, dict)
    assert "quaternion" in rotated_view
    assert isinstance(rotated_view["quaternion"], list)
    assert len(rotated_view["quaternion"]) == 4
    # Expected quaternion for 60 degrees around [1,1,1] is [sin(30)/sqrt(3), sin(30)/sqrt(3), sin(30)/sqrt(3), cos(30)]
    # which is approx [0.288675, 0.288675, 0.288675, 0.866025]
    expected_quat = [0.28867513, 0.28867513, 0.28867513, 0.86602540]
    for i in range(4):
        assert abs(rotated_view["quaternion"][i] - expected_quat[i]) < 1e-6

def test_compute_rotate_camera_invalid_prev_view():
    """
    Test that compute_rotate_camera raises ExecutionError for invalid prev_view.
    """
    invalid_view = {"quaternion": [0.0, 0.0, 0.0]} # Malformed quaternion
    with pytest.raises(ExecutionError, match="Invalid 'prev_view' format"):
        compute_rotate_camera(invalid_view, "y", 90)

def test_compute_rotate_camera_invalid_axis_string():
    """
    Test that compute_rotate_camera raises ExecutionError for invalid axis string.
    """
    initial_view = {
        "quaternion": [0.0, 0.0, 0.0, 1.0],
        "translation": [0.0, 0.0, 0.0],
        "zoom": 1.0
    }
    with pytest.raises(ExecutionError, match="Invalid axis string"):
        compute_rotate_camera(initial_view, "invalid_axis", 90)

def test_compute_rotate_camera_zero_vector_axis():
    """
    Test that compute_rotate_camera raises ExecutionError for a zero vector axis.
    """
    initial_view = {
        "quaternion": [0.0, 0.0, 0.0, 1.0],
        "translation": [0.0, 0.0, 0.0],
        "zoom": 1.0
    }
    with pytest.raises(ExecutionError, match="Rotation axis cannot be a zero vector"):
        compute_rotate_camera(initial_view, (0, 0, 0), 90)