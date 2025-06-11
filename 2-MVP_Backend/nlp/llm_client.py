import os
import json
from typing import List, Optional
from openai import OpenAI
from config import OPENAI_API_KEY
from utils.error_handlers import NLPError
import functools

client = OpenAI(api_key=OPENAI_API_KEY)

# Define OpenAI function definitions for tool use
OPENAI_FUNCTIONS = [
    {
        "name": "buildStructure",
        "description": "Builds a new atomic structure in the 3D viewer from raw file text content. This is useful for displaying custom structures like unit cells or specific molecular configurations provided as text data (e.g., PDB, XYZ, CIF).",
        "parameters": {
            "type": "object",
            "properties": {
                "element": {
                    "type": "string",
                    "description": "Chemical symbol of the element (e.g., 'Al', 'Fe')"
                },
                "lattice": {
                    "type": "string",
                    "description": "Lattice type (e.g., 'fcc', 'bcc', 'hcp')"
                },
                "nx": {
                    "type": "integer",
                    "description": "Supercell dimension along x-axis",
                    "default": 1
                },
                "ny": {
                    "type": "integer",
                    "description": "Supercell dimension along y-axis",
                    "default": 1
                },
                "nz": {
                    "type": "integer",
                    "description": "Supercell dimension along z-axis",
                    "default": 1
                },
                "a": {
                    "type": "number",
                    "description": "Lattice constant in Angstroms (if not default for element/lattice)"
                }
            },
            "required": ["element", "lattice"]
        }
    },
    {
        "name": "rotateCamera",
        "description": "Rotates the 3D viewer's camera around a specified axis by a given angle. Useful for adjusting the view to inspect the structure from different perspectives.",
        "parameters": {
            "type": "object",
            "properties": {
                "axis": {
                    "oneOf": [
                        {
                            "type": "string",
                            "description": "Principal axis name",
                            "enum": ["x", "y", "z"]
                        },
                        {
                            "type": "array",
                            "description": "Custom axis vector [x, y, z]",
                            "items": {"type": "number"},
                            "minItems": 3,
                            "maxItems": 3
                        }
                    ]
                },
                "angle": {
                    "type": "number",
                    "description": "Rotation angle in degrees"
                }
            },
            "required": ["axis", "angle"]
        }
    },
    {
        "name": "setView",
        "description": "Restores the 3D viewer's camera to a previously saved view state. This allows for quick navigation to predefined or user-saved camera positions and zoom levels.",
        "parameters": {
            "type": "object",
            "properties": {
                "viewObject": {
                    "type": "object",
                    "description": "3Dmol.js view state object",
                    "properties": {
                        "quaternion": {
                            "type": "object",
                            "description": "Rotation quaternion",
                            "properties": {
                                "x": {"type": "number"},
                                "y": {"type": "number"},
                                "z": {"type": "number"},
                                "w": {"type": "number"}
                            },
                            "required": ["x", "y", "z", "w"]
                        },
                        "translation": {
                            "type": "object",
                            "description": "Camera translation vector",
                            "properties": {
                                "x": {"type": "number"},
                                "y": {"type": "number"},
                                "z": {"type": "number"}
                            },
                            "required": ["x", "y", "z"]
                        },
                        "zoom": {
                            "type": "number",
                            "description": "Camera zoom level"
                        }
                    },
                    "required": ["quaternion", "translation", "zoom"]
                }
            },
            "required": ["viewObject"]
        }
    }
]

FEW_SHOT_EXAMPLES = [
    {
        "role": "user",
        "content": "build a simple cubic cell of copper"
    },
    {
        "role": "function",
        "name": "buildStructure",
        "content": json.dumps({"element": "copper", "lattice": "sc"})
    },
    {
        "role": "user",
        "content": "rotate the view around the x-axis by 90 degrees"
    },
    {
        "role": "function",
        "name": "rotateCamera",
        "content": json.dumps({"axis": "x", "angle": 90})
    },
    {
        "role": "user",
        "content": "set the view to the default orientation"
    },
    {
        "role": "function",
        "name": "setView",
        "content": json.dumps({"viewObject": {"quaternion": {"x": 0, "y": 0, "z": 0, "w": 1}, "translation": {"x": 0, "y": 0, "z": 0}, "zoom": 1}})
    }
]

# Pre-process initial messages (system prompt + few-shot examples)
_INITIAL_MESSAGES = [
    {
        "role": "system",
        "content": "You are a helpful assistant that translates natural language into 3Dmol.js viewer commands. Respond only with valid JSON commands using the provided functions."
    }
]
for example in FEW_SHOT_EXAMPLES:
    _INITIAL_MESSAGES.append(example)

@functools.lru_cache(maxsize=128)
def generate_commands(
    prompt: str,
    context: Optional[List[dict]] = None
) -> List[dict]:
    """
    Generates a list of commands based on the user's natural language prompt
    using the OpenAI ChatCompletion API with function calling.

    Args:
        prompt: The user's natural-language message.
        context: Optional history of previous commands for multi-turn conversations.

    Returns:
        A list of raw command dictionaries.

    Raises:
        NLPError: If the API call fails or the response is malformed.
    """
    messages = list(_INITIAL_MESSAGES) # Create a mutable copy
    if context:
        messages.extend(context)

    # Add user prompt
    messages.append({"role": "user", "content": prompt})

    try:
        response = client.chat.completions.create(
            model="gpt-4-0613",
            tools=[{"type": "function", "function": f} for f in OPENAI_FUNCTIONS],
            messages=messages,
            tool_choice="auto" # Allow the model to decide whether to call a function
        )
    except Exception as e:
        raise NLPError(f"OpenAI API call failed: {e}")

    if not response.choices[0].message.tool_calls:
        raise NLPError("LLM did not return a tool call.")

    try:
        tool_call = response.choices[0].message.tool_calls[0]
        function_call_name = tool_call.function.name
        function_call_args = json.loads(tool_call.function.arguments)
        commands = [{"command": function_call_name, "params": function_call_args}]
        return commands
    except (AttributeError, KeyError, json.JSONDecodeError) as e:
        raise NLPError(f"Malformed tool call arguments from OpenAI API: {e}")

if __name__ == "__main__":
    try:
        result = generate_commands("3x3x3 FCC Al")
        print(json.dumps(result, indent=2))
    except NLPError as e:
        print(f"Error: {e}")