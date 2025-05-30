# Product Context: NLP-Atomic-Backend

## Why This Project Exists
This backend service is the engine for an NLP-driven 3D atomic structure viewer. The primary goal is to decouple the complexities of natural language processing, 3D model generation, and view calculations from the frontend application. By providing a clean API, frontend developers can focus on creating a rich user experience for visualizing atomic structures, while the backend handles the "heavy lifting."

## Problems It Solves
- **Simplifies Frontend Development:** Abstracts away LLM integration, ASE structure generation, and complex view mathematics.
- **Enables Conversational Interface:** Allows users to interact with the 3D viewer using natural language prompts.
- **Centralizes Core Logic:** Consolidates the "intelligence" of the application (NLP, generation, computation) into a maintainable and scalable backend service.
- **Performance for Interactive Use:** Designed to be stateless and fast, supporting a responsive user experience.

## How It Should Work
1.  **Frontend Request:** The frontend application sends a `POST` request to the `/api/commands` endpoint. The request body contains a natural language prompt from the user (e.g., "show me a 3x3x3 FCC aluminum crystal and rotate it 45 degrees around the x-axis").
2.  **NLP Processing (Backend):**
    *   The backend's `nlp_client` module receives the prompt.
    *   It interacts with an LLM (e.g., OpenAI GPT-4) using function calling and few-shot examples to translate the prompt into a sequence of structured JSON commands (e.g., `{"command": "buildStructure", "params": {"lattice": "FCC", "element": "Al", "nx": 3, "ny": 3, "nz": 3}}`, `{"command": "rotateCamera", "params": {"axis": "x", "angle": 45}}`).
3.  **Command Validation (Backend):**
    *   The `models/commands` module, using Pydantic, validates each generated command against predefined schemas to ensure correctness and security. Invalid commands are rejected.
4.  **Command Execution (Backend):**
    *   The `executor` module processes the validated commands:
        *   `buildStructure`: Uses ASE to generate the atomic model (e.g., as PDB or XYZ text).
        *   `setView`, `rotateCamera`, etc.: Computes the necessary camera/view parameters.
5.  **Backend Response:**
    *   The backend compiles the results of executed commands (e.g., the PDB/XYZ string for `buildStructure`, the `viewObject` for view commands) into a JSON array.
    *   This JSON array is returned to the frontend. For `buildStructure`, the raw model data (PDB/XYZ text) is included directly in the response.
6.  **Frontend Rendering:** The frontend application receives the command results and uses them to update the 3D viewer (e.g., load the PDB/XYZ data into 3Dmol.js, apply the view parameters).

## User Experience Goals (for the end-user of the complete system)
- **Intuitive Interaction:** Users can control the 3D scene using natural language.
- **Rapid Visualization:** Changes in the 3D viewer appear quickly after a prompt.
- **Accurate Interpretation:** The system correctly understands and executes user requests.
- **Clear Feedback:** (Handled by frontend) The frontend should provide feedback on command execution.