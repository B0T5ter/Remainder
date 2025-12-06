import tkinter as tk
import requests

root = tk.Tk()
root.title("Moja apka")
root.geometry("400x500")

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

def add_task(name = None, wybor= None,entry= None,pon= None,wt= None,sr= None,cz= None,pt= None,sb= None,nd= None):
        task = {'name': name, 'repeat': wybor, 'days': entry, "daysofweek":[pon,wt,sr,cz,pt,sb,nd]}

        print(task)
        requests.post("http://192.168.50.200:5000/add_task", json=task)
def main_win():
    for widget in root.winfo_children():
        widget.destroy()

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    tk.Label(root, text="Remainder", font=("Arial", 25), anchor="e").grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    tk.Label(root, text="To do", font=("Arial", 20), anchor="w").grid(row=1, column=0, padx=5, pady=5, sticky="ew")
    tk.Label(root, text="ToDOs\nToDOs\nToDOs\nToDOs\nToDOs\nToDOs\n", bg='gray', font=("Arial", 15), anchor="w").grid(row=3, column=0, padx=5, pady=5, sticky="ew")

    tk.Button(root, text="Add", command=add_func, font=("Arial", 15)).grid(row=1, column=1, padx=5, pady=5,sticky='ew')
    tk.Button(root, text="List all", command=add_func, font=("Arial", 15)).grid(row=2, column=1, padx=5, pady=5,sticky='ew')
if __name__ == "__main__":
    main_win()
    root.mainloop()
