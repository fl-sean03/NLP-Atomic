import os
import json
from typing import List, Optional
import openai
from ..config import OPENAI_API_KEY
from utils.error_handlers import NLPError

openai.api_key = OPENAI_API_KEY

# Define OpenAI function definitions for tool use
OPENAI_FUNCTIONS = [
    {
        "name": "buildStructure",
        "description": "Builds a new atomic structure in the 3D viewer from raw file text content. This is useful for displaying custom structures like unit cells or specific molecular configurations provided as text data (e.g., PDB, XYZ, CIF).",
        "parameters": {
            "type": "object",
            "properties": {
                "format": {
                    "type": "string",
                    "description": "File format of the structure data",
                    "enum": ["pdb", "xyz", "sdf", "mol2", "cif"]
                },
                "content": {
                    "type": "string",
                    "description": "Raw molecular data (PDB/XYZ/etc.) as text"
                },
                "options": {
                    "type": "object",
                    "description": "Optional 3Dmol.js addModel options",
                    "additionalProperties": True
                }
            },
            "required": ["format", "content"]
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
        "content": json.dumps({"format": "cif", "content": "placeholder_copper_sc_cif_data"})
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
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that translates natural language into 3Dmol.js viewer commands. Respond only with valid JSON commands using the provided functions."
        }
    ]

    # Add few-shot examples
    for example in FEW_SHOT_EXAMPLES:
        messages.append(example)

    # Add user prompt
    messages.append({"role": "user", "content": prompt})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-0613",
            functions=OPENAI_FUNCTIONS,
            messages=messages,
            function_call="auto" # Allow the model to decide whether to call a function
        )
    except Exception as e:
        raise NLPError(f"OpenAI API call failed: {e}")

    if not response.choices[0].message.get("function_call"):
        raise NLPError("LLM did not return a function call.")

    try:
        function_call_args = response.choices[0].message.function_call.arguments
        commands = json.loads(function_call_args)
        return commands
    except (AttributeError, KeyError, json.JSONDecodeError) as e:
        raise NLPError(f"Malformed function call arguments from OpenAI API: {e}")

if __name__ == "__main__":
    try:
        result = generate_commands("3x3x3 FCC Al")
        print(json.dumps(result, indent=2))
    except NLPError as e:
        print(f"Error: {e}")