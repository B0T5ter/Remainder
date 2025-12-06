import requests

# wysyłanie zadania
task = {"name": "Nauka Tkinter", "repeat": "Every x"}
res = requests.post("http://192.168.50.200:5000/add_task", json=task)  # <--- zmieniony endpoint
print(res.json())

# pobieranie wszystkich zadań
res = requests.get("http://192.168.50.200:5000/get_tasks")
print(res.json())
