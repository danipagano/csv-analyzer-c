import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def run_pa1(file_path, row_or_col, index):
    try:
        result = subprocess.run(
            ["./pa1", file_path, row_or_col, str(index)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

def browse_file():
    filename = filedialog.askopenfilename(
        title="Select CSV File",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )
    if filename:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, filename)

def process():
    file_path = entry_file.get()
    row_or_col = var_type.get()
    index = entry_index.get()
    if not file_path or not row_or_col or not index.isdigit():
        set_status("All fields must be filled correctly.", "red")
        return
    output = run_pa1(file_path, row_or_col, index)
    set_status(output, "green" if "Error" not in output.lower() else "red")

def set_status(msg, color):
    label_status.config(text=msg, fg=color)

def center_window(win):
    win.update_idletasks()
    w = win.winfo_width()
    h = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (w // 2)
    y = (win.winfo_screenheight() // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')

root = tk.Tk()
root.title("CSV Analyzer")

font_main = ("Segoe UI", 12)
pad = {'padx': 8, 'pady': 6}

frame = ttk.Frame(root, padding="18 12 18 12")
frame.grid(row=0, column=0, sticky="nsew")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

ttk.Label(frame, text="CSV File:", font=font_main).grid(row=0, column=0, sticky="e", **pad)
entry_file = ttk.Entry(frame, width=38, font=font_main)
entry_file.grid(row=0, column=1, **pad)
ttk.Button(frame, text="Browse", command=browse_file).grid(row=0, column=2, **pad)

ttk.Label(frame, text="Type:", font=font_main).grid(row=1, column=0, sticky="e", **pad)
var_type = tk.StringVar(value="r")
ttk.Radiobutton(frame, text="Row", variable=var_type, value="r").grid(row=1, column=1, sticky="w", **pad)
ttk.Radiobutton(frame, text="Column", variable=var_type, value="c").grid(row=1, column=2, sticky="w", **pad)

ttk.Label(frame, text="Index:", font=font_main).grid(row=2, column=0, sticky="e", **pad)
entry_index = ttk.Entry(frame, width=6, font=font_main)
entry_index.grid(row=2, column=1, sticky="w", **pad)

ttk.Button(frame, text="Process", command=process).grid(row=3, column=0, columnspan=3, pady=14)

label_status = tk.Label(frame, text="", font=font_main, anchor="w", fg="black", bg="#f8f8f8", wraplength=400, justify="left")
label_status.grid(row=4, column=0, columnspan=3, sticky="ew", **pad)

center_window(root)
root.resizable(False, False)
root.mainloop()
