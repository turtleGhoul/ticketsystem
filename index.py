import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime
import os
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)

grün = "#7aba28"
grau = "#e9ecef"
black = "#212529"
weiss = "#ffffff"

def ticket_speichern():
    name = entry_kunde.get().strip()
    betrieb = entry_betrieb.get().strip()
    anliegen = entry_anliegen.get("1.0", "end-1c").strip()
    priorität = combo_priorität.get()

    if not name or not anliegen or not betrieb:
        messagebox.showwarning(
            "eingabe fehlt", "bitte alle felder ausfüllen"
        )
        return

    speicherort = os.path.join("tickets", priorität)

    os.makedirs(speicherort, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    betrieb_clean = betrieb.replace(" ", "_")
    filename = f"{timestamp}_{betrieb_clean}.csv"

    pfad = os.path.join(speicherort, filename)

    with open(
        pfad, mode="w", newline="", encoding="utf-8"
    ) as datei:
        writer = csv.writer(datei, delimiter=";")

        writer.writerow(
            ["erstellt am", "name", "betrieb", "priorität", "anliegen"]
        )
        writer.writerow(
            [timestamp, name, betrieb, priorität, anliegen]
        )

        messagebox.showinfo(
            "gesendet",
            f"ticket wurde erfolgreich erstellt"
        )

        entry_kunde.delete(0, "end")
        entry_betrieb.delete(0, "end")
        entry_anliegen.delete("1.0", "end")
        combo_priorität.set("mittel")

        print("neues ticket eingegangen!")



fenster = tk.Tk()
fenster.title("support")
fenster.geometry("400x700")
fenster.resizable(False, False)
fenster.configure(bg=grau)

style = ttk.Style()
style.theme_use("vista")
style.configure(
    "TLabel",
    background=grau,
    foreground=black
)

label_main = ttk.Label(
    fenster,
    text="support ticket",
    font=("Arial", 16, "bold"),
    foreground=grün
)
label_main.pack(pady=20)

label_name = ttk.Label(
    fenster,
    text="name:"
)
label_name.pack(pady=(10,2))

entry_kunde = tk.Entry(
    fenster,
    width=30,
    font=("Segoe UI", 10),
    relief="solid"
)
entry_kunde.pack(pady=5)

label_betrieb = ttk.Label(
    fenster,
    text="firma:"
)
label_betrieb.pack(pady=(10,2))

entry_betrieb = tk.Entry(
    fenster,
    width=30,
    font=("Segoe UI", 10),
    relief="solid"
)
entry_betrieb.pack(pady=5)

label_anliegen = ttk.Label(
    fenster,
    text="anliegen:"
)
label_anliegen.pack(pady=(10,2))

frame_anliegen = tk.Frame(
    fenster,
    bg=grau
)
frame_anliegen.pack(pady=5)

scrollbar =tk.Scrollbar(
    frame_anliegen,
    orient="vertical"
)
scrollbar.pack(side="right", fill="y")

entry_anliegen = tk.Text(
    frame_anliegen,
    width=30,
    height=6,
    font=("Segoe UI", 10),
    bg=weiss,
    fg=black,
    insertbackground=black,
    bd=1,
    relief="solid",
    yscrollcommand=scrollbar.set
)

scrollbar.config(command=entry_anliegen.yview)
entry_anliegen.pack(side="left", fill="both", expand=True)

label_priorität = ttk.Label(
    fenster,
    text="dringlichkeit"
)
label_priorität.pack(pady=(15, 2), anchor="w", padx=45)

combo_priorität = ttk.Combobox(
    fenster,
    values=["niedrig", "normal", "hoch"],
    state="readonly",
    font=("Segoe UI", 10)
)
combo_priorität.set("normal")
combo_priorität.pack(pady=5)

style.configure("send.TButton", background=grün, foreground=grün, font=("Segoe UI", 11, "bold"), borderwidth=0, focusthickness=0)
style.map("send.TButton", background=[("active", "#62971f")])

button_send = ttk.Button(fenster, text="senden", style="send.TButton", cursor="hand2", command=ticket_speichern, width=40)
button_send.pack(pady=25, ipady=5)

fenster.mainloop()
