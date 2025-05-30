# JSON Schema Definitions for Frontend Commands

This document provides the JSON Schema definitions for all commands and their associated parameters, as defined by the Pydantic models in [`2-MVP_Backend/models/commands.py`](2-MVP_Backend/models/commands.py). These schemas ensure consistent data validation for interactions between the backend and frontend.

## Command Schema

The `Command` schema defines the structure for a single instruction sent to the frontend viewer.

```json
{
  "title": "Command",
  "description": "A single instruction for the frontend viewer.",
  "type": "object",
  "properties": {
    "command": {
      "description": "Name of the command to execute",
      "enum": [
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
      ],
      "type": "string"
    },
    "params": {
      "description": "Parameters for the specific command",
      "oneOf": [
        {
          "$ref": "#/$defs/BuildStructureParams"
        },
        {
          "$ref": "#/$defs/LoadPdbParams"
        },
        {
          "$ref": "#/$defs/SetRepresentationParams"
        },
        {
          "$ref": "#/$defs/SetBackgroundColorParams"
        },
        {
          "$ref": "#/$defs/RotateCameraParams"
        },
        {
          "$ref": "#/$defs/TranslateCameraParams"
        },
        {
          "$ref": "#/$defs/ZoomParams"
        },
        {
          "$ref": "#/$defs/ResetViewParams"
        },
        {
          "$ref": "#/$defs/ToggleAxesParams"
        },
        {
          "$ref": "#/$defs/ToggleUnitCellParams"
        },
        {
          "$ref": "#/$defs/SetViewParams"
        },
        {
          "$ref": "#/$defs/DisplayMessageParams"
        }
      ]
    }
  },
  "required": [
    "command",
    "params"
  ],
  "$defs": {
    "BuildStructureParams": {
      "title": "BuildStructureParams",
      "description": "Parameters to build a new atomic structure using ASE.",
      "type": "object",
      "properties": {
        "element": {
          "description": "Chemical symbol of the element (e.g., 'Al', 'Fe')",
          "type": "string"
        },
        "lattice": {
          "description": "Lattice type (e.g., 'fcc', 'bcc', 'hcp')",
          "type": "string"
        },
        "nx": {
          "description": "Supercell dimension along x-axis",
          "default": 1,
          "type": "integer"
        },
        "ny": {
          "description": "Supercell dimension along y-axis",
          "default": 1,
          "type": "integer"
        },
        "nz": {
          "description": "Supercell dimension along z-axis",
          "default": 1,
          "type": "integer"
        },
        "a": {
          "description": "Lattice constant in Angstroms (if not default for element/lattice)",
          "anyOf": [
            {
              "type": "number"
            },
            {
              "type": "null"
            }
          ]
        },
        "format": {
          "description": "Output file format for the structure data",
          "default": "pdb",
          "enum": [
            "pdb",
            "xyz",
            "cif"
          ],
          "type": "string"
        }
      },
      "required": [
        "element",
        "lattice"
      ],
      "additionalProperties": false
    },
    "RotateCameraParams": {
      "title": "RotateCameraParams",
      "description": "Parameters to rotate the camera around an axis.",
      "type": "object",
      "properties": {
        "axis": {
          "description": "Principal axis name or custom axis vector [x, y, z]",
          "anyOf": [
            {
              "enum": [
                "x",
                "y",
                "z"
              ],
              "type": "string"
            },
            {
              "type": "array",
              "items": {
                "type": "number"
              }
            }
          ]
        },
        "angle": {
          "description": "Rotation angle in degrees",
          "type": "number"
        }
      },
      "required": [
        "axis",
        "angle"
      ],
      "additionalProperties": false
    },
    "Quaternion": {
      "title": "Quaternion",
      "type": "object",
      "properties": {
        "x": {
          "type": "number"
        },
        "y": {
          "type": "number"
        },
        "z": {
          "type": "number"
        },
        "w": {
          "type": "number"
        }
      },
      "required": [
        "x",
        "y",
        "z",
        "w"
      ],
      "additionalProperties": false
    },
    "Translation": {
      "title": "Translation",
      "type": "object",
      "properties": {
        "x": {
          "type": "number"
        },
        "y": {
          "type": "number"
        },
        "z": {
          "type": "number"
        }
      },
      "required": [
        "x",
        "y",
        "z"
      ],
      "additionalProperties": false
    },
    "ViewObject": {
      "title": "ViewObject",
      "description": "3Dmol.js view state object.",
      "type": "object",
      "properties": {
        "quaternion": {
          "$ref": "#/$defs/Quaternion"
        },
        "translation": {
          "$ref": "#/$defs/Translation"
        },
        "zoom": {
          "description": "Camera zoom level",
          "type": "number"
        }
      },
      "required": [
        "quaternion",
        "translation",
        "zoom"
      ],
      "additionalProperties": false
    },
    "SetViewParams": {
      "title": "SetViewParams",
      "description": "Parameters to restore a saved camera view.",
      "type": "object",
      "properties": {
        "viewObject": {
          "description": "3Dmol.js view state object",
          "$ref": "#/$defs/ViewObject"
        }
      },
      "required": [
        "viewObject"
      ],
      "additionalProperties": false
    },
    "LoadPdbParams": {
      "title": "LoadPdbParams",
      "description": "Parameters to load a PDB entry by ID.",
      "type": "object",
      "properties": {
        "pdbId": {
          "description": "Four-character PDB identifier",
          "type": "string",
          "pattern": "^[A-Za-z0-9]{4}$"
        }
      },
      "required": [
        "pdbId"
      ],
      "additionalProperties": false
    },
    "SetRepresentationParams": {
      "title": "SetRepresentationParams",
      "description": "Parameters to change the visual style of the model.",
      "type": "object",
      "properties": {
        "style": {
          "description": "Representation style for the model",
          "enum": [
            "stick",
            "line",
            "sphere",
            "cartoon",
            "ballAndStick"
          ],
          "type": "string"
        },
        "options": {
          "description": "Style-specific options (radius, scale, etc.)",
          "anyOf": [
            {
              "type": "object"
            },
            {
              "type": "null"
            }
          ]
        },
        "colorScheme": {
          "description": "Coloring scheme (Jmol, ssPyMol, element, etc.)",
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ]
        },
        "opacity": {
          "description": "Opacity value between 0.0 (transparent) and 1.0 (opaque)",
          "anyOf": [
            {
              "type": "number",
              "minimum": 0.0,
              "maximum": 1.0
            },
            {
              "type": "null"
            }
          ]
        }
      },
      "required": [
        "style"
      ],
      "additionalProperties": false
    },
    "SetBackgroundColorParams": {
      "title": "SetBackgroundColorParams",
      "description": "Parameters to change the viewer background color.",
      "type": "object",
      "properties": {
        "color": {
          "description": "CSS color string or hex code (e.g. 'white', '#FF0000')",
          "type": "string"
        }
      },
      "required": [
        "color"
      ],
      "additionalProperties": false
    },
    "TranslateCameraParams": {
      "title": "TranslateCameraParams",
      "description": "Parameters to pan (translate) the camera.",
      "type": "object",
      "properties": {
        "vector": {
          "description": "Translation vector [dx, dy, dz]",
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 3,
          "maxItems": 3
        }
      },
      "required": [
        "vector"
      ],
      "additionalProperties": false
    },
    "ZoomParams": {
      "title": "ZoomParams",
      "description": "Parameters to zoom the camera in or out.",
      "type": "object",
      "properties": {
        "factor": {
          "description": "Zoom factor (>1 = zoom in; <1 = zoom out)",
          "type": "number"
        },
        "fixedPath": {
          "description": "Zoom along fixed path (true) or relative (false)",
          "anyOf": [
            {
              "type": "boolean"
            },
            {
              "type": "null"
            }
          ]
        }
      },
      "required": [
        "factor"
      ],
      "additionalProperties": false
    },
    "ResetViewParams": {
      "title": "ResetViewParams",
      "description": "Parameters to reset the camera to default view.",
      "type": "object",
      "additionalProperties": false
    },
    "ToggleAxesParams": {
      "title": "ToggleAxesParams",
      "description": "Parameters to show or hide coordinate axes.",
      "type": "object",
      "properties": {
        "show": {
          "description": "true to show axes; false to hide",
          "type": "boolean"
        }
      },
      "required": [
        "show"
      ],
      "additionalProperties": false
    },
    "CrystalData": {
      "title": "CrystalData",
      "type": "object",
      "properties": {
        "a": {
          "description": "Cell length a",
          "type": "number"
        },
        "b": {
          "description": "Cell length b",
          "type": "number"
        },
        "c": {
          "description": "Cell length c",
          "type": "number"
        },
        "alpha": {
          "description": "Angle α in degrees",
          "type": "number"
        },
        "beta": {
          "description": "Angle β in degrees",
          "type": "number"
        },
        "gamma": {
          "description": "Angle γ in degrees",
          "type": "number"
        }
      },
      "required": [
        "a",
        "b",
        "c",
        "alpha",
        "beta",
        "gamma"
      ],
      "additionalProperties": false
    },
    "ToggleUnitCellParams": {
      "title": "ToggleUnitCellParams",
      "description": "Parameters to show or hide the crystallographic unit cell.",
      "type": "object",
      "properties": {
        "show": {
          "description": "true to show unit cell; false to hide",
          "type": "boolean"
        },
        "crystalData": {
          "description": "Optional explicit cell parameters",
          "anyOf": [
            {
              "$ref": "#/$defs/CrystalData"
            },
            {
              "type": "null"
            }
          ]
        }
      },
      "required": [
        "show"
      ],
      "additionalProperties": false
    },
    "DisplayMessageParams": {
      "title": "DisplayMessageParams",
      "description": "Parameters to show a chat message in the frontend.",
      "type": "object",
      "properties": {
        "message": {
          "description": "Text to display in the chat pane",
          "type": "string"
        },
        "type": {
          "description": "Severity or style of the message",
          "enum": [
            "info",
            "success",
            "warning",
            "error"
          ],
          "type": "string"
        }
      },
      "required": [
        "message",
        "type"
      ],
      "additionalProperties": false
    }
  }
}
