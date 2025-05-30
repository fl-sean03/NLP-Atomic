# MODULE\_SPEC.md

This document specifies the backend modules, their responsibilities, and their public interfaces (functions, inputs, and outputs). Use this as a reference when implementing each component.

---

## 1. `app.py` (API Layer)

**Responsibilities:**

* Initialize Flask application and configure CORS
* Define and register the `/api/commands` endpoint
* Orchestrate the pipeline: NLP → Validation → Execution
* Handle top‑level exceptions and map them to HTTP responses

**Public Functions / Globals:**

```python
app: Flask  # Flask application instance
```

### Endpoint Handler

```python
def commands_endpoint() -> Response
```

* **Location:** `app.py`
* **Input:**

  * JSON body with:

    * `prompt` (str)
    * optional `context` (List\[dict])
* **Process:**

  1. Parse request JSON
  2. Call `generate_commands(prompt, context)`
  3. Call `validate_commands(raw_commands)`
  4. Call `execute_commands(valid_commands)`
  5. Return `jsonify(executed_commands)`
* **Output:**

  * On success: HTTP 200 + JSON array of executed commands
  * On client error (e.g. validation): HTTP 400/422 + `{ "error": msg }`
  * On NLP upstream error: HTTP 502 + `{ "error": msg }`
  * On server error: HTTP 500 + `{ "error": msg }`

**Notes:**

* Register error handlers via `app.register_error_handler`
* Log incoming requests and durations

---

## 2. `nlp/llm_client.py` (NLP Client)

**Responsibilities:**

* Configure OpenAI API key
* Define function schemas for ChatCompletion
* Construct few‑shot prompt template
* Invoke OpenAI ChatCompletion to get raw command JSON

**Public Functions:**

```python
def generate_commands(
    prompt: str,
    context: Optional[List[dict]] = None
) -> List[dict]
```

* **Input:**

  * `prompt`: user’s natural‑language message
  * `context`: optional history of previous commands (for multi‑turn)
* **Process:**

  1. Build `messages` list:

     * System message (instructions + function definitions)
     * Few‑shot examples
     * User message(s)
  2. Call `openai.ChatCompletion.create(...)`
  3. Extract `choices[0].message.function_call.arguments`
  4. Parse arguments JSON into Python `List[dict]`
* **Output:**

  * List of raw command dicts, e.g.

    ```json
    [{ "command": "buildStructure", "params": { ... } }, ...]
    ```
* **Exceptions:**

  * Raises `NLPError` if API fails or response malformed

---

## 3. `models/commands.py` (Validation Module)

**Responsibilities:**

* Define Pydantic models for every supported command and its `params`
* Validate raw command dicts against these models

**Public Classes & Functions:**

```python
class BuildStructureParams(BaseModel):
    format: Literal["pdb","xyz","sdf","mol2","cif"]
    content: str
    options: Optional[dict]

class RotateCameraParams(BaseModel):
    axis: Union[Literal["x","y","z"], Tuple[float,float,float]]
    angle: float

# ... other Params classes ...

class Command(BaseModel):
    command: Literal[
      "buildStructure", "loadPdb", "setRepresentation",
      "setBackgroundColor", "rotateCamera",
      "translateCamera", "zoom", "resetView",
      "toggleAxes", "toggleUnitCell",
      "setView", "displayMessage"
    ]
    params: Union[
      BuildStructureParams,
      RotateCameraParams,
      # ... other Params classes ...
    ]


def validate_commands(raw: List[dict]) -> List[Command]
```

* **Input:** raw list of dicts from `generate_commands`
* **Process:** loop `Command.parse_obj(item)` for each
* **Output:** list of validated `Command` instances
* **Exceptions:** raises `ValidationError` on mismatch

---

## 4. `executor/structure.py` (Structure Executor)

**Responsibilities:**

* Build atomic structures using ASE
* Return raw file text (PDB/XYZ) for the frontend

**Public Function:**

```python
def build_structure(params: BuildStructureParams) -> str
```

* **Input:**

  * `params.format`: output format
  * `params.content`: ignored on build (raw generation)
  * `params.options`: currently unused
  * Additional fields from `BuildStructureParams` (e.g. lattice, element, nx, ny, nz if extended)
* **Process:**

  1. Create primitive cell: `ase.build.bulk(...)`
  2. Tile supercell: `cell * (nx,ny,nz)`
  3. Write to `io.StringIO()` via `ase.io.write(buffer, supercell, format)`
* **Output:**

  * PDB/XYZ text as Python `str`
* **Exceptions:**

  * Raises `ExecutionError` on ASE failures

---

## 5. `executor/view.py` (View Executor)

**Responsibilities:**

* Compute camera/view parameters for viewer commands

**Public Functions:**

```python
def compute_set_view(face: str) -> dict
```

* **Input:**

  * `face`: one of `"100"`,`"010"`,`"001"`,`"110"`,`"111"`
* **Process:**

  * Map face → normalized view direction
  * Choose appropriate up vector
* **Output:**

  * `viewObject` dict matching 3Dmol.js `viewer.getView()` shape
  * Contains `quaternion`, `translation`, `zoom`

```python
def compute_rotate_camera(
    prev_view: dict,
    axis: Union[str, Tuple[float,float,float]],
    angle: float
) -> dict
```

* **Input:**

  * `prev_view`: existing viewObject
  * `axis`, `angle` from `RotateCameraParams`
* **Process:**

  * Convert axis/angle → rotation quaternion
  * Combine with `prev_view["quaternion"]`
* **Output:**

  * New `viewObject` dict
* **Exceptions:**

  * Raises `ExecutionError` on calculation errors

---

## 6. `utils/file_utils.py` (File Utilities)

**Responsibilities:**

* Helpers for file or buffer management (if switching to file paths)
* Generate unique filenames or in-memory identifiers

**Public Functions:**

```python
def generate_uuid_filename(extension: str) -> str
```

* **Input:** desired file extension (e.g. `".pdb"`)
* **Output:** a string `"<uuid><extension>"`

```python
def write_temp_file(filename: str, content: str) -> str
```

* **Input:** filename and content text
* **Process:** write to disk under `static/models/`
* **Output:** full file path or URL

---

## 7. `utils/error_handlers.py` (Error Handling)

**Responsibilities:**

* Define custom exception classes
* Map exceptions to HTTP status codes and messages

**Public Classes:**

```python
class NLPError(Exception):
    """Raised when the LLM API call fails or returns invalid output."""

class ValidationError(Exception):
    """Raised when command schema validation fails (wraps Pydantic errors)."""

class ExecutionError(Exception):
    """Raised when structure or view execution logic fails."""
```

**Public Function:**

```python
def handle_exception(e: Exception) -> Response
```

* **Input:** any exception
* **Process:**

  * If `NLPError` → HTTP 502
  * If `ValidationError` → HTTP 400 or 422
  * If `ExecutionError` → HTTP 500
  * Else → HTTP 500
* **Output:** Flask `Response` with JSON `{ "error": str(e) }`

---

> **Note:** As the codebase evolves, update this MODULE\_SPEC.md to reflect any new modules or public interfaces. Ensure consistency with **JSON\_SCHEMA.md** and **ARCHITECTURE.md**.
