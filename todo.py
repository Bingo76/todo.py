import tkinter as tk
from tkinter import messagebox
import json
import os

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.configure(bg='#2e2e2e')
        self.tasks = []

        self.load_tasks()


        self.frame = tk.Frame(self.root, bg='#2e2e2e')
        self.frame.pack(pady=10)

        self.task_entry = tk.Entry(self.frame, width=40, bg='#3e3e3e', fg='#d3d3d3', insertbackground='white')
        self.task_entry.pack(side=tk.LEFT, padx=10)
        self.add_task_button = tk.Button(self.frame, text="Add Task", command=self.add_task, bg='#3e3e3e', fg='#d3d3d3')
        self.add_task_button.pack(side=tk.LEFT)

        self.clear_task_button = tk.Button(self.frame, text="Clear Tasks", command=self.clear_tasks, bg='#3e3e3e', fg='#d3d3d3')
        self.clear_task_button.pack(side=tk.LEFT, padx=10)


        self.task_frame = tk.Frame(self.root, bg='#2e2e2e')
        self.task_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.canvas = tk.Canvas(self.task_frame, borderwidth=0, bg='#2e2e2e', highlightthickness=0)
        self.task_list_frame = tk.Frame(self.canvas, bg='#2e2e2e')
        self.scrollbar = CustomScrollbar(self.task_frame, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.task_list_frame, anchor="nw", tags="self.task_list_frame")

        self.task_list_frame.bind("<Configure>", self.on_frame_configure)

        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.task_frame.grid_rowconfigure(0, weight=1)
        self.task_frame.grid_columnconfigure(0, weight=1)

        self.load_existing_tasks()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def add_task(self):
        task_text = self.task_entry.get()
        if task_text:
            self.create_task(task_text)
            self.task_entry.delete(0, tk.END)
            self.save_tasks()
        else:
            messagebox.showwarning("Warning", "You must enter a task.")

    def create_task(self, task_text):
        var = tk.BooleanVar()
        checkbox = tk.Checkbutton(self.task_list_frame, text=task_text, variable=var, bg='#2e2e2e', fg='#d3d3d3', selectcolor='#2e2e2e', activebackground='#2e2e2e', activeforeground='#d3d3d3')
        checkbox.var = var
        checkbox.config(command=lambda cb=checkbox: self.update_task_status(cb))
        checkbox.pack(anchor="w")
        self.tasks.append((task_text, checkbox))

    def update_task_status(self, checkbox):
        if checkbox.var.get():
            checkbox.config(fg="gray", selectcolor='#2e2e2e', state=tk.DISABLED)
        self.save_tasks()

    def remove_task(self, task_text, checkbox):
        checkbox.destroy()
        self.tasks.remove((task_text, checkbox))
        self.save_tasks()

    def load_tasks(self):
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r") as file:
                self.tasks_data = json.load(file)
        else:
            self.tasks_data = []

    def save_tasks(self):
        with open("tasks.json", "w") as file:
            json.dump([(task_text, checkbox.var.get()) for task_text, checkbox in self.tasks], file)

    def load_existing_tasks(self):
        for task_text, completed in self.tasks_data:
            self.create_task(task_text)
            if completed:
                checkbox = self.tasks[-1][1]
                checkbox.select()
                checkbox.config(fg="gray", selectcolor='#2e2e2e', state=tk.DISABLED)

    def clear_tasks(self):
        # Backs up the current tasks
        if os.path.exists("tasks.json"):
            os.rename("tasks.json", "tasks_old.json")
        
        for task_text, checkbox in self.tasks[:]:
            checkbox.destroy()
        self.tasks.clear()

        self.save_tasks()

class CustomScrollbar(tk.Scrollbar):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
