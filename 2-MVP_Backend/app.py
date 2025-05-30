from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/commands", methods=["POST"])
def commands():
    data = request.json
    return jsonify([]), 200

if __name__ == '__main__':
    app.run(debug=True)