# Feature: Show Unit Cell Toggle

## Description
This feature allows users to toggle the visibility of the crystallographic unit cell within the 3Dmol.js viewer. The unit cell will be rendered as a dotted line cube based on the `CRYST1` record in the loaded PDB file. If the PDB file does not contain `CRYST1` information, the toggle will have no effect.

## Components Affected
1.  **`1-MVP/templates/index.html`**:
    *   A new checkbox input will be added to the "Controls" section within the `info-pane`. This checkbox will serve as the "Show Unit Cell" toggle.
2.  **`1-MVP/static/js/script.js`**:
    *   A new JavaScript function, `toggleUnitCell(show)`, will be implemented. This function will be responsible for adding or removing the unit cell visualization.
    *   The `init3DmolViewerAndUI` function will be modified to:
        *   Get a reference to the new "Show Unit Cell" checkbox.
        *   Attach an event listener to the checkbox to call `toggleUnitCell` when its state changes.
        *   Call `toggleUnitCell` initially based on the checkbox's default state.
    *   The `toggleUnitCell` function will:
        *   Check if `mainModel` (the loaded 3Dmol.js model) contains unit cell information.
        *   If `show` is true and unit cell information is present, use `viewer.addUnitCell({model: mainModel})` to render the unit cell.
        *   If `show` is false, or if no unit cell information is present, remove any existing unit cell visualization using `viewer.removeModel(unitCellModel)` (where `unitCellModel` is a reference to the added unit cell model).
        *   Call `viewer.render()` after adding or removing the unit cell.
3.  **`1-MVP/docs/` (New Directory)**:
    *   This markdown file (`unit_cell_feature.md`) will document this feature's implementation details, including the architectural decisions and code changes.

## Architectural Decisions & Rationale
*   **Leverage 3Dmol.js `addUnitCell`:** 3Dmol.js provides a built-in function to render unit cells directly from PDB data, simplifying implementation and ensuring consistency with the viewer's capabilities. This avoids manual calculation and drawing of the unit cell.
*   **Conditional Rendering:** The feature will gracefully handle PDB files without `CRYST1` records by doing nothing, preventing errors and providing a robust user experience.
*   **Clear Separation of Concerns:** HTML handles the UI element, JavaScript manages the logic and interaction with 3Dmol.js, and documentation provides clarity on the feature.
*   **Event-Driven Interaction:** Using an event listener on the checkbox ensures that the unit cell visibility updates dynamically in response to user input.
*   **Single Source of Truth for Unit Cell Model:** A dedicated variable (`unitCellModel`) will store the reference to the added unit cell model, allowing for efficient removal when the toggle is switched off.

## Data Flow
User interacts with "Show Unit Cell" checkbox in `index.html`
↓
`change` event triggers `toggleUnitCell` function in `script.js`
↓
`toggleUnitCell` checks `mainModel` for unit cell data
↓
If data exists and toggle is ON: `viewer.addUnitCell` is called, rendering the unit cell.
If data exists and toggle is OFF: `viewer.removeModel` is called, removing the unit cell.
If no data: No action.
↓
`viewer.render()` updates the 3D view.

## Security and Privacy Considerations
*   No sensitive data is handled by this feature.
*   The feature operates entirely client-side, reducing backend load.

## Performance and Scalability
*   `addUnitCell` is optimized by 3Dmol.js.
*   Rendering a simple dotted cube is a low-overhead operation.
*   The feature does not introduce significant performance bottlenecks.

## Trade-offs
*   **Simplicity vs. Customization:** Relying on `addUnitCell` is simple but offers limited customization for the unit cell appearance (e.g., line style, color beyond default). For this MVP, simplicity is preferred.