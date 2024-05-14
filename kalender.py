import tkinter as tk
from tkinter import simpledialog
from datetime import datetime
import locale

# Setze die locale auf Deutsch
locale.setlocale(locale.LC_TIME, "de_DE")


def load_termine(filename):
    termine = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 4:
                    name = parts[0]
                    day = int(parts[1])
                    month = int(parts[2])
                    year = int(parts[3])
                    termine.append((name, day, month, year))
    except FileNotFoundError:
        print(f"Datei '{filename}' nicht gefunden. Neue leere Datei wird erstellt.")
    return termine


def add_termine():
    name = simpledialog.askstring("Neuer termin", "Name eingeben:")
    date_str = simpledialog.askstring("Neuer termin", "Geburtsdatum eingeben (Format: DD-MM-YYYY):")
    try:
        day, month, year = map(int, date_str.split("-"))
        with open("birthdays.txt", "a") as file:
            file.write(f"{name} {day} {month} {year}\n")
        show_date()
    except ValueError as e:
        print("Fehler beim Hinzufügen des termins: ungültiges Datumsformat", e)


def show_date():
    now = datetime.now()
    day = now.strftime("%A")
    date = now.strftime("%d-%m-%Y")
    result_label.config(text=f"Heute ist {day}, {date}")
    show_next_appointment(now, "birthdays.txt", next_label)


def show_next_appointment(now, filename, next_label):
    # Lade Geburtstage aus der Datei
    termine = load_termine(filename)

    # Finde den nächsten Geburtstag
    next_termin = None
    for name, day, month, year in termine:
        termin = datetime(year=now.year, month=month, day=day)
        if termin >= now:
            if next_termin is None or termin < next_termin:
                next_termin = termin

    if next_termin:
        next_date = next_termin.strftime("%A, %d-%m-%Y")
        next_label.config(text=f"Nächster Termin: {next_date}")
    else:
        next_label.config(text="Keine weiteren Termine gefunden")


# GUI erstellen
root = tk.Tk()
root.title("Termine")

# Label für das aktuelle Datum erstellen
result_label = tk.Label(root, font=("Helvetica", 16))
result_label.pack(pady=10)

# Label für den nächsten Geburtstag erstellen
next_label = tk.Label(root, font=("Helvetica", 12))
next_label.pack(pady=10)

# Button zum Hinzufügen eines neuen Geburtstags
add_button = tk.Button(root, text="Neuen Termin hinzufügen", command=add_termine)
add_button.pack(pady=10)

# Button zum Aktualisieren des Datums und des nächsten Geburtstags erstellen
update_button = tk.Button(root, text="Aktualisieren", command=show_date)
update_button.pack(pady=10)

# Aktuelles Datum und nächsten Geburtstag anzeigen
show_date()

# GUI starten
root.mainloop()
