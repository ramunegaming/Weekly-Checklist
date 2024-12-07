import tkinter as tk
from tkinter import messagebox
import json
import os

class CompactWeekdayChecklist:
    def __init__(self, master):
        self.master = master
        master.title("Weekday Checklist")
        master.resizable(False, False)
        
        # Set window to be always on top
        master.attributes('-topmost', True)

        self.days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
        self.checkboxes = []
        self.vars = []

        # Load saved state
        self.load_state()

        # Frame for checkboxes
        checkbox_frame = tk.Frame(master)
        checkbox_frame.pack(pady=2)

        for i, day in enumerate(self.days):
            var = tk.BooleanVar(value=self.state.get(day, False))
            cb = tk.Checkbutton(checkbox_frame, text=day, variable=var, command=self.check_all_checked)
            cb.grid(row=0, column=i, padx=2)
            self.checkboxes.append(cb)
            self.vars.append(var)

        # Add a button to toggle 'always on top' behavior
        self.toggle_button = tk.Button(master, text="Toggle Top", command=self.toggle_always_on_top)
        self.toggle_button.pack(pady=2)

        # Adjust window size to fit content
        master.update()
        master.geometry(f"{master.winfo_reqwidth()}x{master.winfo_reqheight()}")

    def check_all_checked(self):
        self.save_state()
        if all(var.get() for var in self.vars):
            messagebox.showinfo("Congratulations!", "You've completed all tasks for the week!")
            self.reset_checkboxes()

    def reset_checkboxes(self):
        for var in self.vars:
            var.set(False)
        self.save_state()

    def toggle_always_on_top(self):
        current_state = self.master.attributes('-topmost')
        self.master.attributes('-topmost', not current_state)
        if current_state:
            self.toggle_button.config(text="Set Top")
        else:
            self.toggle_button.config(text="Unset Top")

    def save_state(self):
        self.state = {day: var.get() for day, var in zip(self.days, self.vars)}
        with open('checklist_state.json', 'w') as f:
            json.dump(self.state, f)

    def load_state(self):
        if os.path.exists('checklist_state.json'):
            with open('checklist_state.json', 'r') as f:
                self.state = json.load(f)
        else:
            self.state = {day: False for day in self.days}

def main():
    root = tk.Tk()
    app = CompactWeekdayChecklist(root)
    root.mainloop()

if __name__ == "__main__":
    main()