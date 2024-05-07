import tkinter as tk
from datetime import datetime
import math

class Demenzuhr(tk.Tk):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Demenzuhr")
        self.geometry("1024x600")  # Größe anpassen je nach Display-Auflösung

        self.analog_uhr = AnalogUhr(self)
        self.analog_uhr.pack(pady=20)

        self.digital_uhr = tk.Label(self, text="", font=("Helvetica", 48))
        self.digital_uhr.pack()

        self.tag_zeit = tk.Label(self, text="", font=("Helvetica", 24))
        self.tag_zeit.pack()

        self.datum_anzeige = tk.Label(self, text="", font=("Helvetica", 24))
        self.datum_anzeige.pack(pady=20, padx=20, side=tk.TOP)  # Unterhalb der digitalen Uhr platzieren

        self.update_time()

    def update_time(self):
        now = datetime.now()

        # Analoge Uhr aktualisieren
        self.analog_uhr.update(now)

        # Digitale Uhr aktualisieren
        digital_time = now.strftime("%H:%M:%S")
        self.digital_uhr.config(text=digital_time)

        # Datumsanzeige aktualisieren
        formatted_date = self.translate_date(now.strftime("%d. %B %Y"))  # Datumsformat: z.B. "7. Mai 2024"
        self.datum_anzeige.config(text=formatted_date)

        # Tageszeit und Wochentag
        day_of_week = now.strftime("%A")  # Wochentag in Englisch
        german_day_of_week = self.translate_day(day_of_week)  # Übersetzen in Deutsch
        part_of_day = self.get_part_of_day(now.hour)  # Tageszeit
        self.tag_zeit.config(text=f"{german_day_of_week} {part_of_day}")

        self.after(1000, self.update_time)  # Alle 1000ms (1 Sekunde) aktualisieren

    def translate_day(self, english_day):
        # Übersetzung der Wochentage
        days_dict = {
            "Monday": "Montag",
            "Tuesday": "Dienstag",
            "Wednesday": "Mittwoch",
            "Thursday": "Donnerstag",
            "Friday": "Freitag",
            "Saturday": "Samstag",
            "Sunday": "Sonntag"
        }
        return days_dict.get(english_day, english_day)  # Rückgabe des übersetzten Tages oder Original
    
    def translate_date(self, english_date):
        # Übersetzung der Monatsnamen
        months_dict = {
            "January": "Januar",
            "February": "Februar",
            "March": "März",
            "April": "April",
            "May": "Mai",
            "June": "Juni",
            "July": "Juli",
            "August": "August",
            "September": "September",
            "October": "Oktober",
            "November": "November",
            "December": "Dezember"
        }
        
        # Datumsstring vorbereiten
        cleaned_date = english_date.strip()  # Leerzeichen entfernen
        parts = cleaned_date.split()
        day = parts[0].lstrip("0")  # Führende Nullen vom Tag entfernen
        translated_month = months_dict.get(parts[1], parts[1])  # Übersetzen des Monatsnamens
        year = parts[2]  # Jahr unverändert übernehmen

        return f"{day} {translated_month} {year}"  # Formatieren des Datums



    def get_part_of_day(self, hour):
        if 6 <= hour < 12:
            return "morgens"
        elif 12 <= hour < 18:
            return "nachmittags"
        elif 18 <= hour < 24:
            return "abends"
        else:
            return "nachts"

class AnalogUhr(tk.Canvas):
    def __init__(self, master, size=300, bg="white"):
        super().__init__(master, width=size, height=size, bg=bg)
        self.size = size
        self.draw_face()

    def draw_face(self):
        self.delete("all")
        center_x, center_y = self.size / 2, self.size / 2
        radius = self.size / 3

        self.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, width=4)

        for i in range(60):
            angle = math.radians(360 * i / 60 - 90)  # Umrechnung in Bogenmaß, Start bei 12 Uhr (-90 Grad)
            length_ratio = 0.85 if i % 5 == 0 else 0.9  # Länge der Stunden- und Minutenmarkierungen
            x1 = center_x + radius * length_ratio * math.cos(angle)
            y1 = center_y + radius * length_ratio * math.sin(angle)
            x2 = center_x + radius * math.cos(angle)
            y2 = center_y + radius * math.sin(angle)

            if i % 5 == 0:
                # Stundenmarkierungen mit Zahlen
                hour_number = (i // 5 + 11) % 12 + 1
                text_x = center_x + (radius * 0.75) * math.cos(angle)  # Text etwas näher zur Mitte
                text_y = center_y + (radius * 0.75) * math.sin(angle)  # Text etwas näher zur Mitte
                self.create_text(text_x, text_y, text=str(hour_number), font=("Helvetica", 12, "bold"))

            # Minutenmarkierungen
            self.create_line(x1, y1, x2, y2, width=1)

    def update(self, now):
        center_x, center_y = self.size / 2, self.size / 2
        radius = self.size / 3

        self.delete("hour_hand", "minute_hand", "second_hand")

        # Sekundenzeiger
        second_angle = math.radians(6 * now.second - 90)
        second_hand_length = radius * 0.8
        x = center_x + second_hand_length * math.cos(second_angle)
        y = center_y + second_hand_length * math.sin(second_angle)
        self.create_line(center_x, center_y, x, y, width=1, tag="second_hand", fill="red")

        # Minutenzeiger
        minute_angle = math.radians(6 * now.minute - 90)
        minute_hand_length = radius * 0.7
        x = center_x + minute_hand_length * math.cos(minute_angle)
        y = center_y + minute_hand_length * math.sin(minute_angle)
        self.create_line(center_x, center_y, x, y, width=2, tag="minute_hand", fill="black")

        # Stundenzeiger (berücksichtigt auch die Minuten)
        hour_angle = math.radians(30 * (now.hour % 12) + 0.5 * now.minute - 90)  # Stündlicher Anteil + Anteil der Minuten
        hour_hand_length = radius * 0.5
        x = center_x + hour_hand_length * math.cos(hour_angle)
        y = center_y + hour_hand_length * math.sin(hour_angle)
        self.create_line(center_x, center_y, x, y, width=4, tag="hour_hand", fill="black")

        self.after(1000, self.update, datetime.now())  # Alle 1000ms (1 Sekunde) aktualisieren

# Anwendung starten
if __name__ == "__main__":
    app = Demenzuhr()
    app.mainloop()