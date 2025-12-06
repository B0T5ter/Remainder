import requests

# wysyłanie zadania
task = {"name": "Nauka Tkinter", "repeat": "Every x"}
res = requests.post("http://127.0.0.1:5000/get_tasks", json=task)
print(res.json())

# pobieranie wszystkich zadań
res = requests.get("http://127.0.0.1:5000/get_tasks")
print(res.json())
