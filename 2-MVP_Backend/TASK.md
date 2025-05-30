
# TASK.md

> **Audience:** Junior backend engineer  
> **Purpose:** A step-by-step, granular checklist to implement the entire backend MVP. Reference the spec documents as you go—PLANNING.md, API_SPEC.md, JSON_SCHEMA.md, ARCHITECTURE.md, MODULE_SPEC.md.

---

## Phase 1: Repository & Environment Setup

- [ ] **Clone the repo & create branch**  
  - `git clone https://github.com/your-org/nlp-atomic-backend.git`  
  - `cd nlp-atomic-backend`  
  - `git checkout -b phase1/env-setup`  

- [ ] **Create Python virtual environment**  
  - `python3 -m venv venv`  
  - `source venv/bin/activate`  

- [ ] **Initialize requirements**  
  - Create `requirements.txt` with:  
    ```
    flask
    flask-cors
    openai
    ase
    pydantic
    pytest
    ```
  - Run `pip install -r requirements.txt`  

- [ ] **Create config file**  
  - Add `config.py` with placeholders for:  
    ```python
    import os
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ```
  - Document environment variables in README.

- [ ] **Set up basic logging**  
  - In `utils/logging.py`, configure Python `logging` at INFO level.  
  - Ensure all modules import and use this logger.

- [ ] **Commit & push**  
  - `git add .` → `git commit -m "Setup project scaffold and environment"` → `git push --set-upstream origin phase1/env-setup`

---

## Phase 2: API Skeleton & Hello World Endpoint

- [ ] **Create `app.py`**  
  - Import Flask and CORS.  
  - Instantiate `app = Flask(__name__)`; enable `CORS(app)`.

- [ ] **Define `/api/commands` stub**  
  ```python
  @app.route("/api/commands", methods=["POST"])
  def commands():
      data = request.json
      return jsonify([]), 200


* [ ] **Run & Smoke-test**

  * `flask run`
  * `curl -X POST http://localhost:5000/api/commands -d '{"prompt":"test"}' -H "Content-Type:application/json"`
  * Expect `[]`.

* [ ] **Reference API spec**

  * Read `/docs/API_SPEC.md` (skeleton) for full request/response format.

* [ ] **Commit & push**

  * `git commit -am "Add Flask skeleton and commands stub endpoint"`

---

## Phase 3: NLP Client & Command Generation

* [ ] **Create `nlp/llm_client.py`**

  * Import `openai` and `config.OPENAI_API_KEY`.
  * Set `openai.api_key`.

* [ ] **Define function schemas**

  * In `nlp/llm_client.py`, list OpenAI function definitions for:

    * `buildStructure`
    * `rotateCamera`
    * `setView`
  * Reference JSON\_SCHEMA.md for parameter shapes.

* [ ] **Write `generate_commands(prompt: str) -> List[dict]`**

  * Build messages array:

    1. System prompt with role and JSON output requirement.
    2. Few-shot examples from MODULE\_SPEC.md.
    3. User prompt.
  * Call `openai.ChatCompletion.create(model="gpt-4-0613", functions=..., ...)`.
  * Extract `.choices[0].message.function_call.arguments` as JSON.

* [ ] **Basic CLI test**

  * Add `if __name__ == "__main__":` block to call `generate_commands("3x3x3 FCC Al")` and `print()` result.
  * Run `python nlp/llm_client.py` and inspect output.

* [ ] **Error fallback**

  * If LLM returns non-JSON or missing function\_call, raise a custom `NLPError`.

* [ ] **Commit & push**

  * `git commit -am "Implement NLP client and generate_commands()"`

---

## Phase 4: Schema & Validation

* [ ] **Create `models/commands.py`**

  * Define Pydantic models:

    * `BuildStructureParams`
    * `RotateCameraParams`
    * `SetViewParams`
    * `Command` union type (see JSON\_SCHEMA.md).

* [ ] **Implement `validate_commands(raw: List[dict]) -> List[Command]`**

  * Loop `Command.parse_obj(item)`; collect or raise `ValidationError`.

