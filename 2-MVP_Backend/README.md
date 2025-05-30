# NLP-Atomic-Backend

A stateless, Python-based service that powers our NLP-driven 3D atomic-structure viewer. It accepts natural-language prompts, invokes an LLM to generate structured JSON commands, executes those commands (structure generation and camera/view calculations), and returns the command sequence to the frontend for visualization.

## Features

- **NLP to JSON Commands**: Translates natural language prompts into validated command objects using OpenAI's function calling.
- **Command Validation**: Rigorous schema enforcement using Pydantic to ensure only valid commands are processed.
- **Structure Generation**: Utilizes the Atomic Simulation Environment (ASE) to build 3D atomic structures (e.g., FCC lattices) from commands.
- **View Calculations**: Computes camera and view parameters for 3D visualization.
- **Stateless API**: Designed as a stateless JSON API, with the frontend managing session state.
- **Performance**: Aims for sub-3 second response times for typical requests.

## Installation

Follow these steps to set up the development environment:

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
    The `requirements.txt` file includes:
    - `flask`
    - `flask-cors`
    - `openai`
    - `ase`
    - `pydantic`
    - `pytest`

## Environment Variables

The application requires an OpenAI API key.

1.  **Create a `.env` file** in the `2-MVP_Backend` directory:
    ```
    OPENAI_API_KEY="your_openai_api_key_here"
    ```
    **Note**: Add `.env` to your `.gitignore` file to prevent it from being committed to version control.

2.  The `config.py` file will load this environment variable.

## Running the Application

To run the Flask application in development mode:

1.  **Activate your virtual environment** (if not already active):
    ```bash
    source venv/bin/activate
    ```

2.  **Set Flask environment variables**:
    ```bash
    export FLASK_APP=app.py
    export FLASK_ENV=development # Enables debug mode
    ```
    On Windows, use `set FLASK_APP=app.py` and `set FLASK_ENV=development`.

3.  **Start the Flask server**:
    ```bash
    flask run
    ```
    The API will be accessible at `http://localhost:5000`.

## Running Tests

Unit and integration tests are written using `pytest`.

1.  **Activate your virtual environment**.

2.  **Run all tests**:
    ```bash
    pytest
    ```

3.  **Run tests with duration reporting** (useful for performance tuning):
    ```bash
    pytest --durations=10
    ```

## Documentation

For more detailed documentation, refer to the `docs/` directory:

-   [`API_SPEC.md`](docs/API_SPEC.md): API endpoint definitions and examples.
-   [`JSON_SCHEMA.md`](docs/JSON_SCHEMA.md): Complete command and parameter schemas.
-   [`ARCHITECTURE.md`](docs/ARCHITECTURE.md): Detailed architecture diagrams and data flow.
-   [`MODULE_SPEC.md`](docs/MODULE_SPEC.md): Module-by-module interface definitions.
-   [`PLANNING.md`](PLANNING.md): High-level project strategy and roadmap.
-   [`TASK.md`](TASK.md): Detailed implementation steps and checklist.

## License

[License Type] (e.g., MIT, Apache 2.0)