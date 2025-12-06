from flask import Flask, request, jsonify
import json
app = Flask(__name__)

filename = "tasks.json"

def add_to_json(name, repeat,days,daysofweek):
    with open(filename, "r") as f:
        data = json.load(f)

    data['tasks'].append({'name': name, 'repeat': repeat, 'days': days, "daysofweek":daysofweek})

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/add_task", methods=["POST"])
def add_task():
    data = request.json
    add_to_json(data)

@app.route("/get_tasks", methods=["GET"])
def get_tasks():
    #return jsonify(tasks)
    pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # dostępny w sieci lokalnej
