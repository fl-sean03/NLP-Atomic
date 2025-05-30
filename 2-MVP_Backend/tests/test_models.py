import pytest
from pydantic import ValidationError
from models.commands import validate_commands

def test_validate_commands_valid_json():
    """
    Test that validate_commands successfully validates a correct command JSON.
    """
    valid_command_list = [
        {
            "command": "displayMessage",
            "params": {
                "message": "Hello, world!",
                "type": "info"
            }
        }
    ]
    validated_commands = validate_commands(valid_command_list)
    assert len(validated_commands) == 1
    assert validated_commands[0].command == "displayMessage"
    assert validated_commands[0].params.message == "Hello, world!"
    assert validated_commands[0].params.type == "info"

def test_validate_commands_invalid_json():
    """
    Test that validate_commands raises ValueError for invalid command JSON.
    """
    invalid_command_list = [
        {
            "command": "invalidCommand",  # Invalid command name
            "params": {
                "message": "Hello, world!",
                "type": "info"
            }
        }
    ]
    with pytest.raises(ValueError):
        validate_commands(invalid_command_list)

def test_validate_commands_missing_required_field():
    """
    Test that validate_commands raises ValueError for missing required fields.
    """
    missing_field_command_list = [
        {
            "command": "displayMessage",
            "params": {
                "message": "Hello, world!"
                # 'type' field is missing
            }
        }
    ]
    with pytest.raises(ValueError):
        validate_commands(missing_field_command_list)

def test_validate_commands_extra_field():
    """
    Test that validate_commands raises ValueError for extra fields.
    """
    extra_field_command_list = [
        {
            "command": "displayMessage",
            "params": {
                "message": "Hello, world!",
                "type": "info",
                "extra_field": "should_not_be_here"
            }
        }
    ]
    with pytest.raises(ValueError):
        validate_commands(extra_field_command_list)