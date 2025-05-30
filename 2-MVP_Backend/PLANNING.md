# PLANNING.md

## 1. Project Overview  
- **Project Name:** NLP-Atomic-Backend  
- **Description:**  
  A stateless, Python-based service that powers our NLP-driven 3D atomic-structure viewer. It accepts natural-language prompts, invokes an LLM to generate structured JSON commands, executes those commands (structure generation and camera/view calculations), and returns the command sequence to the frontend for visualization.  

- **Objective:**  
  Deliver a robust V1 backend MVP that:  
  1. Exposes a single `POST /api/commands` endpoint.  
  2. Translates arbitrary chat prompts into validated command objects.  
  3. Executes “buildStructure” via ASE and camera/view commands.  
  4. Returns raw model data and view parameters within 3 s.  
  5. Provides thorough documentation and a clear extension path.

---

## 2. Vision & Objectives  
- **Vision Statement:**  
  Enable conversational materials design by abstracting all heavy-lifting—language parsing, model building, view math—into a backend service. Frontend teams focus solely on rendering; backend teams focus on generative intelligence, computation, and reliability.

- **Key Objectives (V1):**  
  1. **NLP → JSON commands:** Few-shot, function-calling integration with OpenAI to output exactly the commands our viewer needs.  
  2. **Validation:** Rigorous schema enforcement (Pydantic/JSON-Schema) to catch errors early.  
  3. **Execution:**  
     - **`buildStructure`**: use ASE to produce PDB or XYZ text for cubic lattices.  
     - **Camera/View ops**: compute and return full `viewObject` or axis/angle.  
  4. **Statelessness & Performance:** No user sessions; target sub-3 s end-to-end.  
  5. **Documentation:** Complete set of spec docs—API, command schemas, architecture, module specs—for seamless hand-off and future extension.

---

## 3. Architecture Overview  

### Core Components  
1. **API Layer** (`app.py`)  
   - Single endpoint `POST /api/commands`.  
   - CORS, request parsing, error wrapping.

2. **NLP Client** (`nlp/llm_client.py`)  
   - OpenAI ChatCompletion with function schemas.  
   - Few-shot examples to anchor JSON format.

3. **Validation Module** (`models/commands.py`)  
   - Pydantic models for every `command` + `params` shape.  
   - Ensures only allowed commands pass through.

4. **Executor Module**  
   - **Structure Executor** (`executor/structure.py`): ASE routines for `buildStructure`.  
   - **View Executor** (`executor/view.py`): compute `setView`, `rotateCamera`, etc.

5. **Utilities** (`utils/`)  
   - File/text handling, unique IDs, error classes, logging setup.

6. **Static/File Serving**  
   - Decide between returning raw text vs. hosting files; V1 returns raw content.

### Deliverable Documents  
- **PLANNING.md** (this file)  
- **TASK.md** (detailed implementation steps)  
- **API_SPEC.md** (endpoint definitions, example requests/responses)  
- **JSON_SCHEMA.md** (complete command/params schemas)  
- **ARCHITECTURE.md** (detailed diagrams & data-flow)  
- **MODULE_SPEC.md** (module-by-module interface definitions)

### Technology Stack  
- **Language:** Python 3.9+  
- **Framework:** Flask (or FastAPI)  
- **LLM SDK:** `openai` Python package  
- **Structure Library:** `ase`  
- **Validation:** `pydantic`  
- **Logging:** Python `logging` (Sentry optional)  
- **Testing:** `pytest`  

### Constraints & Considerations  
- **No persistent storage**—all context must be passed in each request.  
- **Stateless JSON API**—frontend drives session state.  
- **Performance target:** ≤3 s typical response.  
- **Security:** sanitize all inputs, hide internal traces in errors.  
- **Non-Goals (V1):**  
  - Async job queues (DFT, XRD)  
  - Authentication, rate limits, billing  
  - Surface/defect generation  

---

## 4. Milestones & Roadmap  

| Phase                                    | Duration | Deliverable                                         |
|------------------------------------------|---------:|-----------------------------------------------------|
| **1. Setup & Infrastructure**            | 3 days   | Repo scaffold, virtualenv, Flask skeleton           |
| **2. NLP & Command Generation**          | 4 days   | `nlp_client.py` with OpenAI functions & few-shot     |
| **3. Schema & Validation**               | 2 days   | Pydantic/JSON-Schema definitions in `models/`       |
| **4. Executor Implementation**           | 5 days   | ASE-based `buildStructure` & view computations      |
| **5. Integration & Error Handling**      | 3 days   | Glue pipeline in `app.py`, error wrappers           |
| **6. Testing & Performance Tuning**      | 4 days   | Unit/integration tests, benchmark <3 s              |
| **7. Documentation & Handoff**           | 2 days   | Write out spec docs (API_SPEC.md, JSON_SCHEMA.md,   |
|                                          |          | ARCHITECTURE.md, MODULE_SPEC.md)                    |
| **8.5. End-to-End Backend Testing**       | 1 day    | Comprehensive `curl` tests against local Flask app  |

---

## 5. Project Organization & Workflow  

### Repository Layout  
```

/backend
├── app.py
├── requirements.txt
├── config.py
├── nlp/
│   └── llm\_client.py
├── models/
│   └── commands.py
├── executor/
│   ├── structure.py
│   └── view\.py
├── utils/
│   ├── file\_utils.py
│   └── error\_handlers.py
└── docs/
├── PLANNING.md
├── TASK.md
├── API\_SPEC.md
├── JSON\_SCHEMA.md
├── ARCHITECTURE.md
└── MODULE\_SPEC.md

```

### Documentation Structure  
- Keep all spec docs in `/backend/docs/`.  
- Update living docs as interfaces evolve.

### Workflow & Best Practices  
1. **Branching:** feature branches named `feature/<module>`  
2. **Commits:** small, atomic, reference TASK.md items  
3. **Code Reviews:** require at least one peer approval  
4. **CI:** GitHub Actions to run `flake8`, `black`, `pytest` on each PR  
5. **Merging:** Squash and merge into `main` after tests pass  

---

## 6. Next Steps  

- Confirm final list of commands and schemas in JSON_SCHEMA.md.  
- Draft initial API_SPEC.md with `/api/commands` examples.  
- Spin up a stubbed Flask app in `app.py` to test the request/response cycle.  
- Assign module owners and break TASK.md into actionable tickets.  

---

This PLANNING.md serves as the strategic blueprint for the backend team. It outlines **what** we’re building, **why**, and **how** we’ll get there—while pointing to the detailed spec documents that contain the exact interface definitions and module contracts. Let’s align on this before moving into TASK.md and the individual spec files.

