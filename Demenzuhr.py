import tkinter as tk
from datetime import datetime
import math

class Demenzuhr(tk.Tk):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Demenzuhr")
        self.geometry("800x480")  # Größe anpassen je nach Display-Auflösung

        self.analog_uhr = AnalogUhr(self)
        self.analog_uhr.pack(pady=20)

        self.digital_uhr = tk.Label(self, text="", font=("Helvetica", 48))
        self.digital_uhr.pack()

        self.tag_zeit = tk.Label(self, text="", font=("Helvetica", 24))
        self.tag_zeit.pack()

        self.update_time()

    def update_time(self):
        now = datetime.now()

        # Analoge Uhr aktualisieren
        self.analog_uhr.update(now)

        # Digitale Uhr aktualisieren
        digital_time = now.strftime("%H:%M:%S")
        self.digital_uhr.config(text=digital_time)

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

        for i in range(12):
            angle = math.radians(360 * i / 12 - 90)  # Umrechnung in Bogenmaß, Start bei 12 Uhr (-90 Grad)
            length_ratio = 0.85  # Länge der Stundenmarkierungen
            x = center_x + radius * length_ratio * math.cos(angle)
            y = center_y + radius * length_ratio * math.sin(angle)

            # Zahl an der Stelle der Stundenmarkierung
            self.create_text(x, y, text=str((i + 11) % 12 + 1), font=("Helvetica", 12, "bold"))

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
