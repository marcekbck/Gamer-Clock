import tkinter as tk
from tkinter import messagebox
import time
from threading import Thread
import pygame  # Para o som de notificação
from PIL import Image, ImageTk  # Importa a biblioteca PIL para manipular imagens
import pickle

# Inicialize o pygame para áudio
pygame.mixer.init()

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gamer Clock")
        self.root.geometry("800x150")  # Tamanho ajustado para uma interface mais espaçosa
        self.root.config(bg="#2c3e50")  # Cor de fundo mais agradável
        
        root.protocol("WM_DELETE_WINDOW", self.on_close) #Guarda os temporizadores antes de fechar a aplicação
        
        self.selected_image = None
        self.selected_img_path = None
        self.timers = []
        self.volume = 0.10

        self.left_frame = tk.Frame(self.root, bg="#2c3e50", width=240) 
        self.left_frame.pack(side="left", fill="y", expand=False) 
        
        self.right_frame = tk.Frame(self.root, bg="#2c3e50")  
        self.right_frame.pack(side="right", fill="both", expand=True)
        
        self.init_ui()

    def init_ui(self): # MAIN INTERFACE
        self.header = tk.Label(self.left_frame, text="Gamer Clock", font=("Arial", 14), fg="#ecf0f1", bg="#2c3e50")
        self.header.pack(side="left", padx=10)
    
        self.add_button = tk.Button(self.left_frame, text="+", font=("Arial", 14), width=3, height=1, bg="#16a085", fg="#ffffff", relief="flat", command=self.show_add_timer_ui)
        self.add_button.pack(side="left", padx=5, pady=10)
        
        self.entry_frame = tk.Frame(self.right_frame, bg="#2c3e50")
        
        self.timer_frame = tk.Frame(self.right_frame, bg="#2c3e50")
        
        self.load_timers() #
        
    def show_add_timer_ui(self): # Shows the add timer interface
        self.left_frame.pack_forget()
        self.timer_frame.pack_forget()
      
        self.entry_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.timer_name_label = tk.Label(self.entry_frame, text="Name:", font=("Arial", 12), fg="#ecf0f1", bg="#2c3e50")
        self.timer_name_label.pack(side="left")
        self.timer_name_entry = tk.Entry(self.entry_frame, font=("Arial", 12), width=8)
        self.timer_name_entry.pack(side="left", pady=3)
    
        self.timer_hours_label = tk.Label(self.entry_frame, text="Hours:", font=("Arial", 12), fg="#ecf0f1", bg="#2c3e50")
        self.timer_hours_label.pack(side="left", padx=5)
        self.timer_hours_entry = tk.Entry(self.entry_frame, font=("Arial", 12), width=3)
        self.timer_hours_entry.pack(side="left", padx=5)
    
        self.timer_minutes_label = tk.Label(self.entry_frame, text="Min:", font=("Arial", 12), fg="#ecf0f1", bg="#2c3e50")
        self.timer_minutes_label.pack(side="left", padx=5)
        self.timer_minutes_entry = tk.Entry(self.entry_frame, font=("Arial", 12), width=3)
        self.timer_minutes_entry.pack(side="left", padx=5)
    
        self.timer_seconds_label = tk.Label(self.entry_frame, text="Sec:", font=("Arial", 12), fg="#ecf0f1", bg="#2c3e50")
        self.timer_seconds_label.pack(side="left", padx=5)
        self.timer_seconds_entry = tk.Entry(self.entry_frame, font=("Arial", 12), width=3)
        self.timer_seconds_entry.pack(side="left", padx=5)
    
        self.timers_images = [
            "hourglass.png",  
            "boss.jpg",       
            "dungeon.png",    
            "blacksmith.png",
            "chest.png",
            "potion.png",
            "quest.png"
        ]
        self.selected_img_path = None  
        self.img_buttons = [] 
    
        for img_path in self.timers_images:
            img = Image.open(img_path)  
            img = img.resize((50, 50), Image.Resampling.LANCZOS)  
            img_tk = ImageTk.PhotoImage(img) 
            img_button = tk.Button(self.right_frame, image=img_tk, command=lambda image_path=img_path: self.select_hourglass_image(image_path))
            img_button.image = img_tk  
            img_button.pack(side="left", padx=5) 
            self.img_buttons.append(img_button)  

        self.add_timer_button = tk.Button(self.right_frame, text="Add", font=("Arial", 10), width=10, height=2, bg="#27ae60", fg="#ffffff", relief="flat", command=self.add_timer)
        self.add_timer_button.pack(pady=10)
    

    def select_hourglass_image(self, image_path): # Selects the image for the timer
        selected_image = Image.open(image_path)
        selected_image = selected_image.resize((40, 40), Image.Resampling.LANCZOS)
        
        self.selected_image = ImageTk.PhotoImage(selected_image)
        self.selected_img_path = image_path
        
    def add_timer(self): #Creates a new timer
        name = self.timer_name_entry.get()
        hours = self.timer_hours_entry.get()
        minutes = self.timer_minutes_entry.get()
        seconds = self.timer_seconds_entry.get()
    
        name = str(name) if name else " "
        hours = int(hours) if hours else 0
        minutes = int(minutes) if minutes else 0
        seconds = int(seconds) if seconds else 0
    
        total_seconds = hours * 3600 + minutes * 60 + seconds
    
        if name and total_seconds > 0 and self.selected_img_path:  
            self.timer_name_label.pack_forget()
            self.timer_name_entry.pack_forget()
            self.timer_hours_label.pack_forget()
            self.timer_hours_entry.pack_forget()
            self.timer_minutes_label.pack_forget()
            self.timer_minutes_entry.pack_forget()
            self.timer_seconds_label.pack_forget()
            self.timer_seconds_entry.pack_forget()
            self.add_timer_button.pack_forget()
            for btn in self.img_buttons:  
                btn.pack_forget()
        
            self.start_timer(name, total_seconds)
        else:
            messagebox.showerror("Error", "Time and icon is mandatory!")

            
    def start_timer(self, name, total_seconds): 
        self.left_frame.pack(side="left", fill="x", pady=10)
        self.entry_frame.pack_forget()  
        self.timer_frame.pack(fill="both", expand=True, padx=10, pady=5)
        

        temp_frame = tk.Frame(self.timer_frame, bg="#34495e")
        temp_frame.pack(side="left", padx=5)
        

        restart_button = tk.Button(temp_frame, text="↻", font=("Arial", 4), width=1, height=1, bg="#7f8c8d", fg="#ffffff", relief="flat", command=lambda: self.restart_timer(total_seconds, countdown_label))
        restart_button.pack(side="left", anchor="nw")
        

        remove_button = tk.Button(temp_frame, text="X", font=("Arial", 4), width=1, height=1, bg="#e74c3c", fg="#ffffff", relief="flat", command=lambda: self.remove_timer(countdown_label, temp_frame))
        remove_button.pack(side="right", anchor="ne")
        

        image_label = tk.Label(temp_frame, image=self.selected_image, bg="#34495e")
        image_label.pack(side="top", padx=5) 
        

        timer_name = tk.Label(temp_frame, text=f"{name}", font=("Arial", 14), fg="#ecf0f1", bg="#34495e")
        timer_name.pack(side="top", padx=5) 
        

        countdown_label = tk.Label(temp_frame, text=f"{self.format_time(total_seconds)}", font=("Arial", 12), fg="#ecf0f1", bg="#34495e")
        countdown_label.pack(side="top", padx=5) 
    

        self.timers.append({
            "name": name,
            "time_left": total_seconds,                    # Add timer to the timers list
            "label": countdown_label,
            "frame": temp_frame,
            "remove_button": remove_button,
            "image": self.selected_image,
            "image_path": self.selected_img_path,
            "is_active": True,
            "run_id": 0
        })
        current_run_id = 0
        thread = Thread(target=self.run_timer, args=(total_seconds, countdown_label, current_run_id))
        thread.daemon = True  # starts the thread
        thread.start()

    def run_timer(self, total_seconds, label, run_id):
        # Encontra o timer correspondente
        for timer in self.timers:
            if timer["label"] == label:
                # Enquanto o tempo for positivo e o run_id não tiver mudado...
                while total_seconds > 0 and timer["run_id"] == run_id:
                    time.sleep(1)
                    total_seconds -= 1
                    self.update_timer_label(label, total_seconds)
                # Se o timer terminar e o run_id for o mesmo, toca o alarme e inicia o blink
                if total_seconds <= 0 and timer["is_active"]:
                    self.play_sound()
                    self.blink_timer(label)
                return

    def update_timer_label(self, countdown_label, total_seconds):
        countdown_label.config(text=self.format_time(total_seconds))
        self.root.update_idletasks()  # Keeps the UI responsive only on the time "box"

    def remove_timer(self, countdown_label, timer_frame):
        countdown_label.pack_forget() 
        timer_frame.pack_forget() 
        for timer in self.timers:
            if timer["label"] == countdown_label:   # removes the timer from the list and from the interface
                timer["is_active"] = False 
        self.timers = [timer for timer in self.timers if timer["label"] != countdown_label]

    def save_timers(self):
        try:
            with open('timers.pkl', 'wb') as f:
                data_to_save = [
                    {
                        "name": timer["name"],
                        "time_left": timer["time_left"],
                        "image_path": timer["image_path"]
                    }
                    for timer in self.timers
                ]
                pickle.dump(data_to_save, f)  # Saves the timers to the file
            print("Timers salvos com sucesso.")
        except Exception as e:
            print(f"Erro ao salvar os timers: {e}")
    
    def restart_timer(self, total_seconds, label):
        # Encontra o timer e desativa o antigo
        for timer in self.timers:
            if timer["label"] == label:
                timer["is_active"] = False
        
        self.stop_blink(label)
        time.sleep(0.1)
        
        # Reinicia o timer: atualiza o tempo e incrementa o run_id para cancelar a thread antiga
        for timer in self.timers:
            if timer["label"] == label:
                timer["time_left"] = total_seconds
                timer["is_active"] = True
                timer["run_id"] += 1  # Incrementa o identificador
                current_run_id = timer["run_id"]
        
        thread = Thread(target=self.run_timer, args=(total_seconds, label, current_run_id))
        thread.daemon = True
        thread.start()
        
    def load_timers(self):
        try:
            with open('timers.pkl', 'rb') as f:
                saved_timers = pickle.load(f)  # Load the saved timers and recreate them in the interface
            for timer_data in saved_timers:
                self.select_hourglass_image(image_path=timer_data["image_path"])
                self.start_timer(
                    name=timer_data["name"],
                    total_seconds=timer_data["time_left"]
                )
            print("Timers carregados com sucesso.")
        except FileNotFoundError:
            print("Nenhum ficheiro encontrado. Inicializando lista vazia.")
        except Exception as e:
            print(f"Erro ao carregar os timers: {e}")
        
    def play_sound(self):
        try:
            sound = pygame.mixer.Sound("notification_sound.wav")  # Triggers the alarm sound
            sound.set_volume(self.volume)  
            sound.play()
        except pygame.error as e:
            print(f"Erro ao carregar o som: {e}")

    def blink_timer(self, countdown_label):
        def toggle_visibility():
            current_color = countdown_label.cget("foreground")
            new_color = "red" if current_color == "#ecf0f1" else "#ecf0f1"
            countdown_label.config(foreground=new_color)
            after_id = self.root.after(500, toggle_visibility)  
            for timer in self.timers:
                if timer["label"] == countdown_label:
                    timer["after_id"] = after_id  
    
        toggle_visibility()

    
    def stop_blink(self, countdown_label):
        for timer in self.timers:
            if timer["label"] == countdown_label and "after_id" in timer:
                self.root.after_cancel(timer["after_id"])
                countdown_label.config(foreground="#ecf0f1")  # Volta à cor original
                del timer["after_id"]  

        
    def format_time(self, seconds):   # Formats the time
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        if hours > 0:
            return f"{hours:02}:{minutes:02}:{seconds:02}"
        else:
            return f"{minutes:02}:{seconds:02}"
    
    def on_close(self):
        if messagebox.askokcancel("Fechar", "Deseja fechar o programa?"):
            self.save_timers()
            self.root.destroy()
        else:
            return
    
if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
