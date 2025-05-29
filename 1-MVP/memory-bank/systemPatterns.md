# System Patterns: NL-Atomic-Flask-MVP

## System Architecture
The application follows a classic client-server architecture, with Flask acting as both the web server and the backend API. The frontend is a single HTML page rendered by Jinja2, utilizing vanilla JavaScript and CSS for interactivity and layout.

```mermaid
graph TD
    User[User] -->|HTTP Request| FlaskApp[Flask Application]
    FlaskApp -->|Serves HTML, CSS, JS| Browser[User's Browser]
    Browser -->|Displays UI, 3D Viewer, Chat| User

    subgraph Frontend (Browser)
        HTML[index.html (Jinja2)]
        CSS[style.css]
        JS[script.js]
        3DmolJS[3Dmol.js Library]
        HTML --> CSS
        HTML --> JS
        JS --> 3DmolJS
    end

    subgraph Backend (Flask Application)
        PythonApp[app.py]
        LLMProcessor[LLM Processor (Python)]
        ASEGenerator[ASE Generator (Python)]
        StaticFiles[Static File Server]
        PythonApp --> LLMProcessor
        PythonApp --> ASEGenerator
        PythonApp --> StaticFiles
    end

    Browser -->|AJAX POST /generate| PythonApp
    PythonApp -->|Calls OpenAI API| LLMProcessor
    LLMProcessor -->|Extracted Parameters| ASEGenerator
    ASEGenerator -->|Generates .xyz/.pdb| StaticFiles
    StaticFiles -->|Serves Structure File| Browser
    Browser -->|Loads Structure URL| 3DmolJS
```

## Key Technical Decisions
- **Single Flask Application:** To meet the constraint of a single POC, all components (frontend serving, API, LLM interaction, structure generation) are consolidated within one Flask application.
- **Vanilla JavaScript:** Avoids the overhead and complexity of frontend frameworks for this MVP, keeping the project lightweight.
- **3Dmol.js for Visualization:** A robust and easy-to-integrate JavaScript library for 3D molecular visualization, suitable for displaying crystal structures.
- **OpenAI for NL Processing:** Leverages a powerful LLM for flexible and accurate extraction of parameters from natural language prompts.
- **ASE for Structure Generation:** The Atomic Simulation Environment (ASE) is a well-established Python library for atomistic simulations, providing reliable tools for building crystal structures.
- **Static File Serving for Models:** Generated crystal structure files are saved to a static directory and served directly by Flask, allowing 3Dmol.js to fetch them via URL.

## Design Patterns in Use
- **MVC (Model-View-Controller) - loosely applied:**
    - **Model:** LLM Processor (extracts data), ASE Generator (creates data).
    - **View:** Jinja2 templates, HTML, CSS, 3Dmol.js (renders data).
    - **Controller:** Flask routes (handles requests, orchestrates model and view).
- **API Endpoint:** A clear `/generate` endpoint for client-server communication.
- **Static File Serving:** Standard pattern for serving user-generated or pre-defined assets.

## Component Relationships
- **Frontend (Browser):**
    - `index.html`: The main page, includes CSS, JS, and the 3Dmol.js library.
    - `style.css`: Defines the layout and visual styling.
    - `script.js`: Handles user input, AJAX calls to Flask, and interaction with 3Dmol.js.
    - `3Dmol.js`: Embedded library for rendering 3D structures.
- **Backend (Flask `app.py`):**
    - **Routes:** Defines endpoints like `/` (for serving the main page) and `/generate` (for processing prompts).
    - **LLM Integration:** A Python function that interfaces with the OpenAI API to interpret natural language.
    - **ASE Integration:** A Python function that uses ASE to construct crystal structures based on LLM output.
    - **File Management:** Saves generated structures to the `static/models/` directory.

## Critical Implementation Paths
1. **Prompt to Render Flow:** User types prompt -> JS sends to `/generate` -> Flask calls LLM -> LLM returns parameters -> Flask calls ASE -> ASE generates file -> Flask returns file URL -> JS loads file into 3Dmol.js. This entire path must be optimized for speed.
2. **Error Handling:** Robust error handling at each step of the prompt-to-render flow, providing clear feedback to the user in the chat pane.
3. **Static File Serving:** Ensuring Flask correctly serves dynamically generated files from the `models/` directory.