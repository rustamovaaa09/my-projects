import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import psutil
import threading

class App:
    def __init__(self, root):
        self.root = root
        root.title("Монитор Событий")
        self.label = ttk.Label(root, text="Монитор Событий", style="Title.TLabel")
        self.label.pack()

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12), padding=10)
        self.style.configure("TLabel", font=("Arial", 12))
        self.style.configure("Title.TLabel", font=("Arial", 16, "bold"))

        self.process_button = ttk.Button(root, text="Мониторить Процессы", command=self.start_monitor_processes)
        self.process_button.pack()

        self.stop_button = ttk.Button(root, text="Остановить Мониторинг", command=self.stop_monitor_processes)
        self.stop_button.pack()

        self.result_label = ttk.Label(root, text="", style="Result.TLabel")
        self.result_label.pack()

        self.result_list = tk.Listbox(root, height=10, width=60)
        self.result_list.pack()

        self.monitoring = False

    def start_monitor_processes(self):
        self.monitoring = True
        threading.Thread(target=self.monitor_processes).start()

    def monitor_processes(self):
        while self.monitoring:
            self.result_list.delete(0, tk.END)
            for proc in psutil.process_iter():
                try:
                    proc_name = 'Процесс {} запущен'.format(proc.name())
                    print(proc_name)
                    self.result_list.insert(tk.END, proc_name)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            if self.monitoring:
                self.root.after(1000)
            else:
                break

    def stop_monitor_processes(self):
        self.monitoring = False

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
