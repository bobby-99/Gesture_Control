from flask import Flask, request, jsonify
from flask_cors import CORS
from gesture_controller import process_gesture, get_status

app = Flask(__name__)
CORS(app)

@app.route("/gesture", methods=["POST"])
def gesture_api():
    data = request.json
    return jsonify(process_gesture(data.get("gesture")))

@app.route("/status", methods=["GET"])
def status_api():
    return jsonify(get_status())

if __name__ == "__main__":
    app.run(port=5000, debug=True)