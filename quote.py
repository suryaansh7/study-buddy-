from pathlib import Path
import random
import tkinter as tk


class QuoteWidget(tk.Frame):
    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent, bd=1, relief="solid", padx=10, pady=10)

        self.quotes = self.load_quotes()

        title = tk.Label(self, text="Daily Motivation", font=("Arial", 14, "bold"))
        title.pack(anchor="w")

        self.quote_var = tk.StringVar(value=random.choice(self.quotes))
        self.quote_label = tk.Label(
            self,
            textvariable=self.quote_var,
            wraplength=460,
            justify="left",
            font=("Arial", 11),
        )
        self.quote_label.pack(fill="x", pady=(8, 10))

        tk.Button(self, text="New Quote", command=self.change_quote).pack(anchor="e")

    def load_quotes(self) -> list[str]:
        path = Path(__file__).with_name("quotes.txt")

        if not path.exists():
            return [
                "Focus on progress, not perfection.",
                "Small steps every day add up.",
                "Discipline beats motivation.",
            ]
        lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines()]
        lines = [line for line in lines if line]
        return lines or ["Keep going."]

    def change_quote(self) -> None:
        self.quote_var.set(random.choice(self.quotes))