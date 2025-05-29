# Product Context: NL-Atomic-Flask-MVP

## Why This Project Exists
The project aims to bridge the gap between natural language interaction and scientific visualization, specifically for crystal structures. Traditional methods of generating and visualizing crystal structures often require specialized software, command-line tools, or complex scripting. This project seeks to simplify this process by allowing users to describe the desired structure in plain English and immediately see a 3D representation.

## Problems It Solves
- **Accessibility:** Lowers the barrier to entry for non-experts or those unfamiliar with crystallography software.
- **Speed of Prototyping:** Enables rapid generation and visualization of basic crystal structures for quick ideation and exploration.
- **User Experience:** Provides an intuitive, conversational interface instead of complex forms or syntax.
- **Educational Tool:** Can serve as a simple tool for students or researchers to quickly visualize concepts.

## How It Should Work
1. **User Input:** A user types a natural language prompt (e.g., "Show me a 2x2x2 FCC aluminum crystal") into a chat input field.
2. **Prompt Processing:** The Flask backend receives the prompt and uses an LLM (Large Language Model) to extract key parameters such as lattice type (FCC, BCC, SC), chemical element, and supercell dimensions (nx, ny, nz).
3. **Structure Generation:** Using the extracted parameters, the Atomic Simulation Environment (ASE) library generates the corresponding crystal structure.
4. **File Output:** The generated structure is saved as a standard file format (e.g., .xyz, .pdb) in a publicly accessible directory.
5. **3D Visualization:** The frontend JavaScript (3Dmol.js) loads the generated structure file and displays it in an interactive 3D viewer.
6. **Chat Feedback:** The chat pane updates with system messages, confirming successful generation or providing error messages if the prompt was unclear or invalid.

## User Experience Goals
- **Simplicity:** The interface should be clean, uncluttered, and easy to understand.
- **Responsiveness:** Interactions should feel immediate, with the 3D model updating quickly after a prompt.
- **Clarity:** System responses in the chat should be clear, concise, and helpful, guiding the user if needed.
- **Interactivity:** The 3D viewer should allow for intuitive rotation, zooming, and panning of the crystal structure.