```markdown
<!-- PLANNING.md -->

# PLANNING.md

## 1. Project Overview
- **Project Name:** NL-Atomic-Flask-MVP  
- **Description:** A single-page Flask application in which users type natural-language prompts in a chat pane (right third) and immediately see a generated cubic crystal structure in a 3D viewer pane (left two-thirds).
- **Active Implementation Directory:** `1-MVP/`

## 2. Vision & Objectives
- **Vision Statement:**  
  Enable rapid prototyping of basic crystal structures through conversational prompts, without requiring specialized software or frontend frameworks.

- **Key Objectives:**  
  1. Deliver a working proof-of-concept entirely within Flask (no React).  
  2. Support three lattice types (FCC, BCC, SC) for any chemical element.  
  3. Achieve under 3 seconds from prompt submission to 3D render.  
  4. Maintain a responsive, two-column layout on one HTML page.  
  5. Provide clear user feedback and error handling in the chat pane.

## 3. Architecture Overview
- **Core Components:**  
  - **Flask App:** Serves HTML template, static assets, and handles API requests.  
  - **HTML Template:** Jinja2 page with a CSS layout dividing viewer and chat.  
  - **JavaScript:** Sends user prompts to the Flask endpoint, updates chat history, and drives the 3D viewer.  
  - **3D Viewer:** 3Dmol.js embedded in the page for rotate/zoom of atomic models.  
  - **LLM Processor:** Python function calling OpenAI to extract lattice parameters.  
  - **ASE Generator:** Python routine that builds a supercell and writes out a structure file.  
  - **Static File Server:** Flask serves generated files for the viewer to fetch.

- **Deliverables:**  
  - This PLANNING.md and a matching TASK.md.  
  - API specification for the `/generate` endpoint.  
  - A simple architecture diagram (Mermaid or drawn).

- **Technology Stack:**  
  - **Backend:** Python 3.9+, Flask, OpenAI Python SDK, ASE.  
  - **Frontend:** Jinja2 templates, vanilla JavaScript, 3Dmol.js, CSS Grid or Flexbox.  
  - **Hosting/Deployment:** Docker (optional), any simple VM or PaaS.

- **Constraints & Non-Goals:**  
  - **Constraints:**  
    - Entire POC within one Flask application; no separate frontend framework.  
    - Only cubic lattices; no surfaces, defects, or nanoparticles in this phase.  
  - **Non-Goals:**  
    - No DFT or energy minimization.  
    - No user login or persistence beyond file generation.  
    - No drag-and-drop editing in the viewer.

## 4. Milestones & Roadmap
| Phase             | Duration   | Deliverable                                  |
|-------------------|------------|----------------------------------------------|
| **1. Setup & Layout**      | 3 days     | Flask scaffold, HTML template with two panels |
| **2. Viewer Integration**  | 2 days     | Embed 3Dmol.js, test static file rendering    |
| **3. NL→Slots**            | 2 days     | LLM prompt logic to extract lattice JSON      |
| **4. Structure Generation**| 2 days     | ASE routine to build and write supercell file |
| **5. Chat Loop**           | 2 days     | AJAX flow: prompt → response → viewer update  |
| **6. Testing & Validation**| 3 days     | Manual & unit tests for all components        |
| **7. Documentation & Handoff** | 2 days | Final docs, README, simple deployment guide   |

## 5. Project Organization & Workflow
- **Repository Layout:**
```

/app.py              ← Flask application
/templates/          ← Jinja2 HTML templates
/static/
/js/               ← JavaScript for chat & viewer
/css/              ← Styles for layout
/models/           ← Generated structure files
/docs/               ← API spec, architecture diagram

```
- **Development Workflow:**
1. Create a feature branch for each phase.  
2. Implement locally, commit early and often.  
3. Open a pull request, request review, merge into `main`.  
4. Run automated tests and manual smoke tests on each merge.  
- **Communication & Reviews:**
- Daily check-ins on progress.  
- Demo the working page at end of each phase.  

