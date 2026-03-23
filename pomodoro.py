import tkinter as tk
from tkinter import messagebox


class Pomodoro(tk.Frame):
    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent, bd=1, relief="solid", padx=10, pady=10)

        self.work_min = tk.IntVar(value=25)
        self.break_min = tk.IntVar(value=5)

        self.remaining = self.work_min.get() * 60
        self.running = False
        self.on_break = False
        self._after_id = None

        tk.Label(self, text="Pomodoro Timer", font=("Arial", 14, "bold")).pack(anchor="w")

        self.phase_var = tk.StringVar(value="Work Session")
        tk.Label(self, textvariable=self.phase_var, font=("Arial", 10)).pack(anchor="w", pady=(4, 6))

        self.time_var = tk.StringVar(value=self.fmt(self.remaining))
        tk.Label(self, textvariable=self.time_var, font=("Consolas", 32, "bold")).pack(pady=(0, 10))

        row = tk.Frame(self)
        row.pack(fill="x", pady=(0, 10))
        tk.Label(row, text="Work (min)").pack(side="left")
        tk.Entry(row, width=5, textvariable=self.work_min).pack(side="left", padx=(6, 16))
        tk.Label(row, text="Break (min)").pack(side="left")
        tk.Entry(row, width=5, textvariable=self.break_min).pack(side="left", padx=(6, 12))
        tk.Button(row, text="Apply", command=self.apply_times).pack(side="left")

        btns = tk.Frame(self)
        btns.pack(fill="x")
        tk.Button(btns, text="Start", command=self.start).pack(side="left")
        tk.Button(btns, text="Pause", command=self.pause).pack(side="left", padx=8)
        tk.Button(btns, text="Reset", command=self.reset).pack(side="left")

    def fmt(self, sec: int) -> str:
        m, s = divmod(max(0, sec), 60)
        return f"{m:02d}:{s:02d}"

    def apply_times(self) -> None:
        try:
            w = int(self.work_min.get())
            b = int(self.break_min.get())
            if w <= 0 or b <= 0:
                raise ValueError
        except Exception:
            messagebox.showerror("Invalid Input", "Work/Break must be positive whole numbers.")
            return
        if not self.running:
            self.reset()

    def start(self) -> None:
        if not self.running:
            self.running = True
            self._tick()

    def pause(self) -> None:
        self.running = False
        if self._after_id is not None:
            self.after_cancel(self._after_id)
            self._after_id = None

    def reset(self) -> None:
        self.pause()
        self.on_break = False
        self.phase_var.set("Work Session")
        self.remaining = int(self.work_min.get()) * 60
        self.time_var.set(self.fmt(self.remaining))

    def _tick(self) -> None:
        if not self.running:
            return

        self.time_var.set(self.fmt(self.remaining))
        if self.remaining <= 0:
            self.running = False
            if not self.on_break:
                self.on_break = True
                self.phase_var.set("Break Session")
                self.remaining = int(self.break_min.get()) * 60
                messagebox.showinfo("Pomodoro", "Work session complete. Take a break.")
            else:
                self.on_break = False
                self.phase_var.set("Work Session")
                self.remaining = int(self.work_min.get()) * 60
                messagebox.showinfo("Pomodoro", "Break complete. Back to work.")
            return

        self.remaining -= 1
        self._after_id = self.after(1000, self._tick)