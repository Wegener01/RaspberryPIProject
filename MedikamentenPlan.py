import tkinter as tk
from tkinter import ttk
import pandas as pd
import datetime

def get_current_weekday():
    # Ermittle den aktuellen Wochentag (Montag = 0, Sonntag = 6)
    return datetime.datetime.today().weekday()

def convert_index_to_time(index):
    # Definiere die Zeit entsprechend des Index
    if index == 0:
        return "8:00"
    elif index == 1:
        return "12:00"
    elif index == 2:
        return "16:00"
    elif index == 3:
        return "20:00"
    else:
        return ""

def calculate_remaining_time(index):
    # Berechne die verbleibende Zeit bis zur Einnahme
    current_time = datetime.datetime.now().time()
    med_time = datetime.datetime.strptime(convert_index_to_time(index), "%H:%M").time()
    if med_time > current_time:
        time_difference = datetime.datetime.combine(datetime.date.today(), med_time) - datetime.datetime.combine(datetime.date.today(), current_time)
    else:
        # Wenn die Einnahmezeit bereits vergangen ist, setze die verbleibende Zeit auf 0
        time_difference = datetime.timedelta(hours=0)
    hours = time_difference.seconds // 3600
    minutes = (time_difference.seconds % 3600) // 60
    return f"{hours} Stunden {minutes} Minuten"

def visualize_medication_plan_for_current_day(filename):
    # Lese die Excel-Datei
    df = pd.read_excel(filename)

    # Bestimme den aktuellen Wochentag
    current_weekday = get_current_weekday()

    # Wähle die Spalte für den aktuellen Wochentag aus
    current_day_plan = df.iloc[:, current_weekday + 2]  # Beachte die Korrektur hier

    # Erstelle ein Tkinter-Fenster
    root = tk.Tk()
    root.title("Medikamentenplan für den aktuellen Wochentag")

    # Erstelle eine Treeview zur Anzeige der Daten
    tree = ttk.Treeview(root)
    tree["columns"] = ("Uhrzeit", "Medikament", "Verbleibende Zeit bis zur Einnahme")
    tree["show"] = "headings"

    # Setze die Spaltenüberschriften
    tree.heading("Uhrzeit", text="Uhrzeit")
    tree.heading("Medikament", text="Medikament")
    tree.heading("Verbleibende Zeit bis zur Einnahme", text="Verbleibende Zeit bis zur Einnahme")

    # Füge die Daten als Zeilen hinzu
    shortest_time_diff = None
    shortest_time_index = None
    for index, medication in current_day_plan.items():
        # Wandle den Index in eine Uhrzeit um
        time = convert_index_to_time(index)
        remaining_time = calculate_remaining_time(index)
        tree.insert("", "end", values=(time, medication, remaining_time))
        if remaining_time != "0 Stunden 0 Minuten" and (shortest_time_diff is None or remaining_time < shortest_time_diff):
            shortest_time_diff = remaining_time
            shortest_time_index = index

    # Markiere die Zeile mit der kürzesten verbleibenden Zeit
    if shortest_time_index is not None:
        tree.tag_configure("shortest_time", background="green")
        tree.item(tree.get_children()[shortest_time_index], tags=("shortest_time",))

    # Packe die Treeview in das Fenster
    tree.pack(expand=True, fill="both")

    # Starte die Tkinter Hauptloop
    root.mainloop()

# Beispielaufruf mit Dateiname "medikamentenplan.xlsx"
filename = "medikamentenplan.xlsx"
visualize_medication_plan_for_current_day(filename)