* [ ] **Unit tests for validation**

  * In `tests/test_models.py`:

    * Test valid command JSON (should parse).
    * Test missing field / wrong type (should raise).

* [ ] **Reference JSON\_SCHEMA.md**

  * Ensure your Pydantic models match the documented schemas exactly.

* [ ] **Commit & push**

  * `git commit -am "Add Pydantic command schemas and validation"`

---

## Phase 5: Executor Modules

### 5.1 Structure Executor

* [ ] **Create `executor/structure.py`**

  * Function `build_structure(params: BuildStructureParams) -> str`:

    1. `cell = bulk(params.element, params.lattice, a=1.0)`
    2. `supercell = cell * (nx, ny, nz)`
    3. Write to `io.StringIO()` via `ase.io.write()`
    4. Return `.getvalue()` text.

* [ ] **Unit tests for structure**

  * In `tests/test_structure.py`:

    * Verify `build_structure(...)` returns text containing correct number of ATOM records (`nx*ny*nz*1`).

### 5.2 View Executor

* [ ] **Create `executor/view.py`**

  * Function `compute_set_view(face: str) -> dict` for presets 100, 010, 001, 110, 111:

    * Normalize vector, choose up vector.
    * Return a `viewObject` matching 3Dmol.js shape.

  * Function `compute_rotate_camera(prev_view: dict, axis, angle) -> dict`:

    * Apply rotation quaternion or matrix to existing `viewObject`.

* [ ] **Unit tests for view**

  * In `tests/test_view.py`:

    * Test each preset face returns plausible `viewObject`.
    * Test rotate\_camera returns modified orientation.

* [ ] **Reference MODULE\_SPEC.md**

  * Confirm function signatures and return structures.

* [ ] **Commit & push**

  * `git commit -am "Implement executor modules for structure and view"`

---

## Phase 6: Pipeline Integration & Error Handling

* [ ] **Update `app.py` to import modules**

  * `from nlp.llm_client import generate_commands`
  * `from models.commands import validate_commands`
  * `from executor.structure import build_structure`
  * `from executor.view import compute_set_view, compute_rotate_camera`

* [ ] **Implement `/api/commands` handler logic**

  1. Parse JSON body for `prompt`.

  2. Call `raw_cmds = generate_commands(prompt)`.

  3. Validate: `cmds = validate_commands(raw_cmds)`.

  4. Initialize `executed: List[dict] = []`.

  5. For each `cmd` in `cmds`:

     * If `cmd.command == "buildStructure"`:

       * `content = build_structure(cmd.params)`
       * `executed.append({"command":"buildStructure","params":{"format":"pdb","content":content}})`
     * Elif `cmd.command == "presetView"`:

       * `view = compute_set_view(cmd.params.face)`
       * Append `{"command":"setView","params":{"viewObject":view}}`
     * Elif `cmd.command == "rotateCamera"`:

       * `view = compute_rotate_camera(prev_view, cmd.params.axis, cmd.params.angle)`
       * Append `{"command":"setView","params":{"viewObject":view}}`
     * Else: propagate other view commands similarly.

  6. Return `jsonify(executed)`.

* [ ] **Global error handler**

  * Wrap handler in `try/except` catching:

    * `NLPError` → HTTP 502 + `{ error: msg }`
    * `ValidationError` → HTTP 400 + `{ error: msg }`
    * `ExecutionError` → HTTP 500 + `{ error: msg }`
    * Generic → HTTP 500.

* [ ] **Reference API\_SPEC.md & ERROR\_HANDLING.md**

  * Ensure handler matches documented request/response and error codes.

* [ ] **Commit & push**

  * `git commit -am "Integrate NLP → validation → executor pipeline in app.py with error handling"`

---

## Phase 7: Testing & Performance Tuning

* [ ] **Integration tests**

  * In `tests/test_api.py` using Flask’s test client:

    * Valid prompt → `200 OK`, valid command list.
    * Invalid prompt → `200 OK` with `displayMessage` or `400` for schema error.
    * LLM down → simulate API error → `502`.

