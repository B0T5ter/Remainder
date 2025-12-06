from flask import Flask, request, jsonify

app = Flask(__name__)
tasks = []

@app.route("/add_task", methods=["POST"])
def add_task():
    data = request.json  # {'name': 'zadanie', 'repeat': 'Every x'}
    tasks.append(data)
    return jsonify({"status": "ok", "tasks": tasks})

@app.route("/get_tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # dostępny w sieci lokalnej
