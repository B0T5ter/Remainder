import tkinter as tk
import requests
from tkinter import messagebox

root = tk.Tk()
root.title("Reminder")
root.geometry("400x500")
SERVERIP = '84.205.172.7'
SERVERPORT = "1002"

#Widgts for showing all task in databse
def all_win():
    for widget in root.winfo_children():
        widget.destroy()

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    
    tk.Label(root, text="Reminder", font=("Arial", 25), anchor="n").grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    tk.Label(root,text = "To do", font=("Arial", 20), anchor="n").grid(row=1, column=0, padx=5, pady=5, sticky="ew")
    
    #Listowanie rzeczy
    listbox = tk.Listbox(root, bg='gray', font=("Arial", 15))
    listbox.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

    res = requests.get(f"http://{SERVERIP}:{SERVERPORT}/get_all_tasks")
    todos = res.json()['tasks']
    idtimestamp = []
    for todo in todos:
        listbox.insert(tk.END, todo['name'])
        idtimestamp.append(todo['timestamp'])

    tk.Button(root, text="Back", command=main_win, font=("Arial", 15)).grid(row=0, column=1, padx=5, pady=5,sticky='ew')
    tk.Button(root, text="Delete",
              command=lambda: messagebox.showerror("Error", "No item selected") 
              if not listbox.curselection() else delete_func(idtimestamp[listbox.curselection()[0]]),
          font=("Arial", 15)).grid(row=1, column=1, padx=5, pady=5, sticky='ew')
    tk.Button(root, text="Edit", command=lambda: messagebox.showerror("Error", "No item selected") 
              if not listbox.curselection() else edit_func(idtimestamp[listbox.curselection()[0]],'all'), font=("Arial", 15)).grid(row=2, column=1, padx=5, pady=5,sticky='ew')
    
#Widgets for editing task
def edit_func(timestamp, backTo):
    req = requests.post(f"http://{SERVERIP}:{SERVERPORT}/get_specific_tasks", json=timestamp)
    data = req.json()
    for widget in root.winfo_children():
        widget.destroy()
    
    wybor = tk.StringVar(root)
    wybor.set(data['repeat'])
    entryoption = tk.StringVar(root)
    entryoption.set(data['repeat'])

    
    pon, wt, sr, cz, pt, sb, nd = tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()

    pon.set(data['daysofweek'][0])
    wt.set(data['daysofweek'][1])
    sr.set(data['daysofweek'][2])
    cz.set(data['daysofweek'][3])
    pt.set(data['daysofweek'][4])
    sb.set(data['daysofweek'][5])
    nd.set(data['daysofweek'][6])
    name = tk.StringVar(root)
    name.set(data['name'])

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    tk.Label(root, text="Adding", font=("Arial", 15), anchor="w").grid(row=0, column=0, padx=5, pady=0, sticky="ew")
    tk.Label(root, text="Name", font=("Arial", 15), anchor="w").grid(row=1, column=0, padx=5, pady=0, sticky="ew")

    tk.Button(root, text="Back", command=lambda: main_win() if backTo != 'all' else all_win(), font=("Arial", 15)).grid(row=0, column=1, padx=5, pady=5, sticky='ew')


    tk.Button(root, text="Change", command=lambda: change_task(nameEntry.get(),wybor.get(),entryoption.get(),pon.get(), wt.get(),sr.get(),cz.get(),pt.get(),sb.get(),nd.get(), data['timestamp'],backTo), font=("Arial", 15)).grid(row=1, column=1, padx=5, pady=5, sticky='ew')


    nameEntry = tk.Entry(root)
    nameEntry.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
    nameEntry.insert(0, data['name'])
    tk.Label(root, text="Repeting", font=("Arial", 15), anchor="w").grid(row=3, column=0, padx=5, pady=5, sticky="ew")
    wybor = tk.StringVar(root)
    wybor.set("None")

    opcje = ["Every x days", "Every x", "Every x day of month"]
    dropdown = tk.OptionMenu(root, wybor, *opcje)
    dropdown.grid(row=4, column=0, padx=5, pady=4, sticky="ew")
    wybor.set(data['repeat'])
    frame_checks = tk.Frame(root)
    frame_checks.grid(row=5, column=0, columnspan=2, sticky="ew")


    check1 = tk.Checkbutton(frame_checks, text="Poniedziałek", variable=pon, anchor='w')
    check2 = tk.Checkbutton(frame_checks, text="Wtorek", variable=wt, anchor='w')
    check3 = tk.Checkbutton(frame_checks, text="Środa", variable=sr, anchor='w')
    check4 = tk.Checkbutton(frame_checks, text="Czwartek", variable=cz, anchor='w')
    check5 = tk.Checkbutton(frame_checks, text="Piątek", variable=pt, anchor='w')
    check6 = tk.Checkbutton(frame_checks, text="Sobota", variable=sb, anchor='w')
    check7 = tk.Checkbutton(frame_checks, text="Niedziela", variable=nd, anchor='w')

    labeloption1 = tk.Label(frame_checks, text="How often (in days)?", font=("Arial", 15), anchor="w")
    labeloption2 = tk.Label(frame_checks, text="Which days?", font=("Arial", 15), anchor="w")
    labeloption3 = tk.Label(frame_checks, text="Which day of month?", font=("Arial", 15), anchor="w")

    entryoption = tk.Entry(frame_checks)
    entryoption.insert(0,data['days'])
    
    def update_checks(*args):
        if wybor.get() == "Every x days":
            for w in frame_checks.winfo_children():
                w.pack_forget()
            labeloption1.pack(anchor='w')
            entryoption.pack(anchor='w',padx=10)

        elif wybor.get() == "Every x":
            for w in frame_checks.winfo_children():
                w.pack_forget()
            labeloption2.pack(anchor='w')
            check1.pack(anchor='w')
            check2.pack(anchor='w')
            check3.pack(anchor='w')
            check4.pack(anchor='w')
            check5.pack(anchor='w')
            check6.pack(anchor='w')
            check7.pack(anchor='w')
        
        elif wybor.get() == "Every x day of month":
            for w in frame_checks.winfo_children():
                w.pack_forget()
            labeloption3.pack(anchor='w')
            entryoption.pack(anchor='w',padx=10)

    
        
    wybor.trace("w", update_checks)
    update_checks()

