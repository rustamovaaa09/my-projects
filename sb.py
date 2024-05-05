import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import psutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from scapy.all import sniff
import scapy.error
import threading
import platform

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

        self.process_button = ttk.Button(root, text="Мониторить Процессы", command=self.monitor_processes)
        self.process_button.pack()

        self.file_button = ttk.Button(root, text="Мониторить Изменения Файлов", command=self.select_file)
        self.file_button.pack()

        self.network_button = ttk.Button(root, text="Мониторить Сетевую Активность", command=self.monitor_network)
        self.network_button.pack()

        self.result_label = ttk.Label(root, text="", style="Result.TLabel")
        self.result_label.pack()

        self.result_list = tk.Listbox(root, height=10, width=60)
        self.result_list.pack()

        self.selected_file = ""

    def monitor_processes(self):
        messagebox.showinfo("Мониторинг Процессов", "Мониторинг процессов...")
        threading.Thread(target=self._monitor_processes).start()

    def _monitor_processes(self):
        self.result_list.delete(0, tk.END)
        for proc in psutil.process_iter():
            try:
                proc_name = 'Процесс {} запущен'.format(proc.name())
                print(proc_name)
                self.result_list.insert(tk.END, proc_name)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    def select_file(self):
        self.selected_file = filedialog.askopenfilename()
        if self.selected_file:
            self.monitor_files()

    def monitor_files(self):
        messagebox.showinfo("Мониторинг Изменений Файлов", "Мониторинг изменений файла {}...".format(self.selected_file))
        threading.Thread(target=self._monitor_files).start()

    def _monitor_files(self):
        self.result_list.delete(0, tk.END)
        class FileChangeHandler(FileSystemEventHandler):
            def on_modified(self, event):
                if not event.is_directory:
                    file_changed = 'Файл {} изменен'.format(event.src_path)
                    print(file_changed)
                    self.result_list.insert(tk.END, file_changed)
        observer = Observer()
        observer.schedule(FileChangeHandler(), self.selected_file, recursive=True)
        observer.start()

    def monitor_network(self):
        messagebox.showinfo("Мониторинг Сетевой Активности", "Мониторинг сетевой активности...")
        threading.Thread(target=self._monitor_network).start()

    def _monitor_network(self):
        self.result_list.delete(0, tk.END)
        try:
            sniff(prn=self.packet_callback, count=1)
        except scapy.error.Scapy_Exception as e:
            print("Ошибка при анализе сетевых пакетов:", e)

    def packet_callback(self, packet):
        network_activity = 'Обнаружена сетевая активность'
        print(network_activity)
        self.result_list.insert(tk.END, network_activity)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
