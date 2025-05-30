````markdown
# JSON_SCHEMA.md

This document provides the full JSON Schema definitions for every supported command and its `params` object. Use this as the authoritative source when validating incoming or outgoing command JSON.

---

## Top-Level Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CommandsArray",
  "description": "An ordered list of commands for the 3D viewer to execute",
  "type": "array",
  "items": { "$ref": "#/definitions/Command" },
  "definitions": { /* see below */ }
}
````

---

## Definitions

### `Command`

A single command object. Must have a `command` name and a `params` object matching that command.

```json
"Command": {
  "type": "object",
  "description": "A single instruction for the frontend viewer",
  "properties": {
    "command": {
      "type": "string",
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
      ]
    },
    "params": {
      "type": "object",
      "description": "Parameters for the specific command"
    }
  },
  "required": ["command", "params"],
  "allOf": [
    {
      "if": { "properties": { "command": { "const": "buildStructure" } } },
      "then": { "properties": { "params": { "$ref": "#/definitions/BuildStructureParams" } } }
    },
    {
      "if": { "properties": { "command": { "const": "loadPdb" } } },
      "then": { "properties": { "params": { "$ref": "#/definitions/LoadPdbParams" } } }
    },
    {
      "if": { "properties": { "command": { "const": "setRepresentation" } } },
      "then": { "properties": { "params": { "$ref": "#/definitions/SetRepresentationParams" } } }
    },
    {
      "if": { "properties": { "command": { "const": "setBackgroundColor" } } },
      "then": { "properties": { "params": { "$ref": "#/definitions/SetBackgroundColorParams" } } }
    },
    {
      "if": { "properties": { "command": { "const": "rotateCamera" } } },
      "then": { "properties": { "params": { "$ref": "#/definitions/RotateCameraParams" } } }
    },
    {
      "if": { "properties": { "command": { "const": "translateCamera" } } },
      "then": { "properties": { "params": { "$ref": "#/definitions/TranslateCameraParams" } } }
    },
    {
      "if": { "properties": { "command": { "const": "zoom" } } },
      "then": { "properties": { "params": { "$ref": "#/definitions/ZoomParams" } } }
    },
    {
      "if": { "properties": { "command": { "const": "resetView" } } },
      "then": { "properties": { "params": { "$ref": "#/definitions/ResetViewParams" } } }
    },
    {
      "if": { "properties": { "command": { "const": "toggleAxes" } } },
      "then": { "properties": { "params": { "$ref": "#/definitions/ToggleAxesParams" } } }
    },
    {
      "if": { "properties": { "command": { "const": "toggleUnitCell" } } },
      "then": { "properties": { "params": { "$ref": "#/definitions/ToggleUnitCellParams" } } }
    },
    {
      "if": { "properties": { "command": { "const": "setView" } } },
      "then": { "properties": { "params": { "$ref": "#/definitions/SetViewParams" } } }
    },
    {
      "if": { "properties": { "command": { "const": "displayMessage" } } },
      "then": { "properties": { "params": { "$ref": "#/definitions/DisplayMessageParams" } } }
    }
  ]
}
```

---

### `BuildStructureParams`

```json
"BuildStructureParams": {
  "type": "object",
  "description": "Parameters to build a new atomic structure from raw file text",
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
      "additionalProperties": true
    }
  },
  "required": ["format", "content"],
  "additionalProperties": false
}
```

---

### `LoadPdbParams`

```json
"LoadPdbParams": {
  "type": "object",
  "description": "Parameters to load a PDB entry by ID",
  "properties": {
    "pdbId": {
      "type": "string",
      "description": "Four-character PDB identifier",
      "pattern": "^[A-Za-z0-9]{4}$"
    }
  },
  "required": ["pdbId"],
  "additionalProperties": false
}
```

---

### `SetRepresentationParams`

```json
"SetRepresentationParams": {
  "type": "object",
  "description": "Parameters to change the visual style of the model",
  "properties": {
    "style": {
      "type": "string",
      "description": "Representation style for the model",
      "enum": ["stick", "line", "sphere", "cartoon", "ballAndStick"]
    },
    "options": {
      "type": "object",
      "description": "Style-specific options (radius, scale, etc.)",
      "additionalProperties": true
    },
    "colorScheme": {
      "type": "string",
      "description": "Coloring scheme (Jmol, ssPyMol, element, etc.)"
    },
    "opacity": {
      "type": "number",
      "description": "Opacity value between 0.0 (transparent) and 1.0 (opaque)",
      "minimum": 0,
      "maximum": 1
    }
  },
  "required": ["style"],
  "additionalProperties": false
}
```

---

### `SetBackgroundColorParams`