#Widget for adding task
def add_func():
    for widget in root.winfo_children():
        widget.destroy()
    
    wybor = tk.StringVar(root)
    wybor.set("None")

    entryoption = tk.StringVar(root)
    entryoption.set("None")

    
    pon,wt,sr,cz,pt,sb,nd = tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar()

    name = tk.StringVar(root)
    name.set("None")

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    tk.Label(root, text="Adding", font=("Arial", 15), anchor="w").grid(row=0, column=0, padx=5, pady=0, sticky="ew")
    tk.Label(root, text="Name", font=("Arial", 15), anchor="w").grid(row=1, column=0, padx=5, pady=0, sticky="ew")

    tk.Button(root, text="Back", command=main_win, font=("Arial", 15)).grid(row=0, column=1, padx=5, pady=5,sticky='ew')

    tk.Button(root, text="Add", command=lambda: add_task(nameEntry.get(),wybor.get(),entryoption.get(),pon.get(), wt.get(),sr.get(),cz.get(),pt.get(),sb.get(),nd.get()), font=("Arial", 15)).grid(row=1, column=1, padx=5, pady=5, sticky='ew')


    nameEntry = tk.Entry(root)
    nameEntry.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

    tk.Label(root, text="Repeting", font=("Arial", 15), anchor="w").grid(row=3, column=0, padx=5, pady=5, sticky="ew")
    wybor = tk.StringVar(root)
    wybor.set("None")

    opcje = ["Every x days", "Every x", "Every x day of month"]
    dropdown = tk.OptionMenu(root, wybor, *opcje)
    dropdown.grid(row=4, column=0, padx=5, pady=4, sticky="ew")

    frame_checks = tk.Frame(root)
    frame_checks.grid(row=5, column=0, columnspan=2, sticky="ew")


    check1 = tk.Checkbutton(frame_checks, text="Poniedziałek", variable=pon, anchor='w')
    check2 = tk.Checkbutton(frame_checks, text="Wtorek", variable=wt, anchor='w')
    check3 = tk.Checkbutton(frame_checks, text="Środa", variable=sr, anchor='w')
    check4 = tk.Checkbutton(frame_checks, text="Czwartek", variable=cz, anchor='w')
    check5 = tk.Checkbutton(frame_checks, text="Piątek", variable=pt, anchor='w')
    check6 = tk.Checkbutton(frame_checks, text="Sobota", variable=sb, anchor='w')
    check7 = tk.Checkbutton(frame_checks, text="Niedziela", variable=nd, anchor='w')

    labeloption1 = tk.Label(frame_checks, text="How often (in days)?", font=("Arial", 15), anchor="w")
    labeloption2 = tk.Label(frame_checks, text="Which days?", font=("Arial", 15), anchor="w")
    labeloption3 = tk.Label(frame_checks, text="Which day of month?", font=("Arial", 15), anchor="w")

    entryoption = tk.Entry(frame_checks)
    
    def update_checks(*args):
        if wybor.get() == "Every x days":
            for w in frame_checks.winfo_children():
                w.pack_forget()
            labeloption1.pack(anchor='w')
            entryoption.pack(anchor='w',padx=10)

        elif wybor.get() == "Every x":
            for w in frame_checks.winfo_children():
                w.pack_forget()
            labeloption2.pack(anchor='w')
            check1.pack(anchor='w')
            check2.pack(anchor='w')
            check3.pack(anchor='w')
            check4.pack(anchor='w')
            check5.pack(anchor='w')
            check6.pack(anchor='w')
            check7.pack(anchor='w')
        
        elif wybor.get() == "Every x day of month":
            for w in frame_checks.winfo_children():
                w.pack_forget()
            labeloption3.pack(anchor='w')
            entryoption.pack(anchor='w',padx=10)

    
        
    wybor.trace("w", update_checks)
    update_checks()

