# Reminder App

A simple task reminder application with a GUI using Tkinter and a backend server using Flask. It supports daily, weekly, and monthly reminders and can send notifications to Discord via webhook.

---

## Features

- Add, edit, and delete tasks.
- Set tasks to repeat:
  - Every x days
  - Specific days of the week
  - Specific day of the month
- View today's tasks or all tasks in the database.
- Receive notifications on Discord for tasks.
- Clear all tasks in the database.

---

## Client (GUI)

- Built using **Tkinter**.
- Provides forms for adding and editing tasks.
- Dynamic checkboxes and dropdown menus for setting task repetition.
- Pop-up error messages for missing task information.

---

## Server

- Built using **Flask**.
- Stores tasks in a JSON file (`tasks.json`).
- API endpoints:
  - `POST /add_task` — add a new task.
  - `POST /change_task` — edit an existing task.
  - `POST /delete_task` — delete a task.
  - `GET /get_all_tasks` — get all tasks.
  - `GET /get_today_tasks` — get tasks due today.
  - `POST /clear_database` — clear all tasks.
  - `POST /get_specific_tasks` — get task by timestamp.

- Background thread checks the time and sends notifications to Discord when a task is due.

---

## Setup

1. Install dependencies:

```bash
pip install flask requests
```

2. Server:

Setup server on one device

```bash
python server.py
```

3. Client:

Update server ip in client and run it

```bash
python client.py
```
