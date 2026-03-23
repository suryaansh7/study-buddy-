import tkinter as tk

from pomodoro import Pomodoro
from quote import QuoteWidget
from task import Todo


def main() -> None:
    root = tk.Tk()
    root.title("Study Buddy")
    root.geometry("520x760")
    root.minsize(480, 680)

    container = tk.Frame(root, padx=12, pady=12)
    container.pack(fill="both", expand=True)

    quote_widget = QuoteWidget(container)
    quote_widget.pack(fill="x", pady=(0, 12))

    pomodoro = Pomodoro(container)
    pomodoro.pack(fill="x", pady=(0, 12))

    todo = Todo(container)
    todo.pack(fill="both", expand=True)

    root.mainloop()


if __name__ == "__main__":
    main()