# Architecture Overview: NLP-Atomic-Backend

This document outlines the high-level architecture and data flow of the NLP-Atomic-Backend service. The service is designed to be stateless, processing natural language prompts to generate and execute commands for 3D atomic structure visualization.

## High-Level Architecture and Data Flow

The following diagram illustrates the main components of the NLP-Atomic-Backend and their interactions:

```mermaid
graph TD
    Client[Frontend Application] -->|POST /api/commands (JSON: {prompt: "..."})| API[API Layer (app.py)]

    subgraph NLP-Atomic-Backend
        API -->|User Prompt| NLPClient[NLP Client (nlp/llm_client.py)]
        NLPClient -->|Prompt, Function Schemas, Few-shot Examples| OpenAI[OpenAI ChatCompletion API]
        OpenAI -->|JSON Command Sequence| NLPClient
        NLPClient -->|Raw JSON Commands| Validator[Validation Module (models/commands.py)]
        Validator -->|Validated Command Objects| Executor[Executor Module]
        Executor -->|Executes buildStructure| StructureExecutor[Structure Executor (executor/structure.py)]
        StructureExecutor -->|Uses ASE| ASE[ASE Library]
        Executor -->|Executes setView, rotateCamera| ViewExecutor[View Executor (executor/view.py)]
        
        StructureExecutor -->|PDB/XYZ Text| Executor
        ViewExecutor -->|View Object| Executor
        Executor -->|Aggregated Results| API
    end

    API -->|JSON: [{command: "...", params: {...}, result: ...}]| Client
```

## Component Responsibilities

*   **Frontend Application:** Initiates requests with natural language prompts to the backend.
*   **API Layer (`app.py`):** Serves as the entry point for all requests, handles routing, request parsing, and orchestrates the flow between other backend components.
*   **NLP Client (`nlp/llm_client.py`):** Interfaces with the OpenAI ChatCompletion API, sending user prompts and receiving structured JSON command sequences. It incorporates function schemas and few-shot examples to guide the LLM's output.
*   **OpenAI ChatCompletion API:** The external Large Language Model service responsible for translating natural language into structured commands.
*   **Validation Module (`models/commands.py`):** Uses Pydantic to validate the raw JSON commands received from the NLP Client, ensuring they conform to predefined schemas.
*   **Executor Module:** Dispatches validated command objects to the appropriate specialized executors.
    *   **Structure Executor (`executor/structure.py`):** Handles commands related to building atomic structures (e.g., `buildStructure`) using the ASE library. Returns PDB or XYZ text.
    *   **View Executor (`executor/view.py`):** Handles commands related to camera and view manipulations (e.g., `setView`, `rotateCamera`). Returns a view object.
*   **ASE Library:** An external Python library used by the Structure Executor for atomic simulation and material science.

## Data Flow Summary

1.  The **Frontend Application** sends a `POST` request to `/api/commands` with a natural language `prompt`.
2.  The **API Layer** receives the prompt and forwards it to the **NLP Client**.
3.  The **NLP Client** interacts with the **OpenAI ChatCompletion API**, providing the prompt, function schemas, and few-shot examples.
4.  **OpenAI** returns a sequence of raw JSON commands.
5.  The **NLP Client** passes these raw commands to the **Validation Module**.
6.  The **Validation Module** validates the commands and converts them into structured Python objects.
7.  The **Executor Module** receives the validated command objects and dispatches them to either the **Structure Executor** (for `buildStructure` commands, which uses **ASE**) or the **View Executor** (for camera/view commands).
8.  The executors perform their respective operations and return results (PDB/XYZ text or view objects) back to the **Executor Module**.
9.  The **Executor Module** aggregates these results and sends them back to the **API Layer**.
10. The **API Layer** formats the aggregated results into a JSON response and sends it back to the **Frontend Application**.
