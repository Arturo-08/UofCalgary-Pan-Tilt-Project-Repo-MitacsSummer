import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import datetime as dt
from PIL import Image, ImageTk

class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        # Make the app responsive
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

        # Create control variables
        self.yaw_value = tk.DoubleVar(value=0.0)
        self.pitch_value = tk.DoubleVar(value=0.0)
        self.speed_value = tk.DoubleVar(value=0.0)
        self.file_path = tk.StringVar()
        self.cycle_time_value = tk.DoubleVar(value=1.0)
        self.min_pitch_value = tk.DoubleVar(value=-60.0)
        self.max_pitch_value = tk.DoubleVar(value=60.0)

        # Create widgets
        self.setup_widgets()

    def update_label(self, slider_var, entry, label):
        value = slider_var.get()
        entry.delete(0, tk.END)
        entry.insert(0, f"{value:.2f}")
        self.check_value()

    def check_value(self):
        yaw = self.yaw_value.get()
        pitch = self.pitch_value.get()
        speed = self.speed_value.get()

        self.yaw_alert_label.config(text="")
        self.pitch_alert_label.config(text="")
        self.speed_alert_label.config(text="")

        if not (-60 <= yaw <= 44):
            self.yaw_alert_label.config(text="Value not allowed", foreground="red")
        if not (-60 <= pitch <= 60):
            self.pitch_alert_label.config(text="Value not allowed", foreground="red")
        if not (1 <= speed <= 30):
            self.speed_alert_label.config(text="Value not allowed", foreground="red")

        if (-60 <= yaw <= 44) and (-60 <= pitch <= 60) and (1 <= speed <= 30):
            self.open_terminal_button.config(state="normal")
        else:
            self.open_terminal_button.config(state="disabled")

    def validate_entry(self, var, entry, label):
        try:
            value = float(var.get())
            if entry == self.yaw_entry:
                if -60 <= value <= 44:
                    self.yaw_value.set(value)
                else:
                    self.yaw_alert_label.config(text="Value not allowed", foreground="red")
            elif entry == self.pitch_entry:
                if -60 <= value <= 60:
                    self.pitch_value.set(value)
                else:
                    self.pitch_alert_label.config(text="Value not allowed", foreground="red")
            elif entry == self.speed_entry:
                if 1 <= value <= 30:
                    self.speed_value.set(value)
                else:
                    self.speed_alert_label.config(text="Value not allowed", foreground="red")
            self.check_value()
        except ValueError:
            label.config(text="Value not allowed", foreground="red")

    def open_terminal(self):
        yaw = self.yaw_value.get()
        pitch = self.pitch_value.get()
        speed = self.speed_value.get()
        print(dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        command = f"""
        #!/bin/bash
        cd ~/ros_python/Pan-Tilt-UofC-Python-Project
        source abl_py_env/bin/activate
        iqr_pan_tilt_tool {yaw} {pitch} {speed}
        """

        script_path = os.path.expanduser("~/temp_script.sh")
        with open(script_path, "w") as f:
            f.write(command)

        subprocess.run(["chmod", "+x", script_path])

        terminal_command = f"gnome-terminal -- bash -c '{script_path}; exec bash'"
        subprocess.Popen(terminal_command, shell=True)

    def run_python_script(self):
        try:
            if self.file_path.get():
                subprocess.run(["python3", self.file_path.get()], check=True)
            else:
                messagebox.showerror("Error", "No file selected")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("Script Files", "*.sh")])
        if file_path:
            self.file_path.set(file_path)
            self.file_label.config(text=os.path.basename(file_path))
            self.run_button.config(state="normal")

    def generate_endless_loop(self):
        try:
            cycle_time = self.cycle_time_value.get()
            min_pitch = self.min_pitch_value.get()
            max_pitch = self.max_pitch_value.get()

            command = f"python3 generate_endless_loop.py {cycle_time} {min_pitch} {max_pitch}"
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def resize_image(self, event):
        """ Redimensionar la imagen cuando cambia el tamaño del frame """
        new_width = event.width
        new_height = event.height

        #Resize the image
        resized_img = Image.open("IQR_robot.png").resize((new_width, new_height), Image.ANTIALIAS)

        # Actualizar la imagen en img_iqr
        self.img_iqr = ImageTk.PhotoImage(resized_img)
        self.img_iqr_view.configure(image=self.img_iqr)

    def setup_widgets(self):
        # Frame for Move IQR to
        self.move_iqr_frame = ttk.LabelFrame(self, text="Move IQR to:", padding=(20, 10))
        self.move_iqr_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        # Create Yaw slider, entry and label
        self.yaw_label_text = ttk.Label(self.move_iqr_frame, text="Yaw: ")
        self.yaw_label_text.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.yaw_entry = ttk.Entry(self.move_iqr_frame, textvariable=self.yaw_value)
        self.yaw_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.yaw_entry.bind("<FocusOut>", lambda e: self.validate_entry(self.yaw_value, self.yaw_entry, self.yaw_alert_label))
        self.yaw_slider = ttk.Scale(self.move_iqr_frame, from_=-60, to=44, orient='horizontal',
                                    variable=self.yaw_value, command=lambda event: self.update_label(self.yaw_value, self.yaw_entry, self.yaw_alert_label))
        self.yaw_slider.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        self.yaw_alert_label = ttk.Label(self.move_iqr_frame, text="")
        self.yaw_alert_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # Create Pitch slider, entry and label
        self.pitch_label_text = ttk.Label(self.move_iqr_frame, text="Pitch: ")
        self.pitch_label_text.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")
        self.pitch_entry = ttk.Entry(self.move_iqr_frame, textvariable=self.pitch_value)
        self.pitch_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.pitch_entry.bind("<FocusOut>", lambda e: self.validate_entry(self.pitch_value, self.pitch_entry, self.pitch_alert_label))
        self.pitch_slider = ttk.Scale(self.move_iqr_frame, from_=-60, to=60, orient='horizontal',
                                      variable=self.pitch_value, command=lambda event: self.update_label(self.pitch_value, self.pitch_entry, self.pitch_alert_label))
        self.pitch_slider.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        self.pitch_alert_label = ttk.Label(self.move_iqr_frame, text="")
        self.pitch_alert_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # Create Speed slider, entry and label
        self.speed_label_text = ttk.Label(self.move_iqr_frame, text="Speed: ")
        self.speed_label_text.grid(row=6, column=0, padx=5, pady=5, sticky="nsew")
        self.speed_entry = ttk.Entry(self.move_iqr_frame, textvariable=self.speed_value)
        self.speed_entry.grid(row=6, column=1, padx=5, pady=5, sticky="ew")
        self.speed_entry.bind("<FocusOut>", lambda e: self.validate_entry(self.speed_value, self.speed_entry, self.speed_alert_label))
        self.speed_slider = ttk.Scale(self.move_iqr_frame, from_=1, to=30, orient='horizontal',
                                      variable=self.speed_value, command=lambda event: self.update_label(self.speed_value, self.speed_entry, self.speed_alert_label))
        self.speed_slider.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        self.speed_alert_label = ttk.Label(self.move_iqr_frame, text="")
        self.speed_alert_label.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # Button for open terminal
        self.open_terminal_button = ttk.Button(self.move_iqr_frame, text="Move to", command=self.open_terminal)
        self.open_terminal_button.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        self.check_value()

        # Frame for Run Python Script
        self.script_frame = ttk.LabelFrame(self, text="Run Python Script", padding=(20, 10))
        self.script_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        self.file_label = ttk.Label(self.script_frame, text="No file selected", anchor="w")
        self.file_label.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.select_button = ttk.Button(self.script_frame, text="Select File", command=self.select_file)
        self.select_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.run_button = ttk.Button(self.script_frame, text="Run", command=self.run_python_script, state="disabled")
        self.run_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

         # Frame for Generate Endless Loop
        self.loop_frame = ttk.LabelFrame(self, text="Generate Endless Loop", padding=(20, 10))
        self.loop_frame.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")

        # Sub-Frame for Generate Endless Loop
        self.loop_sub_frame = ttk.Frame(self.loop_frame, padding=(20, 10))
        self.loop_sub_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
        self.loop_sub_frame.columnconfigure(0, weight=1)
        self.loop_sub_frame.columnconfigure(1, weight=1)
        self.loop_sub_frame.rowconfigure(0, weight=1)
        self.loop_sub_frame.rowconfigure(1, weight=1)

        # Left Sub-Frame (2 rows, 1 column)
        self.left_sub_frame = ttk.Frame(self.loop_sub_frame)
        self.left_sub_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="nsew")
        self.left_sub_frame.columnconfigure(0, weight=1)
        self.left_sub_frame.rowconfigure(0, weight=1)
        self.left_sub_frame.rowconfigure(1, weight=1)

        # Right Sub-Frame (1 row, 1 column) for Image
        self.right_sub_frame = ttk.Frame(self.loop_sub_frame)
        self.right_sub_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.right_sub_frame.columnconfigure(0, weight=1)
        self.right_sub_frame.rowconfigure(0, weight=1)

        # Load image for the right frame
        img_path = os.path.join(os.path.dirname(__file__), "IQR_robot.png")
        img = Image.open(img_path)
        img = img.resize((int(img.width/1.8), int(img.height/1.8)))

        self.img_iqr = ImageTk.PhotoImage(img)
        self.img_iqr_view = ttk.Label(self.right_sub_frame, image=self.img_iqr)
        self.img_iqr_view.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Setting up size photo
        self.right_sub_frame.bind("<Configure>", self.resize_image)

        self.cycle_time_label = ttk.Label(self.left_sub_frame, text="Cycle Time (minutes): ")
        self.cycle_time_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.cycle_time_entry = ttk.Entry(self.left_sub_frame, textvariable=self.cycle_time_value)
        self.cycle_time_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.min_pitch_label = ttk.Label(self.left_sub_frame, text="Pitch Min: ")
        self.min_pitch_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.min_pitch_entry = ttk.Entry(self.left_sub_frame, textvariable=self.min_pitch_value)
        self.min_pitch_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.max_pitch_label = ttk.Label(self.left_sub_frame, text="Pitch Max: ")
        self.max_pitch_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.max_pitch_entry = ttk.Entry(self.left_sub_frame, textvariable=self.max_pitch_value)
        self.max_pitch_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        self.generate_button = ttk.Button(self.loop_frame, text="Generate endless loop", command=self.generate_endless_loop)
        self.generate_button.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        # Frame for Last Values
        self.last_values_frame = ttk.LabelFrame(self, text="Last Values", padding=(20, 10))
        self.last_values_frame.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")

        # Last values Table
        self.last_values_tree = ttk.Treeview(self.last_values_frame, columns=("Yaw", "Pitch", "Speed", "Instruction"), show="headings")
        self.last_values_tree.heading("Yaw", text="Yaw")
        self.last_values_tree.heading("Pitch", text="Pitch")
        self.last_values_tree.heading("Speed", text="Speed")
        self.last_values_tree.heading("Instruction", text="Instruction")
        self.last_values_tree.pack(expand=True, fill="both")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Pan-Tilt Control Application")
    app = App(root)
    app.pack(expand=True, fill="both")
    root.mainloop()
