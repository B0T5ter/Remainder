from flask import Flask, request, jsonify
import json
import time
from datetime import datetime
import threading
import requests

app = Flask(__name__)

filename = "tasks.json"

def add_to_json(name, repeat,days,daysofweek):
    with open(filename, "r") as f:
        data = json.load(f)
    timestamp = time.time()  
    data['tasks'].append({'name': name, 'repeat': repeat, 'days': days, "daysofweek":daysofweek, 'timestamp':timestamp})

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

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

@app.route("/get_specific_tasks", methods=["POST"])
def get_specific_tasks():
    specific_data = request.json
    print(specific_data)
    with open(filename, "r") as f:
        data = json.load(f)
    
    for task in data['tasks']:
        if task['timestamp'] == specific_data:
            return jsonify(task)
        
@app.route("/get_today_tasks", methods=["GET"])
def get_today_tasks():
    taskstoreturn = []
    with open(filename, "r") as f:
            data = json.load(f)

            for task in data["tasks"]:
                if task["repeat"] == "Every x days":
                    days_passed = int((time.time() - task['timestamp']) / (24*60*60))
                    if days_passed%task["days"] == 0:
                        taskstoreturn.append(task)


                elif task["repeat"] == "Every x":
                    dayofweek = datetime.now().weekday()
                    if task['daysofweek'][dayofweek] == 1:
                        taskstoreturn.append(task)

                if task["repeat"] == "Every x day of month":
                    dayofmonth = datetime.now().day
                    if task["days"] == dayofmonth:
                        taskstoreturn.append(task)
    return jsonify(taskstoreturn)

def checkTask():
    while True:
        if datetime.now().hour in [0,12,16,20] and datetime.now().second == 0 and datetime.now().min == 0:
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

def sendNotification(task):
    print(task["name"])
    webhook_url = 'https://discord.com/api/webhooks/1446938714520420443/MJbFXdq9rdM3AJ60hw7sXqpOn0-Vor0uj2VWxLzcey4yV0PxyIsF2HDzPfNZaw0IUJ4W'
    requests.post(webhook_url, json={"content": task["name"]})

def backgroundcheck():
    thread = threading.Thread(target=checkTask, daemon=True)
    thread.start()

if __name__ == "__main__":
    backgroundcheck()
    app.run(host="0.0.0.0", port=5000)  # dostępny w sieci lokalnej
