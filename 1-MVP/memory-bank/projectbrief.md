# Project Brief: NL-Atomic-Flask-MVP

## Project Name
NL-Atomic-Flask-MVP

## Description
A single-page Flask application where users input natural-language prompts in a chat pane (right third) and immediately see a generated cubic crystal structure in a 3D viewer pane (left two-thirds).

## Core Requirements
- **Flask-only:** The entire proof-of-concept must be built within a single Flask application, without external frontend frameworks like React.
- **Cubic Lattice Support:** Must support Face-Centered Cubic (FCC), Body-Centered Cubic (BCC), and Simple Cubic (SC) lattice types.
- **Any Chemical Element:** The system should be able to generate structures for any specified chemical element.
- **Performance Target:** Achieve a response time of under 3 seconds from prompt submission to 3D render.
- **Responsive Layout:** Maintain a two-column layout (2/3 viewer, 1/3 chat) on a single HTML page, responsive to different window sizes.
- **User Feedback & Error Handling:** Provide clear messages and handle errors gracefully within the chat pane.

## Goals
- **Rapid Prototyping:** Enable quick generation of basic crystal structures through conversational prompts.
- **Ease of Use:** No specialized software or complex setup required for users.
- **Proof-of-Concept:** Deliver a working MVP to demonstrate the core idea.

## Non-Goals
- **Advanced Material Science:** No DFT (Density Functional Theory) or energy minimization calculations.
- **User Management:** No user login, authentication, or persistence of user sessions.
- **Complex Structure Editing:** No drag-and-drop editing or advanced manipulation within the 3D viewer.
- **Non-Cubic Lattices:** Only cubic lattices are supported in this phase; no surfaces, defects, or nanoparticles.