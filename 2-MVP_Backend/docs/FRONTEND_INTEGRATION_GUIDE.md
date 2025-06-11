# Frontend Integration Guide: NLP-Atomic-Backend

This guide provides frontend developers with all the necessary information to integrate with the NLP-Atomic-Backend. It assumes no prior backend knowledge and aims to be a comprehensive resource for making API calls, understanding expected outputs, and handling various integration scenarios.

## Table of Contents
1. [Overview of the Backend](#1-overview-of-the-backend)
2. [Local Development Setup](#2-local-development-setup)
3. [API Endpoint Usage](#3-api-endpoint-usage)
    - [POST /api/commands](#post-apicommands)
4. [Request Format](#4-request-format)
    - [Headers](#headers)
    - [Request Body Structure](#request-body-structure)
5. [Response Format](#5-response-format)
    - [Success Response (200 OK)](#success-response-200-ok)
    - [Error Responses (4xx / 5xx)](#error-responses-4xx--5xx)
6. [Understanding Command Objects](#6-understanding-command-objects)
    - [Common Command Properties](#common-command-properties)
    - [Detailed Command Parameters](#detailed-command-parameters)
        - [`buildStructure`](#buildstructure)
        - [`loadPdb`](#loadpdb)
        - [`setRepresentation`](#setrepresentation)
        - [`setBackgroundColor`](#setbackgroundcolor)
        - [`rotateCamera`](#rotatecamera)
        - [`translateCamera`](#translatecamera)
        - [`zoom`](#zoom)
        - [`resetView`](#resetview)
        - [`toggleAxes`](#toggleaxes)
        - [`toggleUnitCell`](#toggleunitcell)
        - [`setView`](#setview)
        - [`displayMessage`](#displaymessage)
7. [Full Request-Response Examples](#7-full-request-response-examples)
    - [Example 1: Building and Viewing a Structure](#example-1-building-and-viewing-a-structure)
    - [Example 2: Handling an Unsupported Prompt](#example-2-handling-an-unsupported-prompt)
    - [Example 3: Malformed Request Body](#example-3-malformed-request-body)
8. [Behavioral Notes for Frontend Interaction](#8-behavioral-notes-for-frontend-interaction)

---

## 1. Overview of the Backend

The **NLP-Atomic-Backend** is a stateless Python service designed to process natural language prompts related to 3D atomic structures. Its core purpose is to:

- **Translate natural language**: Convert user prompts (e.g., "build an FCC aluminum cell") into structured JSON commands.
- **Execute commands**: Perform operations like generating 3D atomic structures (using the Atomic Simulation Environment - ASE) and calculating camera/view parameters for visualization.
- **Return commands**: Send an ordered sequence of these executed commands back to the frontend for rendering in a 3D viewer (like 3Dmol.js).

The backend is designed to be fast (targeting sub-3 second responses) and stateless, meaning it doesn't maintain user sessions. All necessary context for a request must be provided by the frontend.

---

## 2. Local Development Setup

To set up the backend for local testing and development:

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-org/nlp-atomic-backend.git
    cd nlp-atomic-backend/2-MVP_Backend
    ```

2.  **Create and activate a Python virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    Key dependencies include `flask` (for the API), `openai` (for LLM interaction), `ase` (for structure generation), and `pydantic` (for data validation).

4.  **Set up OpenAI API Key**:
    The backend requires an OpenAI API key to function.
    ```bash
    cp .env.example .env
    ```
    Open the newly created `.env` file and replace `your_openai_api_key_here` with your actual OpenAI API key. This file is ignored by Git for security.

5.  **Run the Flask application**:
    ```bash
    export FLASK_APP=app.py
    export FLASK_ENV=development # Enables debug mode
    flask run
    ```
    (On Windows, use `set FLASK_APP=app.py` and `set FLASK_ENV=development`).
    The API will typically be accessible at `http://localhost:5000`.

---

## 3. API Endpoint Usage

The backend exposes a single API endpoint for all interactions:

### `POST /api/commands`

This endpoint is used to send a natural language prompt to the backend. The backend will process the prompt, generate and execute relevant commands, and return a list of structured command objects for the frontend to interpret and execute.

| Method | Path            | Description                               |
| :----- | :-------------- | :---------------------------------------- |
| `POST` | `/api/commands` | Processes a natural language prompt and returns a sequence of JSON commands. |

---

## 4. Request Format

All requests to `/api/commands` must be `POST` requests with a JSON body.

### Headers
- `Content-Type: application/json`
- **Authentication**: For V1, no authentication is required. In future versions, an `Authorization: Bearer <token>` header might be necessary.

### Request Body Structure

The request body is a JSON object with the following fields:

| Field   | Type   | Required | Description                                |
| :------ | :----- | :------- | :----------------------------------------- |
| `prompt`  | `string` | Yes      | The user's natural language instruction (e.g., "build a diamond silicon structure"). |
| `context` | `array`  | No       | An optional array of previously executed command objects. This is used for multi-turn conversations where the current prompt depends on prior actions. |

**Example Request Body:**

```json
{
  "prompt": "Build a 3x3x3 FCC Al cell and look down the 111 direction."
}
```

**Example Request Body with Context (for multi-turn interactions):**

```json
{
  "prompt": "Now rotate it by 90 degrees around the x-axis.",
  "context": [
    {
      "command": "buildStructure",
      "params": {
        "element": "Al",
        "lattice": "fcc",
        "nx": 3,
        "ny": 3,
        "nz": 3,
        "format": "pdb"
      }
    },
    {
      "command": "setView",
      "params": {
        "viewObject": {
          "quaternion": { "x":0.7,"y":0.7,"z":0,"w":0 },
          "translation": { "x":0,"y":0,"z":0 },
          "zoom": 1.1
        }
      }
    }
  ]
}
```

---

## 5. Response Format

The backend responds with either a success (HTTP 200 OK) or an error (HTTP 4xx/5xx) response.

### Success Response (200 OK)

Upon successful processing, the API returns an HTTP `200 OK` status with a JSON array of command objects in the response body. The frontend should iterate through this array and execute each command in the order they appear.

- **Content-Type**: `application/json`
- **Body**: A JSON array of command objects.

**Example Success Response Body:**

```json
[
  {
    "command": "buildStructure",
    "params": {
      "format": "pdb",
      "content": "ATOM      1  Al  ..."
    }
  },
  {
    "command": "setView",
    "params": {
      "viewObject": {
        "quaternion": { "x":0.7,"y":0.7,"z":0,"w":0 },
        "translation": { "x":0,"y":0,"z":0 },
        "zoom": 1.1
      }
    }
  }
]
```

### Error Responses (4xx / 5xx)

For protocol or system failures, the API returns an appropriate HTTP error status code (4xx or 5xx) with a JSON object containing an `error` field.

| Status Code | Meaning                                   |
| :---------- | :---------------------------------------- |
| `400 Bad Request`         | The request body is malformed (e.g., not valid JSON, missing `prompt` field). |
| `422 Unprocessable Entity` | The backend's internal validation failed for the commands generated by the LLM. This means the LLM produced commands that don't conform to the expected schema. |
| `500 Internal Server Error` | An unexpected error occurred during backend processing (e.g., an unhandled exception during NLP processing, command execution). |
| `502 Bad Gateway`         | The backend failed to communicate with an external service, such as the LLM (OpenAI). |

**Example Error Response Body (400 Bad Request):**

```json
{
  "error": "Request body must be valid JSON with a 'prompt' field."
}
```

**Important Note on `displayMessage` vs. HTTP Errors:**
If the backend understands the prompt but cannot fulfill it (e.g., "Show me graphene structure" when only FCC, BCC, SC are supported), it will return a `200 OK` response containing a `displayMessage` command. This allows the frontend to show an inline, user-friendly error message within the chat interface, rather than a generic HTTP error. Reserve HTTP errors for true system or protocol failures.

---

## 6. Understanding Command Objects

The core of the backend's response is an array of "command objects." Each object instructs the frontend 3D viewer to perform a specific action.

### Common Command Properties

Every command object has two primary properties:

| Property | Type   | Description                                    |
| :------- | :----- | :--------------------------------------------- |
| `command`  | `string` | The name of the command to execute (e.g., `buildStructure`, `rotateCamera`). |
| `params`   | `object` | An object containing parameters specific to the `command`. The structure of `params` varies for each command. |

### Detailed Command Parameters

Here's a breakdown of each supported command and its expected `params` structure. These are derived from the backend's JSON Schema definitions.

#### `buildStructure`
**Description**: Builds a new atomic structure and provides its data.
**Parameters**:
- `element` (string, **required**): Chemical symbol (e.g., "Al", "Fe").
- `lattice` (string, **required**): Lattice type (e.g., "fcc", "bcc", "hcp").
- `nx`, `ny`, `nz` (integer, optional, default: 1): Supercell dimensions along x, y, z axes.
- `a` (number, optional): Lattice constant in Angstroms. If not provided, a default for the element/lattice will be used.
- `format` (string, optional, default: "pdb"): Output file format for the structure data (`"pdb"`, `"xyz"`, `"cif"`).

**Example `params`**:
```json
{
  "element": "Al",
  "lattice": "fcc",
  "nx": 3,
  "ny": 3,
  "nz": 3,
  "format": "pdb"
}
```

#### `loadPdb`
**Description**: Loads a PDB entry by its ID.
**Parameters**:
- `pdbId` (string, **required**): Four-character PDB identifier (e.g., "1CRN").

**Example `params`**:
```json
{
  "pdbId": "1CRN"
}
```

#### `setRepresentation`
**Description**: Changes the visual style of the model.
**Parameters**:
- `style` (string, **required**): Representation style (`"stick"`, `"line"`, `"sphere"`, `"cartoon"`, `"ballAndStick"`).
- `options` (object, optional): Style-specific options (e.g., `{"radius": 0.5}` for `stick` style).
- `colorScheme` (string, optional): Coloring scheme (e.g., `"Jmol"`, `"ssPyMol"`, `"element"`).
- `opacity` (number, optional): Opacity value between `0.0` (transparent) and `1.0` (opaque).

**Example `params`**:
```json
{
  "style": "ballAndStick",
  "colorScheme": "element",
  "opacity": 0.8
}
```

#### `setBackgroundColor`
**Description**: Changes the viewer background color.
**Parameters**:
- `color` (string, **required**): CSS color string or hex code (e.g., `"white"`, `"#FF0000"`).

**Example `params`**:
```json
{
  "color": "lightblue"
}
```

#### `rotateCamera`
**Description**: Rotates the camera around a specified axis.
**Parameters**:
- `axis` (string or array, **required**): Principal axis name (`"x"`, `"y"`, `"z"`) or a custom axis vector `[x, y, z]`.
- `angle` (number, **required**): Rotation angle in degrees.

**Example `params`**:
```json
{
  "axis": "y",
  "angle": 90
}
```

#### `translateCamera`
**Description**: Pans (translates) the camera.
**Parameters**:
- `vector` (array of numbers, **required**): Translation vector `[dx, dy, dz]`.

**Example `params`**:
```json
{
  "vector": [10, 0, 0]
}
```

#### `zoom`
**Description**: Zooms the camera in or out.
**Parameters**:
- `factor` (number, **required**): Zoom factor (`>1` zooms in; `<1` zooms out).
- `fixedPath` (boolean, optional): `true` to zoom along a fixed path; `false` for relative zoom.

**Example `params`**:
```json
{
  "factor": 1.5
}
```

#### `resetView`
**Description**: Resets the camera to its default view.
**Parameters**: None.

**Example `params`**:
```json
{}
```

#### `toggleAxes`
**Description**: Shows or hides coordinate axes.
**Parameters**:
- `show` (boolean, **required**): `true` to show axes; `false` to hide.

**Example `params`**:
```json
{
  "show": true
}
```

#### `toggleUnitCell`
**Description**: Shows or hides the crystallographic unit cell.
**Parameters**:
- `show` (boolean, **required**): `true` to show unit cell; `false` to hide.
- `crystalData` (object, optional): Explicit cell parameters if needed (e.g., `{"a": 10, "b": 10, "c": 10, "alpha": 90, "beta": 90, "gamma": 90}`).

**Example `params`**:
```json
{
  "show": true
}
```

#### `setView`
**Description**: Restores a saved camera view using a 3Dmol.js view state object.
**Parameters**:
- `viewObject` (object, **required**): A 3Dmol.js view state object containing `quaternion`, `translation`, and `zoom`.

**Example `params`**:
```json
{
  "viewObject": {
    "quaternion": { "x":0.7,"y":0.7,"z":0,"w":0 },
    "translation": { "x":0,"y":0,"z":0 },
    "zoom": 1.1
  }
}
```

#### `displayMessage`
**Description**: Displays a chat message in the frontend. This is used for user-friendly feedback, especially for prompts the backend understands but cannot fully process.
**Parameters**:
- `message` (string, **required**): The text to display in the chat pane.
- `type` (string, **required**): Severity or style of the message (`"info"`, `"success"`, `"warning"`, `"error"`).

**Example `params`**:
```json
{
  "message": "Unsupported lattice type: graphene. Only FCC, BCC, SC supported.",
  "type": "error"
}
```

---

## 7. Full Request-Response Examples

Here are some common scenarios demonstrating the full request-response cycle.

### Example 1: Building and Viewing a Structure

**Scenario**: User asks to build an FCC Aluminum cell and view it from a specific direction.

**Request**:
```http
POST /api/commands
Content-Type: application/json

{ "prompt": "Build a 3x3x3 FCC Al cell and look down the 111 direction." }
```

**Response (200 OK)**:
```json
[
  {
    "command": "buildStructure",
    "params": {
      "element": "Al",
      "lattice": "fcc",
      "nx": 3,
      "ny": 3,
      "nz": 3,
      "format": "pdb",
      "content": "HEADER    3x3x3 FCC Al cell\nREMARK    Generated by ASE\nATOM      1  Al  AL  1       0.000   0.000   0.000  1.00  0.00           Al\n..."
    }
  },
  {
    "command": "setView",
    "params": {
      "viewObject": {
        "quaternion": { "x":0.7,"y":0.7,"z":0,"w":0 },
        "translation": { "x":0,"y":0,"z":0 },
        "zoom": 1.1
      }
    }
  }
]
```
*Frontend Action*: First, render the PDB content from `buildStructure`. Then, apply the camera `viewObject` from `setView` to orient the view.

### Example 2: Handling an Unsupported Prompt

**Scenario**: User asks for a structure type not currently supported by the backend.

**Request**:
```http
POST /api/commands
Content-Type: application/json

{ "prompt": "Show me graphene structure." }
```

**Response (200 OK)**:
```json
[
  {
    "command": "displayMessage",
    "params": {
      "message": "Unsupported lattice type: graphene. Only FCC, BCC, SC supported.",
      "type": "error"
    }
  }
]
```
*Frontend Action*: Display the `message` content in the chat interface, styled as an error. No 3D model changes occur.

### Example 3: Malformed Request Body

**Scenario**: Frontend sends an invalid JSON request (e.g., missing the `prompt` field).

**Request**:
```http
POST /api/commands
Content-Type: application/json

{ "user_input": "Build a structure." }
```

**Response (400 Bad Request)**:
```json
{
  "error": "Request body must be valid JSON with a 'prompt' field."
}
```
*Frontend Action*: Handle this as a standard HTTP error, potentially logging it or showing a generic "something went wrong" message to the user.

---

## 8. Behavioral Notes for Frontend Interaction

-   **Statelessness**: Each request to `/api/commands` is independent. The backend does not remember previous interactions. If a command relies on prior context (e.g., "rotate *it*"), the frontend must explicitly pass that context in the `context` array of the request body.
-   **Command Ordering**: The array of command objects returned in a successful response is ordered. The frontend **must** execute these commands sequentially to achieve the intended visual state.
-   **Idempotency**: Many commands (like `setBackgroundColor`, `setView`, `toggleAxes`) are idempotent, meaning they can be applied multiple times without unintended side effects. Applying `setView` multiple times with the same `viewObject` will simply maintain that view.
-   **`displayMessage` vs. HTTP Errors**: As noted above, `displayMessage` commands are for user-level feedback when the prompt is understood but cannot be fulfilled. HTTP errors (4xx/5xx) are reserved for fundamental issues like malformed requests, internal server problems, or external service failures. Frontend should differentiate between these two types of responses for appropriate user feedback.
-   **Performance**: The backend aims for sub-3 second response times. Frontend should implement appropriate loading indicators or timeouts for API calls.
