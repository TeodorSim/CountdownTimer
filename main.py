import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import threading
import winsound

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Temporizator")
        self.root.geometry("300x300")
        self.root.minsize(200, 200)

        self.hours_var = tk.StringVar()
        self.minutes_var = tk.StringVar()
        self.seconds_var = tk.StringVar()

        self.latest_timer = None
        self.notification_displayed = False

        self.create_widgets()

    def create_widgets(self):
        # input
        ttk.Label(self.root, text="Ore:").grid(row=0, column=0, padx=5, pady=5,  sticky=tk.W)
        ttk.Entry(self.root, textvariable=self.hours_var, width=5).grid(row=0, column=1, padx=5, pady=5,  sticky=tk.W)
        ttk.Label(self.root, text="Minute:").grid(row=1, column=0, padx=5, pady=5,  sticky=tk.W)
        ttk.Entry(self.root, textvariable=self.minutes_var, width=5).grid(row=1, column=1, padx=5, pady=5,  sticky=tk.W)
        ttk.Label(self.root, text="Secunde:").grid(row=2, column=0, padx=5, pady=5,  sticky=tk.W)
        ttk.Entry(self.root, textvariable=self.seconds_var, width=5).grid(row=2, column=1, padx=5, pady=5,  sticky=tk.W)

        # predefined timers
        ttk.Button(self.root, text="5 secunde", command=lambda: self.set_predefined_timer(0, 0, 5)).grid(row=4, column=0, pady=5,  sticky=tk.W)
        ttk.Button(self.root, text="30 secunde", command=lambda: self.set_predefined_timer(0, 0, 30)).grid(row=4, column=1, pady=5,  sticky=tk.W)
        ttk.Button(self.root, text="1 minut", command=lambda: self.set_predefined_timer(0, 1, 0)).grid(row=5, column=0, pady=5,  sticky=tk.W)
        ttk.Button(self.root, text="2 minute", command=lambda: self.set_predefined_timer(0, 2, 0)).grid(row=5, column=1, pady=5,  sticky=tk.W)

        ttk.Button(self.root, text="Seteaza Alarma", command=self.start_timer).grid(row=6, column=0, columnspan=2, pady=10,  sticky=tk.W)

        ttk.Sizegrip(self.root).grid(row=999, column=999, sticky=(tk.S, tk.E))
        self.root.resizable(True, True)


        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(999, weight=1)

        self.remaining_time_label = ttk.Label(self.root, text="")
        self.remaining_time_label.grid(row=7, column=0, columnspan=2, pady=5, sticky=tk.W)

    def start_timer(self):
        try:
            if self.hours_var.get() == "":
                self.hours_var.set("0")
            hours = int(self.hours_var.get())
        except ValueError:
            messagebox.showerror("Eroare", "Introdu o valoarea valida pentru ore!")
            return
        try:
            if self.minutes_var.get() == "":
                self.minutes_var.set("0")
            minutes = int(self.minutes_var.get())
        except ValueError:
            messagebox.showerror("Eroare", "Introdu o valoarea valida pentru minute!")
            return
        try:
            if self.seconds_var.get() == "":
                self.seconds_var.set("1")
            seconds = int(self.seconds_var.get())
        except ValueError:
            messagebox.showerror("Eroare", "Introdu o valoarea valida pentru secunde!")
            return

        hours, minutes, seconds = self.restriction_check(hours, minutes, seconds)
        if hours == -1:
            messagebox.showerror("Eroare", "Orele nu pot fi mai mult de 23!")
        self.set_predefined_timer(hours, minutes, seconds)

    def set_predefined_timer(self, hours, minutes, seconds):
        current_time = datetime.datetime.now().time()
        self.time_when_up = datetime.datetime.combine(datetime.date.today(), current_time) + datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)

        if self.latest_timer is None and self.notification_displayed is True:
            self.notification_displayed = False
        self.latest_timer = self.time_when_up
        self.one_banner = True

        self.run_countdown()

    def restriction_check(self, hours, minutes, seconds):
        if seconds > 59:
            minutes += int(seconds / 60)
            seconds %= 60
        if minutes > 59:
            hours += int(minutes / 60)
            minutes %= 60
        if hours > 23:
            return -1, -1, -1
        return hours, minutes, seconds

    def countdown(self):
        while datetime.datetime.now() < self.time_when_up:
            remaining_time = self.time_when_up - datetime.datetime.now()
            remaining_str = str(remaining_time).split(".")[0]
            self.remaining_time_label.config(text=f"Time remaining: {remaining_str}")
            self.root.update()
        self.show_notification()
        self.latest_timer = None

    def run_countdown(self):
        timer_thread = threading.Thread(target=self.countdown)
        timer_thread.start()

    def show_notification(self):
        if self.notification_displayed is False:
            self.notification_displayed = True
            winsound.Beep(800, 500)
            messagebox.showinfo("Alaaaaaarma", "Bomb has been defused!")
            ##self.root.after(10, self.root.destroy)  # close app in 10ms

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
