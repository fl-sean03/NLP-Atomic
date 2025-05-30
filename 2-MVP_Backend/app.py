from flask import Flask, jsonify, request
from flask_cors import CORS
from models.commands import generate_commands, validate_commands
from executor.structure import build_structure
from executor.view import compute_set_view, compute_rotate_camera
from nlp.llm_client import LLMClient
from utils.error_handlers import NLPError, ExecutionError
import json

app = Flask(__name__)
CORS(app)

# Define ValidationError if it's not already defined elsewhere
class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

@app.errorhandler(NLPError)
def handle_nlp_error(e):
    return jsonify({"error": str(e)}), 400

@app.errorhandler(ValidationError)
def handle_validation_error(e):
    return jsonify({"error": str(e)}), 400

@app.errorhandler(ExecutionError)
def handle_execution_error(e):
    return jsonify({"error": str(e)}), 500

@app.errorhandler(Exception)
def handle_generic_error(e):
    app.logger.error(f"An unexpected error occurred: {e}", exc_info=True)
    return jsonify({"error": "An unexpected error occurred."}), 500

@app.route("/api/commands", methods=["POST"])
def commands():
    data = request.json
    prompt = data.get("prompt")

    if not prompt:
        raise ValidationError("No prompt provided")

    llm_client = LLMClient()
    try:
        generated_commands_json = llm_client.generate_commands(prompt)
    except Exception as e: # Catching generic exception from LLM client for now, can be refined to NLPError if LLMClient raises it
        raise NLPError(f"Error generating commands from NLP: {str(e)}")

    try:
        generated_commands = json.loads(generated_commands_json)
    except json.JSONDecodeError:
        raise NLPError("Invalid JSON from LLM")

    validation_result = validate_commands(generated_commands)
    if not validation_result["is_valid"]:
        raise ValidationError({"error": "Command validation failed", "details": validation_result["errors"]})

    results = []
    for command in generated_commands["commands"]:
        command_type = command.get("type")
        command_args = command.get("args", {})

        try:
            if command_type == "build_structure":
                result = build_structure(command_args)
            elif command_type == "set_view":
                result = compute_set_view(command_args)
            elif command_type == "rotate_camera":
                result = compute_rotate_camera(command_args)
            else:
                raise ExecutionError(f"Unknown command type: {command_type}")
            results.append(result)
        except Exception as e:
            raise ExecutionError(f"Error executing command {command_type}: {str(e)}")

    return jsonify(results), 200

if __name__ == '__main__':
    app.run(debug=True)