<!-- TASK.md -->

# TASK.md

> **Audience:** Junior developer (expert coder, needs explicit guidance)  
> **Goal:** Build the one-page Flask-based MVP: chat input → 3D crystal render.
> **Active Implementation Directory:** `1-MVP/`

---

## Phase 1: Environment & Project Scaffold (3 days)

1. **Set up Python environment**  
   - Install Python 3.9+ and create a virtual environment.  
   - Install Flask, OpenAI SDK, and ASE.  
2. **Initialize Git repository**  
   - Create `main` branch and push to remote.  
   - Create a `phase1/setup` feature branch.  
3. **Scaffold Flask app**  
   - Create an `app.py` file that starts a Flask server.  
   - Configure Flask to serve static files and templates.  
4. **Define folder structure**  
   - Create `templates/` for HTML.  
   - Create `static/js/` and `static/css/` for frontend assets.  
   - Create `models/` (or `static/models/`) for generated files.  
5. **Basic HTML template**  
   - Create a Jinja2 template with an empty container.  
   - Include links to CSS and JS files.  
6. **Set up CSS layout**  
   - Define CSS classes to split the page into two columns: left viewer (2/3) and right chat (1/3).  
7. **Verify the empty page**  
   - Run Flask, open the page in a browser, and confirm the two-column layout appears.

---

## Phase 2: Viewer Integration (2 days) - DONE
- **"Show Unit Cell" Feature Implemented:**
    - New checkbox for "Show Unit Cell" added to `1-MVP/templates/index.html`.
    - `toggleUnitCell` function implemented in `1-MVP/static/js/script.js` to display a magenta, dashed unit cell based on `CRYST1` data.
    - Debugging ensured correct display and hiding of the unit cell.
- Created `1-MVP/docs/unit_cell_feature.md` to document the new feature.

1. **Add 3Dmol.js to page**  
   - Include the 3Dmol.js script in the HTML template.  
2. **Build viewer container**  
   - Add a `div` for the 3D viewer in the left column.  
3. **Implement JS loader function**  
   - Write a vanilla JavaScript function that takes a URL to a structure file and loads it into the viewer.  
4. **Test with a sample file**  
   - Place a known `.pdb` or `.xyz` in `models/`, call the loader on page load, and confirm you can rotate/zoom.

---

## Phase 3: Natural-Language → Slot Extraction (2 days)

1. **Define LLM interaction**  
   - In Python, create a function to send the user’s prompt to OpenAI with clear examples mapping phrases to lattice, element, and dimensions.  
2. **Parse LLM response**  
   - Extract a Python dictionary with keys: lattice, element, nx, ny, nz.  
3. **Handle invalid output**  
   - If keys are missing or values are unexpected, prepare a clear error message.  
4. **Unit test slot extractor**  
   - Write simple tests for valid prompts (e.g. “3×3×3 FCC Al”) and invalid ones (e.g. “make graphene”).

---

## Phase 4: ASE-Based Structure Generation (2 days)

1. **Write build routine**  
   - Create a Python function that calls ASE to build a unit cell and scale by (nx, ny, nz).  
   - Save the resulting structure to a new file in `models/` with a unique name.  
2. **Integrate into Flask**  
   - In the `/generate` route, call the slot extractor, then the build function, catch errors, and assemble a JSON response containing a message and the file URL.  
3. **Serve generated files**  
   - Ensure Flask can serve files from the `models/` folder via static routing.  
4. **Test end-to-end**  
   - Manually invoke the `/generate` endpoint (e.g. via browser or curl) with a prompt and verify the file appears and is valid.

---

## Phase 5: Chat Pane & AJAX Flow (2 days)

1. **Build chat UI elements**  
   - In the right column, add a scrollable message list, a text input, and a “Send” button.  
2. **Write JavaScript to send prompts**  
   - On clicking “Send,” read the input value, clear the field, and append the user message to the list.  
   - Send an AJAX POST to `/generate` with the prompt in JSON.  
3. **Handle backend response**  
   - On success, append the system message to chat and call the viewer loader with the returned file URL.  
   - On error, display the error message in the chat pane.  
4. **Maintain scroll position**  
   - Ensure the chat pane always scrolls to the newest message.

---

## Phase 6: Testing & Quality Assurance (3 days)

1. **Manual testing scenarios**  
   - Valid prompts for FCC, BCC, SC and various elements.  
   - Invalid prompts or unsupported lattices.  
   - Network failure or server error.  
2. **Backend unit tests**  
   - Test slot extraction and ASE build routine separately.  
3. **Frontend tests (optional)**  
   - Manually verify chat → generate → viewer cycle.  
4. **Performance checks**  
   - Measure time from button click to viewer update; target under 3 seconds.  
5. **Accessibility & Responsiveness**  
   - Confirm layout works on different window sizes.  
   - Ensure keyboard focus and basic ARIA labels for chat input.

---

## Phase 7: Documentation & Deployment (2 days)

1. **Write README**  
   - Installation steps, how to run locally, how to invoke `/generate`.  
2. **API specification**  
   - Describe `/generate` payload and response format in `docs/API.md`.  
3. **Architecture diagram**  
   - Add a simple Mermaid or drawn diagram to `docs/ARCHITECTURE.md`.  
4. **Cleanup**  
   - Remove debug logs, confirm dependency versions.  
5. **Optional Dockerization**  
   - Add Dockerfile and instructions if desired.  
6. **Final review & merge**  
   - Create a pull request against `main`, request review, merge once approved.  

---

## Backlog / Future Enhancements
- Support non-cubic lattices and surfaces.  
- Add drag-and-drop atom editing in the 3D viewer.  
- Integrate simple physics or DFT relaxation calls.  
- Persist user sessions and save project files.  
- Add user authentication and project management.  