```json
"SetBackgroundColorParams": {
  "type": "object",
  "description": "Parameters to change the viewer background color",
  "properties": {
    "color": {
      "type": "string",
      "description": "CSS color string or hex code (e.g. 'white', '#FF0000')"
    }
  },
  "required": ["color"],
  "additionalProperties": false
}
```

---

### `RotateCameraParams`

```json
"RotateCameraParams": {
  "type": "object",
  "description": "Parameters to rotate the camera around an axis",
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
          "items": { "type": "number" },
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
  "required": ["axis", "angle"],
  "additionalProperties": false
}
```

---

### `TranslateCameraParams`

```json
"TranslateCameraParams": {
  "type": "object",
  "description": "Parameters to pan (translate) the camera",
  "properties": {
    "vector": {
      "type": "array",
      "description": "Translation vector [dx, dy, dz]",
      "items": { "type": "number" },
      "minItems": 3,
      "maxItems": 3
    }
  },
  "required": ["vector"],
  "additionalProperties": false
}
```

---

### `ZoomParams`

```json
"ZoomParams": {
  "type": "object",
  "description": "Parameters to zoom the camera in or out",
  "properties": {
    "factor": {
      "type": "number",
      "description": "Zoom factor (>1 = zoom in; <1 = zoom out)"
    },
    "fixedPath": {
      "type": "boolean",
      "description": "Zoom along fixed path (true) or relative (false)"
    }
  },
  "required": ["factor"],
  "additionalProperties": false
}
```

---

### `ResetViewParams`

```json
"ResetViewParams": {
  "type": "object",
  "description": "Parameters to reset the camera to default view",
  "properties": {},
  "additionalProperties": false
}
```

---

### `ToggleAxesParams`

```json
"ToggleAxesParams": {
  "type": "object",
  "description": "Parameters to show or hide coordinate axes",
  "properties": {
    "show": {
      "type": "boolean",
      "description": "true to show axes; false to hide"
    }
  },
  "required": ["show"],
  "additionalProperties": false
}
```

---

### `ToggleUnitCellParams`

```json
"ToggleUnitCellParams": {
  "type": "object",
  "description": "Parameters to show or hide the crystallographic unit cell",
  "properties": {
    "show": {
      "type": "boolean",
      "description": "true to show unit cell; false to hide"
    },
    "crystalData": {
      "type": "object",
      "description": "Optional explicit cell parameters",
      "properties": {
        "a": { "type": "number", "description": "Cell length a" },
        "b": { "type": "number", "description": "Cell length b" },
        "c": { "type": "number", "description": "Cell length c" },
        "alpha": { "type": "number", "description": "Angle α in degrees" },
        "beta": { "type": "number", "description": "Angle β in degrees" },
        "gamma": { "type": "number", "description": "Angle γ in degrees" }
      },
      "required": ["a","b","c","alpha","beta","gamma"],
      "additionalProperties": false
    }
  },
  "required": ["show"],
  "additionalProperties": false
}
```

---

### `SetViewParams`

```json
"SetViewParams": {
  "type": "object",
  "description": "Parameters to restore a saved camera view",
  "properties": {
    "viewObject": {
      "type": "object",
      "description": "3Dmol.js view state object",
      "properties": {
        "quaternion": {
          "type": "object",
          "description": "Rotation quaternion",
          "properties": {
            "x": { "type": "number" },
            "y": { "type": "number" },
            "z": { "type": "number" },
            "w": { "type": "number" }
          },
          "required": ["x","y","z","w"],
          "additionalProperties": false
        },
        "translation": {
          "type": "object",
          "description": "Camera translation vector",
          "properties": {
            "x": { "type": "number" },
            "y": { "type": "number" },
            "z": { "type": "number" }
          },
          "required": ["x","y","z"],
          "additionalProperties": false
        },
        "zoom": {
          "type": "number",
          "description": "Camera zoom level"
        }
      },
      "required": ["quaternion","translation","zoom"],
      "additionalProperties": false
    }
  },
  "required": ["viewObject"],
  "additionalProperties": false
}
```

---

### `DisplayMessageParams`

```json
"DisplayMessageParams": {
  "type": "object",
  "description": "Parameters to show a chat message in the frontend",
  "properties": {
    "message": {
      "type": "string",
      "description": "Text to display in the chat pane"
    },
    "type": {
      "type": "string",
      "description": "Severity or style of the message",
      "enum": ["info", "success", "warning", "error"]
    }
  },
  "required": ["message","type"],
  "additionalProperties": false
}
```

---

> **Note:** Any additional commands introduced in future versions must be added to the `Command` enum and have a corresponding `Params` definition in this file. Always keep **JSON\_SCHEMA.md** and **MODULE\_SPEC.md** in sync.
