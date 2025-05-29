# Technical Context: NL-Atomic-Flask-MVP

## Technologies Used

### Backend
- **Python 3.9+:** The primary programming language for the Flask application, LLM integration, and ASE.
- **Flask:** A lightweight WSGI web application framework in Python. Used for routing, serving static files, and handling API requests.
- **OpenAI Python SDK:** Official Python library for interacting with OpenAI's API, used for natural language processing and parameter extraction.
- **Atomic Simulation Environment (ASE):** A Python library for atomistic simulations. Used for building and manipulating crystal structures (e.g., FCC, BCC, SC) and writing them to file formats.

### Frontend
- **Jinja2:** A modern and designer-friendly templating language for Python, used by Flask to render HTML pages.
- **Vanilla JavaScript:** Pure JavaScript (ES6+) for all frontend interactivity, including AJAX calls, DOM manipulation, and 3Dmol.js integration. No frontend frameworks (e.g., React, Vue, Angular) are used.
- **3Dmol.js:** A JavaScript library for molecular visualization. Embedded in the HTML to render and interact with 3D crystal structures.
- **CSS Grid / Flexbox:** Modern CSS layout modules used for creating the responsive two-column layout of the application.

## Development Setup

### Local Environment
1. **Python Virtual Environment:** It is highly recommended to use a virtual environment (e.g., `venv`) to manage project dependencies.
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. **Dependency Installation:** All Python dependencies should be listed in a `requirements.txt` file and installed using pip.
   ```bash
   pip install -r requirements.txt
   ```
3. **OpenAI API Key:** An OpenAI API key is required for the LLM integration. This should be set as an environment variable (e.g., `OPENAI_API_KEY`).
   ```bash
   export OPENAI_API_KEY='your_api_key_here'
   ```
4. **Running the Flask App:** The Flask development server can be started from the command line.
   ```bash
   export FLASK_APP=app.py
   flask run
   ```

### Project Structure
```
/app.py              ← Main Flask application file
/templates/          ← Jinja2 HTML templates (e.g., index.html)
/static/             ← Static assets (CSS, JS, generated models)
    /css/            ← Stylesheets (e.g., style.css)
    /js/             ← JavaScript files (e.g., script.js)
    /models/         ← Directory for generated crystal structure files (.xyz, .pdb)
/docs/               ← Project documentation (API spec, architecture diagrams)
/tests/              ← Unit and integration tests
/venv/               ← Python virtual environment (ignored by Git)
/requirements.txt    ← Python dependency list
/.gitignore          ← Git ignore file
/PLANNING.md         ← Project planning document
/TASK.md             ← Current tasks and backlog
/memory-bank/        ← Project memory bank files
```

## Technical Constraints
- **No External Frontend Frameworks:** Strictly adhere to vanilla JavaScript and Jinja2 for the frontend.
- **Cubic Lattices Only:** The ASE generation logic should only handle FCC, BCC, and SC cubic structures.
- **Single Page Application (SPA) within Flask:** The entire user interface should reside on a single HTML page served by Flask.
- **Performance:** The 3-second render target is a hard constraint for the prompt-to-render cycle.

## Dependencies
- `Flask`
- `openai`
- `ase`
- `pydantic` (for data validation, if needed for LLM output parsing)
- `SQLAlchemy` or `SQLModel` (not applicable for this MVP, as no database persistence is required)

## Tool Usage Patterns
- **Git:** For version control, branching, and merging.
- **Pip:** For Python package management.
- **Black:** For Python code formatting (PEP8 compliance).
- **Pytest:** For running unit and integration tests.
- **Mermaid:** For generating diagrams within Markdown documentation.