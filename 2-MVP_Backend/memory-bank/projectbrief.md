# Project Brief: NLP-Atomic-Backend

## Project Name
NLP-Atomic-Backend

## Description
A stateless, Python-based service that powers our NLP-driven 3D atomic-structure viewer. It accepts natural-language prompts, invokes an LLM to generate structured JSON commands, executes those commands (structure generation and camera/view calculations), and returns the command sequence to the frontend for visualization.

## Core Requirements
- **Single API Endpoint:** Expose a single `POST /api/commands` endpoint.
- **NLP to JSON Commands:** Translate arbitrary chat prompts into validated command objects using an LLM.
- **Command Execution:**
    - Execute "buildStructure" commands via ASE.
    - Execute camera/view commands and calculate view parameters.
- **Data Return:** Return raw model data (e.g., PDB/XYZ text) and view parameters.
- **Performance:** Target a response time of under 3 seconds.
- **Documentation:** Provide thorough documentation (API spec, command schemas, architecture, module specs).

## Goals
- **Robust V1 Backend MVP:** Deliver a reliable backend service.
- **Enable Conversational Design:** Abstract backend complexities to allow frontend teams to focus on rendering.
- **Clear Extension Path:** Design for future enhancements and scalability.

## Non-Goals (V1)
- Async job queues (e.g., for DFT, XRD calculations).
- Authentication, rate limits, or billing.
- Generation of surfaces or defects.
- Persistent storage or user sessions (the API is stateless).