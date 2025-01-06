import tkinter as tk
from tkinter import messagebox
import time
from threading import Thread
import pygame  # Para o som de notificação

# Inicialize o pygame para áudio
pygame.mixer.init()

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RPG Timer App")
        self.root.geometry("400x600")  # Tamanho ajustado para uma interface mais espaçosa
        self.root.config(bg="#2c3e50")  # Cor de fundo mais agradável

        # Lista de temporizadores
        self.timers = []

        # Definir volume fixo para 0.10
        self.volume = 0.10

        # Inicializa a interface
        self.init_ui()

    def init_ui(self):
        # Cabeçalho
        self.header = tk.Label(self.root, text="RPG Timer App", font=("Arial", 24), fg="#ecf0f1", bg="#2c3e50")
        self.header.pack(pady=20)

        # Botão "+" para adicionar um novo temporizador
        self.add_button = tk.Button(self.root, text="Adicionar Temporizador", font=("Arial", 14), width=20, height=2, bg="#16a085", fg="#ffffff", relief="flat", command=self.show_add_timer_ui)
        self.add_button.pack(pady=10)

        # Exibe os temporizadores na interface
        self.timer_frame = tk.Frame(self.root, bg="#2c3e50")
        self.timer_frame.pack(pady=10)

    def show_add_timer_ui(self):
        # Limpa a interface e exibe os campos para adicionar um temporizador
        self.add_button.pack_forget()  # Esconde o botão "+"
        
        # Campos para o nome e a duração do temporizador
        self.timer_name_label = tk.Label(self.root, text="Nome do Temporizador:", font=("Arial", 12), fg="#ecf0f1", bg="#2c3e50")
        self.timer_name_label.pack(pady=5)
        self.timer_name_entry = tk.Entry(self.root, font=("Arial", 12))
        self.timer_name_entry.pack(pady=5)

        self.timer_hours_label = tk.Label(self.root, text="Horas:", font=("Arial", 12), fg="#ecf0f1", bg="#2c3e50")
        self.timer_hours_label.pack(pady=5)
        self.timer_hours_entry = tk.Entry(self.root, font=("Arial", 12))
        self.timer_hours_entry.pack(pady=5)

        self.timer_minutes_label = tk.Label(self.root, text="Minutos:", font=("Arial", 12), fg="#ecf0f1", bg="#2c3e50")
        self.timer_minutes_label.pack(pady=5)
        self.timer_minutes_entry = tk.Entry(self.root, font=("Arial", 12))
        self.timer_minutes_entry.pack(pady=5)

        self.timer_seconds_label = tk.Label(self.root, text="Segundos:", font=("Arial", 12), fg="#ecf0f1", bg="#2c3e50")
        self.timer_seconds_label.pack(pady=5)
        self.timer_seconds_entry = tk.Entry(self.root, font=("Arial", 12))
        self.timer_seconds_entry.pack(pady=5)

        # Botão para adicionar o temporizador
        self.add_timer_button = tk.Button(self.root, text="Adicionar", font=("Arial", 14), width=20, height=2, bg="#27ae60", fg="#ffffff", relief="flat", command=self.add_timer)
        self.add_timer_button.pack(pady=15)

    def add_timer(self):
        name = self.timer_name_entry.get()
        hours = self.timer_hours_entry.get()
        minutes = self.timer_minutes_entry.get()
        seconds = self.timer_seconds_entry.get()

        # Se os campos estiverem vazios, considera 0
        hours = int(hours) if hours else 0
        minutes = int(minutes) if minutes else 0
        seconds = int(seconds) if seconds else 0

        total_seconds = hours * 3600 + minutes * 60 + seconds

        if name and total_seconds > 0:
            # Limpa os campos de entrada após adicionar o temporizador
            self.timer_name_label.pack_forget()
            self.timer_name_entry.pack_forget()
            self.timer_hours_label.pack_forget()
            self.timer_hours_entry.pack_forget()
            self.timer_minutes_label.pack_forget()
            self.timer_minutes_entry.pack_forget()
            self.timer_seconds_label.pack_forget()
            self.timer_seconds_entry.pack_forget()
            self.add_timer_button.pack_forget()

            self.start_timer(name, total_seconds)
        else:
            messagebox.showerror("Erro", "Por favor, insira valores válidos para o nome e o tempo.")

    def start_timer(self, name, total_seconds):
        # Exibe o botão "+" novamente
        self.add_button.pack(pady=10)
    
        # Cria o widget do temporizador na interface
        timer_frame = tk.Frame(self.timer_frame, bg="#34495e", padx=20, pady=5)
        timer_frame.pack(pady=5, fill="x")
    
        # Rótulo com o nome do temporizador e a contagem regressiva
        timer_label = tk.Label(timer_frame, text=f"{name}: {self.format_time(total_seconds)}", font=("Arial", 14), fg="#ecf0f1", bg="#34495e", width=30)
        timer_label.pack(side="left", padx=10)
    
        # X para remover
        remove_button = tk.Button(timer_frame, text="X", font=("Arial", 12), width=3, height=1, bg="#e74c3c", fg="#ffffff", relief="flat", command=lambda: self.remove_timer(timer_label, timer_frame))
        remove_button.pack(side="right")
    
        # Adiciona o temporizador à lista com o campo 'is_active'
        self.timers.append({
            "name": name,
            "time_left": total_seconds,
            "label": timer_label,
            "frame": timer_frame,
            "remove_button": remove_button,
            "is_active": True  # Adiciona esse campo para controle de status do temporizador
        })
        # Inicia o temporizador em uma thread separada
        thread = Thread(target=self.run_timer, args=(name, total_seconds, timer_label, timer_frame))
        thread.daemon = True  # A thread será fechada quando o programa for fechado
        thread.start()

    def run_timer(self, name, total_seconds, timer_label, timer_frame):
        while total_seconds > 0:
            time.sleep(1)
            total_seconds -= 1
            # Atualiza a contagem regressiva no rótulo do temporizador
            self.update_timer_label(timer_label, name, total_seconds)
        
        # Atualiza o rótulo com a mensagem de "Tempo Acabou!" ou outra informação
        self.update_timer_label(timer_label, name, "Tempo Acabou!")
    
        # Verifique se o temporizador está ativo antes de tocar o som
        for timer in self.timers:
            if timer["label"] == timer_label and timer["is_active"]:
                self.play_sound()  # Toca o som apenas se o temporizador não foi removido
                self.blink_timer(timer_label)  # Inicia o efeito de piscar


    def update_timer_label(self, timer_label, name, total_seconds):
        # Atualiza o texto do temporizador
        if isinstance(total_seconds, int):
            timer_label.config(text=f"{name}: {self.format_time(total_seconds)}")
        else:
            timer_label.config(text=f"{name}: {total_seconds}")
        self.root.update_idletasks()  # Força a atualização da interface gráfica

    def remove_timer(self, timer_label, timer_frame):
        # Remove o temporizador da interface
        timer_label.pack_forget()  # Remove o rótulo
        timer_frame.pack_forget()  # Remove o frame que contém o rótulo e o botão de remoção
        
        # Encontre o temporizador na lista e defina como inativo
        for timer in self.timers:
            if timer["label"] == timer_label:
                timer["is_active"] = False  # Define o temporizador como inativo
        
        # Remova o temporizador da lista
        self.timers = [timer for timer in self.timers if timer["label"] != timer_label]

    def play_sound(self):
        try:
            sound = pygame.mixer.Sound("notification_sound.wav")  # Certifique-se de ter esse arquivo .wav
            sound.set_volume(self.volume)  # Ajusta o volume
            sound.play()
        except pygame.error as e:
            print(f"Erro ao carregar o som: {e}")

    def blink_timer(self, timer_label):
        # Função para fazer o temporizador piscar
        def toggle_visibility():
            current_color = timer_label.cget("foreground")
            new_color = "red" if current_color == "#ecf0f1" else "#ecf0f1"
            timer_label.config(foreground=new_color)
            self.root.after(500, toggle_visibility)  # Alterna a cada 500ms

        toggle_visibility()

    def format_time(self, seconds):
        """Converte os segundos em formato dinâmico, exibindo apenas horas, minutos e segundos quando necessário"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        # Se não houver horas, exibe apenas minutos e segundos
        if hours > 0:
            return f"{hours:02}:{minutes:02}:{seconds:02}"
        else:
            return f"{minutes:02}:{seconds:02}"

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    print("Aplicativo iniciado...")
    root.mainloop()
