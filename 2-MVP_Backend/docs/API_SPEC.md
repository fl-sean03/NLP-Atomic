````markdown
# API_SPEC.md

## Table of Contents
1. [Overview](#overview)  
2. [Base URL & Authentication](#base-url--authentication)  
3. [Endpoints](#endpoints)  
   - [POST /api/commands](#post-apicommands)  
4. [Request Format](#request-format)  
   - [Headers](#headers)  
   - [Path & Query Parameters](#path--query-parameters)  
   - [Request Body Schema](#request-body-schema)  
5. [Response Format](#response-format)  
   - [Success Response (200)](#success-response-200)  
   - [Error Responses (4xx / 5xx)](#error-responses-4xx--5xx)  
6. [Command Object Schema](#command-object-schema)  
7. [Examples](#examples)  
   - [Example: Build & View Structure](#example-build--view-structure)  
   - [Example: Error Handling](#example-error-handling)  
8. [Behavioral Notes](#behavioral-notes)  
9. [Versioning & Change Log](#versioning--change-log)  

---

## 1. Overview
The `/api/commands` endpoint is the sole entry point for the backend service. It accepts a single natural-language prompt and returns an ordered array of JSON “command” objects that the frontend will execute in sequence (see [JSON_SCHEMA.md](docs/JSON_SCHEMA.md) for full command definitions).

---

## 2. Base URL & Authentication
- **Base URL:**  
  - Production: `https://api.yourdomain.com`  
  - Staging: `https://staging.api.yourdomain.com`

- **Authentication:**  
  - **None** for V1 (open access within protected network).  
  - In future, an `Authorization: Bearer <API_KEY>` header may be required.

---

## 3. Endpoints

### POST `/api/commands`
Generate and execute natural-language commands.

| Method | Path              | Description                         |
|--------|-------------------|-------------------------------------|
| POST   | `/api/commands`   | Parse prompt → return JSON commands |

---

## 4. Request Format

### Headers
- `Content-Type: application/json`
- *(Optional future)* `Authorization: Bearer <token>`

### Path & Query Parameters
- None

### Request Body Schema
| Field   | Type   | Required | Description                        |
|---------|--------|----------|------------------------------------|
| prompt  | string | Yes      | Raw user input (chat message)      |
| context | array  | No       | Prior commands for multi-turn NLP  |

```jsonschema
{
  "type": "object",
  "properties": {
    "prompt": {
      "type": "string",
      "description": "Natural-language instruction from the user."
    },
    "context": {
      "type": "array",
      "items": { "$ref": "#/definitions/Command" },
      "description": "Optional history of previous commands."
    }
  },
  "required": ["prompt"],
  "definitions": {
    "Command": {
      "type": "object",
      "properties": {
        "command": { "type": "string" },
        "params": { "type": "object" }
      },
      "required": ["command", "params"]
    }
  }
}
````

See **/docs/JSON\_SCHEMA.md** for the authoritative per-command schemas.

---

## 5. Response Format

### Success Response (200)

* **Content-Type:** `application/json`
* **Body:** JSON array of command objects.

```jsonschema
{
  "type": "array",
  "items": { "$ref": "#/definitions/Command" }
}
```

Each `Command` object follows the schema defined in **/docs/JSON\_SCHEMA.md**.

### Error Responses (4xx / 5xx)

On failure, the API returns a single-object JSON with an `error` field.

| Status Code | Meaning                                   |
| ----------- | ----------------------------------------- |
| 400         | Bad Request (e.g. prompt missing)         |
| 422         | Unprocessable Entity (validation failure) |
| 500         | Internal Server Error (execution failure) |
| 502         | Bad Gateway (LLM service unavailable)     |

```json
{
  "error": "Descriptive, user-friendly error message."
}
```

* **Prompt-understanding errors** (e.g. unknown molecule ID) should return **200** with a `displayMessage` command rather than a 4xx status, to allow the frontend to show an inline error.

---

## 6. Command Object Schema

A **Command** object has:

| Property | Type   | Description                                    |
| -------- | ------ | ---------------------------------------------- |
| command  | string | One of the supported command names (see below) |
| params   | object | Parameters object specific to `command`        |

Supported `command` values (with param shapes) include:

* `buildStructure`
* `loadPdb`
* `setRepresentation`
* `setBackgroundColor`
* `rotateCamera`
* `translateCamera`
* `zoom`
* `resetView`
* `toggleAxes`
* `toggleUnitCell`
* `setView`
* `displayMessage`

For full details on each command’s `params` object, see **/docs/JSON\_SCHEMA.md** and **/docs/MODULE\_SPEC.md**.

---

## 7. Examples

### Example: Build & View Structure

**Request:**

```http
POST /api/commands
Content-Type: application/json

{ "prompt": "Build a 3×3×3 FCC Al cell and look down the 111 direction." }
```

**Response (200):**

```json
[
  {
    "command": "buildStructure",
    "params": {
      "format": "pdb",
      "content": "ATOM      1  Al  ..."
    }
  },
  {
    "command": "setView",
    "params": {
      "viewObject": {
        "quaternion": { "x":0.7,"y":0.7,"z":0,"w":0 },
        "translation": { "x":0,"y":0,"z":0 },
        "zoom": 1.1
      }
    }
  }
]
```

### Example: Error Handling

**Request:**

```http
POST /api/commands
Content-Type: application/json

{ "prompt": "Show me graphene structure." }
```

**Response (200):**

```json
[
  {
    "command": "displayMessage",
    "params": {
      "message": "Unsupported lattice type: graphene. Only FCC, BCC, SC supported.",
      "type": "error"
    }
  }
]
```

**Response (400) on malformed JSON:**

```json
{ "error": "Request body must be valid JSON with a 'prompt' field." }
```

---

## 8. Behavioral Notes

* **Statelessness:** Each request is independent. Any required context must be passed via the optional `context` array.
* **Command Ordering:** The frontend executes commands in the array order.
* **Idempotency:** Commands like `setBackgroundColor` and `setView` may be repeated without side effects.
* **Message vs. Error Status:** Use in-band `displayMessage` for user-level feedback; reserve HTTP errors for protocol or system failures.

---

## 9. Versioning & Change Log

* **v1.0** (2025-05-30): Initial release.
* Future versions will be under `/api/v2/commands` with backward-compatible enhancements.

---

> **References:**
>
> * **PLANNING.md**: strategic blueprint
> * **JSON\_SCHEMA.md**: full command & params definitions
> * **MODULE\_SPEC.md**: code-level function contracts
> * **TASK.md**: implementation checklist
> * **ARCHITECTURE.md**: data flow and component diagrams
