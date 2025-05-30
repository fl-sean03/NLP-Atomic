let viewer = null;
let mainModel = null; // To store the reference to the main PDB model
let unitCellModel = null; // To store the reference to the unit cell model

/**
 * Adds X, Y, Z coordinate axes to the viewer manually at the world origin.
 * @param {$3Dmol.GLViewer} viewerInstance The 3Dmol viewer instance.
 * @param {number} [length=2] The length of the axes from the origin.
 */
function addViewerAxesManually(viewerInstance, length = 2) {
    if (!viewerInstance) return;

    // Clear existing axes before adding new ones
    viewerInstance.removeAllShapes();
    viewerInstance.removeAllLabels();

    const axisRadius = 0.05;
    const arrowheadRadiusRatio = 0.3; // Controls arrowhead size relative to axis radius
    const labelOffset = 0.3; // How far the label is from the arrowhead

    // X-axis (Red)
    viewerInstance.addArrow({
        start: { x: 0, y: 0, z: 0 },
        end:   { x: length, y: 0, z: 0 },
        radius: axisRadius,
        color: 'red',
        radiusRadio: arrowheadRadiusRatio,
        mid: 1.0
    });
    viewerInstance.addLabel("X", {
        position: { x: length + labelOffset, y: 0, z: 0 },
        fontColor: "red",
        fontSize: 14,
        showBackground: false,
    });

    // Y-axis (Green)
    viewerInstance.addArrow({
        start: { x: 0, y: 0, z: 0 },
        end:   { x: 0, y: length, z: 0 },
        radius: axisRadius,
        color: 'green',
        radiusRadio: arrowheadRadiusRatio,
        mid: 1.0
    });
    viewerInstance.addLabel("Y", {
        position: { x: 0, y: length + labelOffset, z: 0 },
        fontColor: "green",
        fontSize: 14,
        showBackground: false,
    });

    // Z-axis (Blue)
    viewerInstance.addArrow({
        start: { x: 0, y: 0, z: 0 },
        end:   { x: 0, y: 0, z: length },
        radius: axisRadius,
        color: 'blue',
        radiusRadio: arrowheadRadiusRatio,
        mid: 1.0
    });
    viewerInstance.addLabel("Z", {
        position: { x: 0, y: 0, z: length + labelOffset },
        fontColor: "blue",
        fontSize: 14,
        showBackground: false,
    });
}


// Function to update molecular representation
function updateRepresentation(styleType) {
    if (!viewer || !mainModel) return;
    viewer.setStyle({model: mainModel}, {}); // Clear existing styles before applying new ones

    let styleSpec = {};
    switch (styleType) {
        case 'sphere': styleSpec = { sphere: { radius: 0.7, colorscheme: 'Jmol' } }; break;
        case 'ballAndStick': styleSpec = { stick: { radius: 0.15, colorscheme: 'Jmol' }, sphere: { radius: 0.4, colorscheme: 'Jmol' } }; break;
        case 'stick': styleSpec = { stick: { colorscheme: 'Jmol', radius: 0.1 } }; break;
        case 'line': styleSpec = { line: { colorscheme: 'Jmol', lineWidth: 2 } }; break;
    }
    viewer.setStyle({model: mainModel}, styleSpec);
}

// Function to toggle XYZ axes visibility
function toggleViewerAxes(show) {
    if (!viewer) return;
    if (show) {
        addViewerAxesManually(viewer, 2.5); // Re-adds axes
    } else {
        viewer.removeAllShapes(); // Remove arrows
        viewer.removeAllLabels(); // Remove labels
    }
    viewer.render();
}

// Function to change viewer background color
function changeBackgroundColor(color) {
    if (!viewer) return;
    // 3Dmol.js setBackgroundColor typically handles CSS color names (e.g., "black")
    // and hex strings (e.g., "#000000") correctly.
    viewer.setBackgroundColor(color);
}
/**
 * Parses the CRYST1 record from a PDB data string.
 * @param {string} pdbDataString The full PDB file content as a string.
 * @returns {object|null} An object containing a, b, c, alpha, beta, gamma, or null if not found/invalid.
 */
