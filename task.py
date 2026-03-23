import json
from pathlib import Path
import tkinter as tk


class Todo(tk.Frame):
    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent, bd=1, relief="solid", padx=10, pady=10)

        self.data_file = Path(__file__).with_name("data.json")
        self.tasks = self.load_tasks()

        tk.Label(self, text="To-Do List", font=("Arial", 14, "bold")).pack(anchor="w", pady=(0, 8))

        entry_row = tk.Frame(self)
        entry_row.pack(fill="x", pady=(0, 8))
        self.entry = tk.Entry(entry_row)
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        tk.Button(entry_row, text="Add Task", command=self.add_task).pack(side="right")

        list_row = tk.Frame(self)
        list_row.pack(fill="both", expand=True)
        self.listbox = tk.Listbox(list_row, selectmode=tk.SINGLE)
        self.listbox.pack(side="left", fill="both", expand=True)
        scrollbar = tk.Scrollbar(list_row, command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        btn_row = tk.Frame(self)
        btn_row.pack(fill="x", pady=(8, 0))
        tk.Button(btn_row, text="Mark Complete", command=self.mark_completed).pack(side="left")
        tk.Button(btn_row, text="Delete Selected", command=self.delete_task).pack(side="left", padx=8)

        self.refresh_tasks()

    def load_tasks(self) -> list[str]:
        if not self.data_file.exists():
            self.data_file.write_text("[]", encoding="utf-8")
            return []
        try:
            data = json.loads(self.data_file.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except Exception:
            return []

    def save_tasks(self) -> None:
        self.data_file.write_text(json.dumps(self.tasks, indent=2), encoding="utf-8")

    def refresh_tasks(self) -> None:
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            self.listbox.insert(tk.END, task)

    def add_task(self) -> None:
        text = self.entry.get().strip()
        if text:
            self.tasks.append(text)
            self.save_tasks()
            self.refresh_tasks()
            self.entry.delete(0, tk.END)

    def delete_task(self) -> None:
        sel = self.listbox.curselection()
        if sel:
            del self.tasks[sel[0]]
            self.save_tasks()
            self.refresh_tasks()

    def mark_completed(self) -> None:
        sel = self.listbox.curselection()
        if sel:
            i = sel[0]
            if not self.tasks[i].startswith("✓ "):
                self.tasks[i] = "✓ " + self.tasks[i]
                self.save_tasks()
                self.refresh_tasks()