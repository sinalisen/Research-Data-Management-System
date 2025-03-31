import tkinter as tk
from tkinter import ttk
import os

class ResearchDataManager:
    def __init__(self):
        self.entries = []
        self.filename = "research_data.txt"
    
    def add_entry(self, experiment_name, date, researcher, data_points):
        entry = {"experiment_name": experiment_name, "date": date, "researcher": researcher, "data_points": data_points}
        self.entries.append(entry)
    
    def get_entries(self):
        return self.entries
    
    def update_entry(self, index, experiment_name=None, date=None, researcher=None, data_points=None):
        if 0 <= index < len(self.entries):
            if experiment_name: self.entries[index]["experiment_name"] = experiment_name
            if date: self.entries[index]["date"] = date
            if researcher: self.entries[index]["researcher"] = researcher
            if data_points: self.entries[index]["data_points"] = data_points
    
    def delete_entry(self, index):
        if 0 <= index < len(self.entries):
            del self.entries[index]

    def load_entries_from_file(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                self.entries = [
                    {"experiment_name": line.split(',')[0], "date": line.split(',')[1], "researcher": line.split(',')[2],
                     "data_points": list(map(float, line.strip().split(',')[3:]))}
                    for line in file
                ]
        else:
            print("File not found.")
    
def add_entry(manager, tree):
    experiment_name = input("Enter experiment name: ")
    date = input("Enter date (YYYY-MM-DD): ")
    researcher = input("Enter researcher's name: ")
    data_points = list(map(float, input("Enter data points separated by commas: ").split(',')))
    manager.add_entry(experiment_name, date, researcher, data_points)
    refresh_table(manager, tree)

def update_entry(manager, tree):
    selected_item = tree.selection()
    if selected_item:
        index = tree.index(selected_item[0])
        experiment_name = input("Enter new experiment name (leave blank to keep current): ")
        date = input("Enter new date (leave blank to keep current): ")
        researcher = input("Enter new researcher's name (leave blank to keep current): ")
        data_points = input("Enter new data points separated by commas (leave blank to keep current): ")
        data_points = list(map(float, data_points.split(','))) if data_points else None
        manager.update_entry(index, experiment_name, date, researcher, data_points)
        refresh_table(manager, tree)
    else:
        print("No item selected for update.")

def delete_entry(manager, tree):
    selected_item = tree.selection()
    if selected_item:
        index = tree.index(selected_item[0])
        manager.delete_entry(index)
        refresh_table(manager, tree)
    else:
        print("No item selected for deletion.")

def refresh_table(manager, tree):
    for i in tree.get_children():
        tree.delete(i)
    for entry in manager.get_entries():
        tree.insert("", "end", values=(entry["experiment_name"], entry["date"], entry["researcher"], entry["data_points"]))

def load_entries(manager, tree):
    manager.load_entries_from_file()
    refresh_table(manager, tree)

def sort_by_column(tree, col, descending):
    data = [(tree.set(child, col), child) for child in tree.get_children("")]
    data.sort(reverse=descending)
    for i, (val, child) in enumerate(data):
        tree.move(child, "", i)
    tree.heading(col, command=lambda: sort_by_column(tree, col, not descending))

def main():
    manager = ResearchDataManager()
    
    root = tk.Tk()
    root.title("Research Data Manager")
    
    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True)
    
    columns = ("Experiment Name", "Date", "Researcher", "Data Points")
    tree = ttk.Treeview(frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col, command=lambda c=col: sort_by_column(tree, c, False))
        tree.column(col, anchor="center")
    tree.pack(fill="both", expand=True)
    
    add_button = tk.Button(root, text="Add Entry", command=lambda: add_entry(manager, tree))
    add_button.pack(side="left")
    
    update_button = tk.Button(root, text="Update Entry", command=lambda: update_entry(manager, tree))
    update_button.pack(side="left")
    
    delete_button = tk.Button(root, text="Delete Entry", command=lambda: delete_entry(manager, tree))
    delete_button.pack(side="right")

    load_button = tk.Button(root, text="Load Entries", command=lambda: load_entries(manager, tree))
    load_button.pack(side="right")

    refresh_button = tk.Button(root, text="Refresh Table", command=lambda: refresh_table(manager, tree))
    refresh_button.pack(side="right")
    
    root.mainloop()

if __name__ == "__main__":
    main()
