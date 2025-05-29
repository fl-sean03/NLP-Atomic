# Active Context: NL-Atomic-Flask-MVP

## Current Work Focus
The current focus is on setting up the foundational project structure and documentation for the NL-Atomic-Flask-MVP. This includes:
- Creating the `1-MVP` subdirectory to house the current implementation.
- Moving `PLANNING.md` and `TASK.md` into the `1-MVP` directory.
- Creating symlinks for `PLANNING.md` and `TASK.md` in the workspace root, pointing to their new locations within `1-MVP`.
- Populating the `memory-bank` directory within `1-MVP` with initial core documentation files (`projectbrief.md`, `productContext.md`, `systemPatterns.md`, `techContext.md`).

## Recent Changes
- Created `1-MVP/` directory.
- Moved `PLANNING.md` and `TASK.md` to `1-MVP/`.
- Created symlinks `PLANNING.md` and `TASK.md` in the root to `1-MVP/PLANNING.md` and `1-MVP/TASK.md` respectively.
- Created `1-MVP/memory-bank/` directory.
- Created `1-MVP/memory-bank/projectbrief.md`.
- Created `1-MVP/memory-bank/productContext.md`.
- Created `1-MVP/memory-bank/systemPatterns.md`.
- Created `1-MVP/memory-bank/techContext.md`.
- Updated `1-MVP/PLANNING.md` and `1-MVP/TASK.md` to include the `Active Implementation Directory` reference.
- Created symlink `memory-bank` in workspace root pointing to `1-MVP/memory-bank`.
- Initialized Git repository with remote origin set to `https://github.com/fl-sean03/NLP-Atomic.git`.
- Renamed Git branch to `main`.

## Next Steps
1. Create `1-MVP/memory-bank/progress.md`.
2. Begin Phase 1 of the `TASK.md`: "Environment & Project Scaffold". This will involve:
    - Setting up the Python virtual environment.
    - Installing initial dependencies (Flask, OpenAI SDK, ASE).
    - Creating the basic Flask application structure (`app.py`, `templates/`, `static/`).

## Active Decisions and Considerations
- The project will strictly adhere to the "Flask-only" constraint for the MVP.
- All generated crystal structure files will be saved in `static/models/` to be served directly by Flask.
- The `memory-bank` will be the primary source of truth for project context and progress.

## Important Patterns and Preferences
- **Documentation First:** Comprehensive documentation in the `memory-bank` is crucial due to the memory reset characteristic.
- **Modular Design:** Code will be organized into clear, separated modules.
- **Test-Driven Development (TDD):** New features will have associated Pytest unit tests.
- **PEP8 and Black:** Adherence to Python style guidelines and automatic formatting.

## Learnings and Project Insights
- The initial setup involves significant file system manipulation and documentation creation to establish the project's foundational context.
- The symlinking of `PLANNING.md` and `TASK.md` is critical for maintaining a consistent entry point to the active implementation's documentation from the workspace root.