function parseCryst1(pdbDataString) {
    const lines = pdbDataString.split("\n");
    const cryst1Line = lines.find(line => line.startsWith("CRYST1"));
    if (!cryst1Line) return null;

    try {
        const a = Number.parseFloat(cryst1Line.substring(6, 15));
        const b = Number.parseFloat(cryst1Line.substring(15, 24));
        const c = Number.parseFloat(cryst1Line.substring(24, 33));
        const alpha = Number.parseFloat(cryst1Line.substring(33, 40));
        const beta = Number.parseFloat(cryst1Line.substring(40, 47));
        const gamma = Number.parseFloat(cryst1Line.substring(47, 54));

        if ([a, b, c, alpha, beta, gamma].some(isNaN)) {
            console.warn("Parsed CRYST1 values contain NaN:", { a, b, c, alpha, beta, gamma });
            return null;
        }
        return { a, b, c, alpha, beta, gamma };
    } catch (e) {
        console.error("Error parsing CRYST1 line:", e);
        return null;
    }
}

// Function to toggle unit cell visibility
function toggleUnitCell(show) {
    if (!viewer || !mainModel || !mainModel.crystal) {
        console.warn("Cannot toggle unit cell: viewer, mainModel, or mainModel.crystal is missing.");
        return;
    }

    if (show) {
        const crystalData = mainModel.crystal;
        const { a, b, c, alpha, beta, gamma } = crystalData;

        if ([a, b, c, alpha, beta, gamma].some(val => typeof val === 'undefined' || isNaN(val))) {
            console.error("Invalid crystal data for unit cell drawing:", crystalData);
            return;
        }

        // Clear any previously drawn unit cell lines
        if (unitCellModel) {
            viewer.removeModel(unitCellModel); // Remove the previous unit cell model if it was added by 3Dmol.js
            unitCellModel = null;
        }
        viewer.removeAllShapes(); // Remove any manually drawn shapes

        // Convert angles to radians
        const alphaRad = (alpha * Math.PI) / 180;
        const betaRad = (beta * Math.PI) / 180;
        const gammaRad = (gamma * Math.PI) / 180;

        // Calculate vectors for the unit cell axes
        const vecA = { x: a, y: 0, z: 0 };
        const vecB = { x: b * Math.cos(gammaRad), y: b * Math.sin(gammaRad), z: 0 };
        
        // Calculate vecC using the formula for triclinic cells
        const cosAlpha = Math.cos(alphaRad);
        const cosBeta = Math.cos(betaRad);
        const cosGamma = Math.cos(gammaRad);
        const sinGamma = Math.sin(gammaRad);

        const cx = c * cosBeta;
        const cy = c * (cosAlpha - cosBeta * cosGamma) / sinGamma;
        const cz = Math.sqrt(c * c - cx * cx - cy * cy);
        const vecC = { x: cx, y: cy, z: cz };

        // Define the 8 vertices of the unit cell
        const vertices = [
            { x: 0, y: 0, z: 0 }, // 0: origin
            vecA,                 // 1: a
            vecB,                 // 2: b
            vecC,                 // 3: c
            { x: vecA.x + vecB.x, y: vecA.y + vecB.y, z: vecA.z + vecB.z }, // 4: a+b
            { x: vecA.x + vecC.x, y: vecA.y + vecC.y, z: vecA.z + vecC.z }, // 5: a+c
            { x: vecB.x + vecC.x, y: vecB.y + vecC.y, z: vecB.z + vecC.z }, // 6: b+c
            { x: vecA.x + vecB.x + vecC.x, y: vecA.y + vecB.y + vecC.y, z: vecA.z + vecB.z + vecC.z } // 7: a+b+c
        ];

        // Define the 12 edges of the unit cell
        const edges = [
            [0, 1], [0, 2], [0, 3], // Edges from origin
            [1, 4], [1, 5],         // Edges from a
            [2, 4], [2, 6],         // Edges from b
            [3, 5], [3, 6],         // Edges from c
            [4, 7], [5, 7], [6, 7]  // Edges to a+b+c
        ];

        const dashLength = 0.6; // fraction of segment that's visible
        const numSegments = 10; // Number of segments per edge for dashing
        const radius = 0.05; // Thickness of the unit cell lines
        const color = 'magenta'; // Color of the unit cell lines

        // Draw each edge as a dashed line using cylinders
        edges.forEach(([startIdx, endIdx]) => {
            const startPos = vertices[startIdx];
            const endPos = vertices[endIdx];

            for (let i = 0; i < numSegments; i++) {
                const t1 = i / numSegments;
                const t2 = t1 + dashLength / numSegments;

                if (t2 <= 1) {
                    const p1 = {
                        x: startPos.x + t1 * (endPos.x - startPos.x),
                        y: startPos.y + t1 * (endPos.y - startPos.y),
                        z: startPos.z + t1 * (endPos.z - startPos.z),
                    };
                    const p2 = {
                        x: startPos.x + t2 * (endPos.x - startPos.x),
                        y: startPos.y + t2 * (endPos.y - startPos.y),
                        z: startPos.z + t2 * (endPos.z - startPos.z),
                    };

                    viewer.addCylinder({
                        start: p1,
                        end: p2,
                        radius: radius,
                        color: color,
                        alpha: 0.8,
                    });
                }
            }
        });
        console.log("Unit cell drawn manually.");
    } else { // If 'show' is false, remove the unit cell
        viewer.removeAllShapes(); // Remove all manually drawn shapes (unit cell)
        if (unitCellModel) { // If a 3Dmol.js unit cell model was added, remove it
            viewer.removeModel(unitCellModel);
            unitCellModel = null;
        }
        console.log("Unit cell removed.");
        // Reset zoom to model when unit cell is hidden
        if(mainModel) viewer.zoomTo({model: mainModel});
    }
    viewer.render();
}


