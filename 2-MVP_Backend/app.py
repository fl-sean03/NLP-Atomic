from flask import Flask, jsonify, request
from flask_cors import CORS
from models.commands import validate_commands, BuildStructureParams, RotateCameraParams
from executor.structure import build_structure
from executor.view import compute_set_view, compute_rotate_camera
from nlp.llm_client import generate_commands
from utils.error_handlers import NLPError, ExecutionError
import json
import time
from functools import wraps

app = Flask(__name__)
CORS(app)

def timing_decorator(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        time1 = time.time()
        result = f(*args, **kwargs)
        time2 = time.time()
        app.logger.info(f"Request took {round((time2-time1)*1000, 2)} ms")
        return result
    return wrap

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
@timing_decorator
def commands():
    data = request.json
    prompt = data.get("prompt")

    if not prompt:
        raise ValidationError("No prompt provided")

    try:
        generated_commands = generate_commands(prompt)
    except Exception as e: # Catching generic exception from LLM client for now, can be refined to NLPError if LLMClient raises it
        raise NLPError(f"Error generating commands from NLP: {str(e)}")

    try:
        validated_commands = validate_commands(generated_commands)
    except ValueError as e:
        raise ValidationError({"error": "Command validation failed", "details": str(e)})

    results = []
    for command in validated_commands:
        command_type = command.command
        command_args = command.params.model_dump()

        try:
            if command_type == "buildStructure":
                build_params = BuildStructureParams(**command_args)
                result = build_structure(build_params)
            elif command_type == "set_view":
                result = compute_set_view(command_args)
            elif command_type == "rotateCamera":
                rotate_params = RotateCameraParams(**command_args)
                result = compute_rotate_camera(rotate_params)
            else:
                raise ExecutionError(f"Unknown command type: {command_type}")
            results.append(result)
        except Exception as e:
            raise ExecutionError(f"Error executing command {command_type}: {str(e)}")

    return jsonify(results), 200

if __name__ == '__main__':
    app.run(debug=True)