* [ ] **Benchmark timing**

  * Add a decorator in `app.py` to log request duration.
  * Run `pytest --durations=10` or manual tests to confirm <3s.

* [ ] **Fix performance issues**

  * Cache repeated LLM function definitions if needed.
  * Optimize ASE call for small supercells.

* [ ] **Commit & push**

  * `git commit -am "Add integration tests and performance logging"`

---

## Phase 8: Documentation & Handoff

* [ ] **Generate API spec**

  * Complete `/docs/API_SPEC.md` with request/response examples.

* [ ] **Publish JSON schemas**

  * Populate `/docs/JSON_SCHEMA.md` from Pydantic models.

* [ ] **Draw architecture diagram**

  * In `/docs/ARCHITECTURE.md`, embed Mermaid flowchart.

* [ ] **Detail module interfaces**

  * Fill `/docs/MODULE_SPEC.md` with function signatures and descriptions.

* [ ] **Update README**

  * Add setup instructions, environment variables, how to run tests.

* [ ] **Commit & push**

  * `git commit -am "Finalize documentation for backend V1"`

---

## Phase 8.5: End-to-End Backend Testing

* [x] **Run Flask app locally**
  * `export FLASK_APP=app.py`
  * `export FLASK_ENV=development`
  * `flask run` (run in a separate terminal)

* [x] **Perform end-to-end curl tests**
  * Test valid prompt for structure generation:
    `curl -X POST http://localhost:5000/api/commands -d '{"prompt":"build a 2x2x2 FCC aluminum crystal"}' -H "Content-Type:application/json"`
    * Expect `200 OK` and a JSON response containing PDB/XYZ content.
  * Test valid prompt for camera rotation:
    `curl -X POST http://localhost:5000/api/commands -d '{"prompt":"rotate the camera 90 degrees around the y-axis"}' -H "Content-Type:application/json"`
    * Expect `200 OK` and a JSON response containing view object.
  * Test invalid prompt (e.g., unrecognized command):
    `curl -X POST http://localhost:5000/api/commands -d '{"prompt":"do something weird"}' -H "Content-Type:application/json"`
    * Expect `400 Bad Request` or `502 Bad Gateway` (depending on LLM response) and an error message.
  * Test invalid command parameters (e.g., missing required field):
    `curl -X POST http://localhost:5000/api/commands -d '{"prompt":"build a crystal"}' -H "Content-Type:application/json"`
    * Expect `400 Bad Request` and a validation error message.

* [x] **Verify expected outputs**
  * Confirm HTTP status codes and JSON response structures match expectations from `API_SPEC.md` and `ERROR_HANDLING.md`.

* [x] **Commit & push**
  * `git commit -am "Add end-to-end backend testing phase"`

---

## Phase 9: CI/CD & Deployment Prep

* [ ] **Add GitHub Actions**

  * `.github/workflows/ci.yml` to run lint (`flake8`), format check (`black --check`), tests (`pytest`).

* [ ] **Dockerfile (optional)**

  * Create `Dockerfile` for containerizing the service.

* [ ] **Environment variables**

  * Document in `.env.example`: `OPENAI_API_KEY`.

* [ ] **Commit & push**

  * `git commit -am "Add CI workflow and Dockerfile"`

---

## Phase 10: Final Review & Release

* [ ] **Code review & merge PR**
* [ ] **Tag release**

  * `git tag v1.0.0 && git push --tags`
* [ ] **Announce readiness**

  * Notify frontend team to switch from mock to real `/api/commands`.
* [ ] **Monitor logs**

  * Ensure no unexpected errors in staging.

---

## References & Further Reading

* **PLANNING.md**: high-level strategy & roadmap
* **API\_SPEC.md**: endpoint definitions & examples
* **JSON\_SCHEMA.md**: command & params schemas
* **ARCHITECTURE.md**: module/data-flow diagrams
* **MODULE\_SPEC.md**: detailed module/interface specs
* **ERROR\_HANDLING.md**: mapping exceptions to HTTP responses


