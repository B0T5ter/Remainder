from flask import Flask, request, jsonify
import json
import time
from datetime import datetime
import threading
import requests

app = Flask(__name__)

filename = "tasks.json"


#Adding task to file
@app.route("/add_task", methods=["POST"])
def add_task():
    data = request.json
    add_to_json(
    data["name"],
    data["repeat"],
    data["days"],
    data["daysofweek"]
    
    )
    return jsonify({"status": "ok"})

#Getting specific task data
@app.route("/get_specific_tasks", methods=["POST"])
def get_specific_tasks():
    specific_data = request.json
    print(specific_data)
    with open(filename, "r") as f:
        data = json.load(f)
    
    for task in data['tasks']:
        if task['timestamp'] == specific_data:
            return jsonify(task)

#Changing specific task
@app.route("/change_task", methods=["POST"])
def change_task():
    specific_data = request.json

    with open(filename, "r") as f:
        data = json.load(f)
    
    for task in data['tasks']:
        if task['timestamp'] == specific_data['timestamp']:
            task['name'] = specific_data['name']
            task['repeat'] = specific_data['repeat']
            task['days'] = specific_data['days']
            task['daysofweek'] = specific_data['daysofweek']
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)
            return jsonify({"status": "ok"})

#Deleting choosen task
@app.route("/delete_task", methods=["POST"])
def delete_task():
    specific_data = request.json
    ts_to_delete = specific_data['timestamp']

    with open(filename, "r") as f:
        data = json.load(f)

    data['tasks'] = [task for task in data['tasks'] if task['timestamp'] != ts_to_delete]

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    return jsonify({"status": "ok"})

#Getting all tasks
@app.route("/get_all_tasks", methods=["GET"])
def get_all_tasks():
    with open(filename, "r") as f:
        data = json.load(f)

        return jsonify(data)

#Clearing database
@app.route("/clear_database", methods=["POST"])
def clear_database():
    with open(filename, "w") as f:
        json.dump({"tasks": []}, f, indent=4)
    return jsonify({"status": "cleared"})

#Getting tasks for today
@app.route("/get_today_tasks", methods=["GET"])
def get_today_tasks():
    taskstoreturn = []
    with open(filename, "r") as f:
            data = json.load(f)

            for task in data["tasks"]:
                if task["repeat"] == "Every x days":
                    days_passed = int((time.time() - task['timestamp']) / (24*60*60))
                    if days_passed%int(task["days"]) == 0:
                        taskstoreturn.append(task)


                elif task["repeat"] == "Every x":
                    dayofweek = datetime.now().weekday()
                    if task['daysofweek'][dayofweek] == 1:
                        taskstoreturn.append(task)

                if task["repeat"] == "Every x day of month":
                    dayofmonth = datetime.now().day
                    if int(task["days"]) == dayofmonth:
                        taskstoreturn.append(task)
    return jsonify(taskstoreturn)

#Checking if it is time to notification
def checkTask():
    while True:
        if datetime.now().hour in [0,12,16,20] and datetime.now().second == 0 and datetime.now().minute  == 0:
            with open(filename, "r") as f:
                data = json.load(f)

            for task in data["tasks"]:
                if task["repeat"] == "Every x days":
                    days_passed = int((time.time() - task['timestamp']) / (24*60*60))
                    if days_passed%task["days"] == 0:
                        sendNotification(task)

                elif task["repeat"] == "Every x":
                    dayofweek = datetime.now().weekday()
                    if task['daysofweek'][dayofweek] == 1:
                        sendNotification(task)

                if task["repeat"] == "Every x day of month":
                    dayofmonth = datetime.now().day
                    if task["days"] == dayofmonth:
                        sendNotification(task)
            time.sleep(1)

#Sending notification(in my case on discord)
def sendNotification(task):
    with open('discord_webhoo.txt', 'r') as f:
        webhook_url = f.read()
    requests.post(webhook_url, json={"content": task["name"]})

#Adding new task to file
def add_to_json(name, repeat,days,daysofweek):
    with open(filename, "r") as f:
        data = json.load(f)
    timestamp = time.time()  
    data['tasks'].append({'name': name, 'repeat': repeat, 'days': days, "daysofweek":daysofweek, 'timestamp':timestamp})

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

#Thread for checking time
def backgroundcheck():
    thread = threading.Thread(target=checkTask, daemon=True)
    thread.start()


if __name__ == "__main__":
    backgroundcheck()
    app.run(host="0.0.0.0", port=443, ssl_context=('cert.pem', 'key.pem'))