#Funcion that send signal to delete specific task
def delete_func(timestamp):
    requests.post(f"http://{SERVERIP}:{SERVERPORT}/delete_task", json={"timestamp": timestamp})
    all_win()

#Funcion that send information to change specific task
def change_task(name = None, wybor= None,entry= None,pon= None,wt= None,sr= None,cz= None,pt= None,sb= None,nd= None, timestamp = None, backTo = None):
    if name == '':
        messagebox.showerror("Error", "Please, provide name")
    elif entry == '' and pon == 0 and wt == 0 and sr == 0 and cz == 0 and pt == 0 and sb == 0 and nd == 0:
        messagebox.showerror("Error", "Please, provide days to remind")
    else:
        task = {'name': name, 'repeat': wybor, 'days': entry, "daysofweek":[pon,wt,sr,cz,pt,sb,nd], 'timestamp':timestamp}
        requests.post(f"http://{SERVERIP}:{SERVERPORT}/change_task", json=task)
        print(backTo)
        if backTo == "all":
            main_win()
        else:
            all_win()
    
#Funcion that adding task
def add_task(name = None, wybor= None,entry= None,pon= None,wt= None,sr= None,cz= None,pt= None,sb= None,nd= None):
    task = {'name': name, 'repeat': wybor, 'days': entry, "daysofweek":[pon,wt,sr,cz,pt,sb,nd]}
    if name == '':
        messagebox.showerror("Error", "Please, provide name")
    elif entry == '' and pon == 0 and wt == 0 and sr == 0 and cz == 0 and pt == 0 and sb == 0 and nd == 0:
        messagebox.showerror("Error", "Please, provide days to remind")
    else:
        requests.post(f"http://{SERVERIP}:{SERVERPORT}/add_task", json=task)
        main_win()

#Widgts for main window that show task for today
def main_win():
    for widget in root.winfo_children():
        widget.destroy()

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    
    tk.Label(root, text="Reminder", font=("Arial", 25), anchor="n").grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    tk.Label(root,text = "To do", font=("Arial", 20), anchor="n").grid(row=1, column=0, padx=5, pady=5, sticky="ew")
    
    #Listowanie rzeczy
    listbox = tk.Listbox(root, bg='gray', font=("Arial", 15))
    listbox.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

    res = requests.get(f"http://{SERVERIP}:{SERVERPORT}/get_today_tasks")
    todos = res.json()
    idtimestamp = []
    for todo in todos:
        listbox.insert(tk.END, todo['name'])
        idtimestamp.append(todo['timestamp'])

    tk.Button(root, text="Add", command=add_func, font=("Arial", 15)).grid(row=1, column=1, padx=5, pady=5,sticky='ew')
    tk.Button(root, text="List all", command=all_win, font=("Arial", 15)).grid(row=0, column=1, padx=5, pady=5,sticky='ew')
    tk.Button(root, text="Edit", command=lambda: messagebox.showerror("Error", "No item selected") 
              if not listbox.curselection() else edit_func(idtimestamp[listbox.curselection()[0]],'all'), font=("Arial", 15)).grid(row=2, column=1, padx=5, pady=5,sticky='ew')
if __name__ == "__main__":
    main_win()
    root.mainloop()
