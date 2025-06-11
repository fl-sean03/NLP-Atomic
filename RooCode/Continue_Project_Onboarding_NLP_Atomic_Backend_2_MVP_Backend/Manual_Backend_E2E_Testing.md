# Manual Backend E2E Testing Report

## Test Case 1: Valid prompt for structure generation

**Command:**
```bash
curl -X POST http://localhost:5000/api/commands -d '{"prompt":"build a 2x2x2 FCC aluminum crystal"}' -H "Content-Type:application/json"
```

**Request Body:**
```json
{"prompt":"build a 2x2x2 FCC aluminum crystal"}
```

**Actual Response:**
```json
["CRYST1    8.100    8.100    8.100  90.00  90.00  90.00 P 1\nMODEL     1\nATOM      1   Al MOL     1       0.000   0.000   0.000  1.00  0.00          AL  \nATOM      2   Al MOL     1       0.000   2.025   2.025  1.00  0.00          AL  \nATOM      3   Al MOL     1       2.025   0.000   2.025  1.00  0.00          AL  \nATOM      4   Al MOL     1       2.025   2.025   0.000  1.00  0.00          AL  \nATOM      5   Al MOL     1       0.000   0.000   4.050  1.00  0.00          AL  \nATOM      6   Al MOL     1       0.000   2.025   6.075  1.00  0.00          AL  \nATOM      7   Al MOL     1       2.025   0.000   6.075  1.00  0.00          AL  \nATOM      8   Al MOL     1       2.025   2.025   4.050  1.00  0.00          AL  \nATOM      9   Al MOL     1       0.000   4.050   0.000  1.00  0.00          AL  \nATOM     10   Al MOL     1       0.000   6.075   2.025  1.00  0.00          AL  \nATOM     11   Al MOL     1       2.025   4.050   2.025  1.00  0.00          AL  \nATOM     12   Al MOL     1       2.025   6.075   0.000  1.00  0.00          AL  \nATOM     13   Al MOL     1       0.000   4.050   4.050  1.00  0.00          AL  \nATOM     14   Al MOL     1       0.000   6.075   6.075  1.00  0.00          AL  \nATOM     15   Al MOL     1       2.025   4.050   6.075  1.00  0.00          AL  \nATOM     16   Al MOL     1       2.025   6.075   4.050  1.00  0.00          AL  \nATOM     17   Al MOL     1       4.050   0.000   0.000  1.00  0.00          AL  \nATOM     18   Al MOL     1       4.050   2.025   2.025  1.00  0.00          AL  \nATOM     19   Al MOL     1       6.075   0.000   2.025  1.00  0.00          AL  \nATOM     20   Al MOL     1       6.075   2.025   0.000  1.00  0.00          AL  \nATOM     21   Al MOL     1       4.050   0.000   4.050  1.00  0.00          AL  \nATOM     22   Al MOL     1       4.050   2.025   6.075  1.00  0.00          AL  \nATOM     23   Al MOL     1       6.075   0.000   6.075  1.00  0.00          AL  \nATOM     24   Al MOL     1       6.075   2.025   4.050  1.00  0.00          AL  \nATOM     25   Al MOL     1       4.050   4.050   0.000  1.00  0.00          AL  \nATOM     26   Al MOL     1       4.050   6.075   2.025  1.00  0.00          AL  \nATOM     27   Al MOL     1       6.075   4.050   2.025  1.00  0.00          AL  \nATOM     28   Al MOL     1       6.075   6.075   0.000  1.00  0.00          AL  \nATOM     29   Al MOL     1       4.050   4.050   4.050  1.00  0.00          AL  \nATOM     30   Al MOL     1       4.050   6.075   6.075  1.00  0.00          AL  \nATOM     31   Al MOL     1       6.075   4.050   6.075  1.00  0.00          AL  \nATOM     32   Al MOL     1       6.075   6.075   4.050  1.00  0.00          AL  \nENDMDL\n"]
```

**Verification:**
The response is `200 OK` and contains a JSON array with a single string element, which appears to be PDB/XYZ content. This matches the expected output for a `buildStructure` command as per `API_SPEC.md` (Section 7. Example: Build & View Structure).

---

## Test Case 2: Valid prompt for camera rotation

**Command:**
```bash
curl -X POST http://localhost:5000/api/commands -d '{"prompt":"rotate the camera 90 degrees around the y-axis"}' -H "Content-Type:application/json"
```

**Request Body:**
```json
{"prompt":"rotate the camera 90 degrees around the y-axis"}
```

**Actual Response:**
```json
[{"quaternion":[0.0,0.7071067811865475,0.0,0.7071067811865476],"translation":[0,0,0],"zoom":1}]
```

**Verification:**
The response is `200 OK` and contains a JSON array with a single object, which appears to be a 3Dmol.js view state object. This matches the expected output for a `rotateCamera` command as per `API_SPEC.md` (Section 7. Example: Build & View Structure, though it shows `setView` which is similar).

---

## Test Case 3: Invalid prompt (e.g., unrecognized command)

**Command:**
```bash
curl -X POST http://localhost:5000/api/commands -d '{"prompt":"do something weird"}' -H "Content-Type:application/json"
```

**Request Body:**
```json
{"prompt":"do something weird"}
```

**Actual Response:**
```json
{"error":"Error generating commands from NLP: LLM did not return a tool call."}
```

**Verification:**
The response is `400 Bad Request` with an error message indicating that the LLM did not return a tool call. This matches the expected `400 Bad Request` for invalid prompts as per `TASK.md` Phase 8.5.

---

## Test Case 4: Invalid command parameters (e.g., missing required field)

**Command:**
```bash
curl -X POST http://localhost:5000/api/commands -d '{"prompt":"build a crystal"}' -H "Content-Type:application/json"
```

**Request Body:**
```json
{"prompt":"build a crystal"}
```

**Actual Response:**
```json
{"error":"Error generating commands from NLP: LLM did not return a tool call."}
```

**Verification:**
The response is `400 Bad Request` with an error message indicating that the LLM did not return a tool call. This matches the expected `400 Bad Request` for invalid command parameters as per `TASK.md` Phase 8.5.
```