// Main initialization function for 3Dmol viewer and UI
function init3DmolViewerAndUI() {
    const viewerElement = document.getElementById('viewer');
    if (viewerElement) {
        viewer = $3Dmol.createViewer(viewerElement, {
            defaultcolors: $3Dmol.rasmolColors,
            backgroundColor: 'white',
            antialias: true
        });

        // Fetch PDB content directly to parse CRYST1
        fetch('../static/models/fcc_al.pdb')
            .then(response => response.text())
            .then(pdbText => {
                viewer.addModel(pdbText, 'pdb'); // Add model from text
                mainModel = viewer.getModel(); // Get the newly added model
                console.log("Model loaded from text. mainModel:", mainModel);

                const parsedCrystalData = parseCryst1(pdbText);
                if (parsedCrystalData) {
                    mainModel.crystal = parsedCrystalData;
                    console.log("CRYST1 data parsed and attached to mainModel.crystal:", mainModel.crystal);
                } else {
                    console.warn("No CRYST1 data found or could not be parsed from PDB file.");
                }

                unitCellModel = null; // Reset unitCellModel when a new model is loaded

            // Initialize axes based on toggle state
            const axesToggle = document.getElementById('axes-toggle');
            if (axesToggle) { // Ensure element exists
                toggleViewerAxes(axesToggle.checked);
            } else { // Fallback if toggle not found, show axes
                addViewerAxesManually(viewer, 2.5);
            }

            // Initialize unit cell based on toggle state
            const unitCellToggle = document.getElementById('unit-cell-toggle');
            if (unitCellToggle) {
                console.log("Attempting to initialize unit cell display state based on toggle (will check mainModel inside).");
                toggleUnitCell(unitCellToggle.checked);
            } else {
                 console.warn("Unit cell toggle checkbox not found; unit cell display not initialized.");
            }


            document.getElementById('representation-select').value = 'ballAndStick';
            updateRepresentation('ballAndStick');

            const initialBgColor = document.getElementById('background-color-select').value;
            changeBackgroundColor(initialBgColor);

            // Initial zoom to the model itself, unit cell zoom will be handled by toggleUnitCell
            if(mainModel) viewer.zoomTo({model: mainModel});
            viewer.render(); // Render once after all initial setup

            document.getElementById('representation-select').addEventListener('change', function() {
                updateRepresentation(this.value);
                viewer.render(); // Render only when representation changes
            });
            const axesToggleEventListener = document.getElementById('axes-toggle');
            if (axesToggleEventListener) {
                axesToggleEventListener.addEventListener('change', function() {
                    toggleViewerAxes(this.checked); // toggleViewerAxes already calls render
                });
            }
            const unitCellToggleEventListener = document.getElementById('unit-cell-toggle');
            if (unitCellToggleEventListener) {
                unitCellToggleEventListener.addEventListener('change', function() {
                    toggleUnitCell(this.checked);
                });
            }
            document.getElementById('background-color-select').addEventListener('change', function() {
                changeBackgroundColor(this.value);
                viewer.render(); // Render only when background color changes
            });
            document.getElementById('reset-view-button').addEventListener('click', function() {
                if(viewer && mainModel) {
                    const unitCellToggle = document.getElementById('unit-cell-toggle');
                    if (unitCellToggle && unitCellToggle.checked && mainModel.crystal) {
                        // If unit cell is shown, zoom to include it
                        // No specific anti-clipping, just zoom to model
                        viewer.zoomTo({model: mainModel});
                    } else {
                        // Otherwise, just zoom to the molecule
                        viewer.zoomTo({model: mainModel});
                    }
                    viewer.render();
                }
            });

            viewer.setHoverable({model: mainModel}, true,
                function(atom, currentViewer, event, container) {
                    if(atom) {
                        const labelText = `${atom.elem} ${atom.atom}${atom.resi ? '.'+atom.resi : ''}`;
                        const currentBgSetting = document.getElementById('background-color-select').value;
                        const isDarkBackground = (currentBgSetting === 'black' || currentBgSetting === '#4b5563');
                        const hoverFontColor = isDarkBackground ? 0xFFFFFF : 0x000000;
                        currentViewer.addLabel(labelText, {
                            position: { x: atom.x, y: atom.y, z: atom.z },
                            backgroundColor: isDarkBackground ? 'rgba(50,50,50,0.8)' : 'rgba(220,220,220,0.8)',
                            fontColor: hoverFontColor,
                            showBackground: true, fontSize: 12
                        });
                        currentViewer.render(); // Render to show the label
                    }
                },
                function(atom, currentViewer, event, container) {
                    currentViewer.removeAllLabels();
                    currentViewer.render(); // Render to remove the label
                }
            );
        });

    } else {
        console.error("Viewer element with ID 'viewer' not found.");
    }

    const showControlsBtn = document.getElementById('show-controls-btn');
    const showChatBtn = document.getElementById('show-chat-btn');
    const controlsContentArea = document.getElementById('controls-content-area');
    const chatContentArea = document.getElementById('chat-content-area');

    function setActiveTab(tabToShow) {
        showControlsBtn.classList.remove('bg-indigo-500', 'text-white');
        showControlsBtn.classList.add('bg-gray-200', 'text-gray-700', 'hover:bg-gray-300');
        showChatBtn.classList.remove('bg-indigo-500', 'text-white');
        showChatBtn.classList.add('bg-gray-200', 'text-gray-700', 'hover:bg-gray-300');

        if (tabToShow === 'controls') {
            controlsContentArea.classList.remove('hidden');
            chatContentArea.classList.add('hidden');
            showControlsBtn.classList.remove('bg-gray-200', 'text-gray-700', 'hover:bg-gray-300');
            showControlsBtn.classList.add('bg-indigo-500', 'text-white');
        } else { 
            chatContentArea.classList.remove('hidden');
            controlsContentArea.classList.add('hidden');
            showChatBtn.classList.remove('bg-gray-200', 'text-gray-700', 'hover:bg-gray-300');
            showChatBtn.classList.add('bg-indigo-500', 'text-white');
        }
    }
    setActiveTab('controls'); 
    showControlsBtn.addEventListener('click', () => setActiveTab('controls'));
    showChatBtn.addEventListener('click', () => setActiveTab('chat'));
}
document.addEventListener('DOMContentLoaded', init3DmolViewerAndUI);
