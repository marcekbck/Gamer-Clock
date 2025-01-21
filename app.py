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
        # Lista de temporizadores
        self.timers = []
        # Definir volume fixo para 0.10
        self.volume = 0.10

        # Criação de dois frames: um para o botão de adicionar e titulo
        self.left_frame = tk.Frame(self.root, bg="#2c3e50", width=240)  # Frame fixo no topo
        self.left_frame.pack(side="left", fill="y", expand=False)  #lado esquerdo 
        
        # Frame principal onde os temporizadores serão listados
        self.right_frame = tk.Frame(self.root, bg="#2c3e50")  # Fundo diferente para destaque
        self.right_frame.pack(side="right", fill="both", expand=True)
        
        
        # Inicializa a interface
        self.init_ui()

    def init_ui(self):
        # Cabeçalho no frame esquerdo
        self.header = tk.Label(self.left_frame, text="Gamer Clock", font=("Arial", 14), fg="#ecf0f1", bg="#2c3e50")
        self.header.pack(side="left", padx=10)
    
        # Botão "+" no frame esquerdo
        self.add_button = tk.Button(self.left_frame, text="+", font=("Arial", 14), width=3, height=1, bg="#16a085", fg="#ffffff", relief="flat", command=self.show_add_timer_ui)
        self.add_button.pack(side="left", padx=5, pady=10)
        
        # Frame para os campos de entrada
        self.entry_frame = tk.Frame(self.right_frame, bg="#2c3e50")
        
        #Frame para listar os timers
        self.timer_frame = tk.Frame(self.right_frame, bg="#2c3e50")
        
        self.load_timers() # Carrega os temporizadores salvos
        
    def show_add_timer_ui(self):
        # Limpa a interface e exibe os campos para adicionar um temporizador
        self.left_frame.pack_forget()
        self.timer_frame.pack_forget()
      
        #Mostra o frame de entrada de dados
        self.entry_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Campos para o nome do temporizador
        self.timer_name_label = tk.Label(self.entry_frame, text="Name:", font=("Arial", 12), fg="#ecf0f1", bg="#2c3e50")
        self.timer_name_label.pack(side="left")
        self.timer_name_entry = tk.Entry(self.entry_frame, font=("Arial", 12), width=8)
        self.timer_name_entry.pack(side="left", pady=3)
    
        # Campos para Horas, Minutos e Segundos
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
    
        # Criando botões para escolher os icons
        self.hourglass_images = [
            "hourglass.png",  # Caminho para a imagem 1
            "boss.jpg",       # Caminho para a imagem 2
            "dungeon.png",    # Caminho para a imagem 3
            "blacksmith.png",
            "chest.png",
            "potion.png",
            "quest.png"
        ]
        self.selected_img_path = None  # Variável para armazenar a imagem escolhida
        self.img_buttons = []  # Lista para armazenar os botões de imagem
    
        for img_path in self.hourglass_images:
            img = Image.open(img_path)  # Abre a imagem
            img = img.resize((50, 50), Image.Resampling.LANCZOS)  # Redimensiona a imagem
            img_tk = ImageTk.PhotoImage(img)  # Converte a imagem para o formato compatível com Tkinter
            # Cria o botão para cada imagem dentro do frame
            img_button = tk.Button(self.right_frame, image=img_tk, command=lambda image_path=img_path: self.select_hourglass_image(image_path))
            img_button.image = img_tk  # Armazena a referência para a imagem
            img_button.pack(side="left", padx=5)  # Adiciona ao frame, lado a lado
            self.img_buttons.append(img_button)  # Adiciona o botão à lista

            
        # Botão para adicionar o temporizador
        self.add_timer_button = tk.Button(self.right_frame, text="Add", font=("Arial", 10), width=10, height=2, bg="#27ae60", fg="#ffffff", relief="flat", command=self.add_timer)
        self.add_timer_button.pack(pady=10)
    

    def select_hourglass_image(self, image_path):
        # Carrega a imagem a partir do caminho fornecido
        selected_image = Image.open(image_path)
        selected_image = selected_image.resize((40, 40), Image.Resampling.LANCZOS)
        
        # Converte a imagem para PhotoImage e armazena como selecionada
        self.selected_image = ImageTk.PhotoImage(selected_image)
        self.selected_img_path = image_path
        
    def add_timer(self): #Cria um temporizador
        name = self.timer_name_entry.get()
        hours = self.timer_hours_entry.get()
        minutes = self.timer_minutes_entry.get()
        seconds = self.timer_seconds_entry.get()
    
        # Se os campos estiverem vazios, considera 0
        name = str(name) if name else " "
        hours = int(hours) if hours else 0
        minutes = int(minutes) if minutes else 0
        seconds = int(seconds) if seconds else 0
    
        total_seconds = hours * 3600 + minutes * 60 + seconds
    
        if name and total_seconds > 0 and self.selected_img_path:  # Verifica se há uma imagem selecionada
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
            for btn in self.img_buttons:  # Esconde todos os botões de imagem
                btn.pack_forget()
        
            # Chama o método para iniciar o temporizador e passa a imagem selecionada
            self.start_timer(name, total_seconds)
        else:
            messagebox.showerror("Erro", "Time and icon is mandatory!")

            
    def start_timer(self, name, total_seconds): #Mostra e inicializa o temporizador
        # Exibe o botão "+" novamente
        self.left_frame.pack(side="left", fill="x", pady=10) #Mostra o frame da app e o botão de adicionar
        self.entry_frame.pack_forget()  # Esconde o frame de entrada de dados
        self.timer_frame.pack(fill="both", expand=True, padx=10, pady=5) #Mostra o frame de timers
        
        # Coloca o frame para um temporizador único
        temp_frame = tk.Frame(self.timer_frame, bg="#34495e")
        temp_frame.pack(side="left", padx=5)
        
        # Botão para reiniciar o temporizador
        restart_button = tk.Button(temp_frame, text="↻", font=("Arial", 4), width=1, height=1, bg="#7f8c8d", fg="#ffffff", relief="flat", command=lambda: (name, total_seconds))
        restart_button.pack(side="left", anchor="nw")
        
        # X para remover
        remove_button = tk.Button(temp_frame, text="X", font=("Arial", 4), width=1, height=1, bg="#e74c3c", fg="#ffffff", relief="flat", command=lambda: self.remove_timer(countdown_label, temp_frame))
        remove_button.pack(side="right", anchor="ne")
        
        # Coloca a imagem no topo do temporizador
        image_label = tk.Label(temp_frame, image=self.selected_image, bg="#34495e")
        image_label.pack(side="top", padx=5)  # Empacota a imagem no topo
        
        # Rótulo com o nome do temporizador abaixo da imagem
        timer_name = tk.Label(temp_frame, text=f"{name}", font=("Arial", 14), fg="#ecf0f1", bg="#34495e")
        timer_name.pack(side="top", padx=5)  # Empacota o nome abaixo da imagem
        
        # Rótulo com a contagem regressiva abaixo do tempo pedido
        countdown_label = tk.Label(temp_frame, text=f"{self.format_time(total_seconds)}", font=("Arial", 12), fg="#ecf0f1", bg="#34495e")
        countdown_label.pack(side="top", padx=5)  # Empacota a contagem regressiva abaixo do tempo pedido
    
        # Adiciona o temporizador à lista com o campo 'is_active'
        self.timers.append({
            "name": name,
            "time_left": total_seconds,
            "label": countdown_label,
            "frame": temp_frame,
            "remove_button": remove_button,
            "image": self.selected_image,
            "image_path": self.selected_img_path,
            "is_active": True  # Adiciona esse campo para controle de status do temporizador
        })
        
        # Inicia o temporizador em uma thread separada
        thread = Thread(target=self.run_timer, args=(total_seconds, countdown_label))
        thread.daemon = True  # A thread será fechada quando o programa for fechado
        thread.start()

    def run_timer(self, total_seconds, timer_label):
        while total_seconds > 0:
            time.sleep(1)
            total_seconds -= 1
            # Atualiza a contagem regressiva no rótulo do temporizador
            self.update_timer_label(timer_label, total_seconds)
        
        # Verifique se o temporizador está ativo antes de tocar o som
        for timer in self.timers:
            if timer["label"] == timer_label and timer["is_active"]:
                self.play_sound()  # Toca o som apenas se o temporizador não foi removido
                self.blink_timer(timer_label)  # Inicia o efeito de piscar

    def update_timer_label(self, countdown_label, total_seconds):
        # Atualiza o texto do temporizador apenas no countdown_label
        countdown_label.config(text=self.format_time(total_seconds))
        self.root.update_idletasks()  # Força a atualização da interface gráfica

    def remove_timer(self, countdown_label, timer_frame):
        # Remove o temporizador da interface
        countdown_label.pack_forget()  # Remove o rótulo
        timer_frame.pack_forget()  # Remove o frame que contém o rótulo e o botão de remoção
        
        # Encontre o temporizador na lista e defina como inativo
        for timer in self.timers:
            if timer["label"] == countdown_label:
                timer["is_active"] = False  # Define o temporizador como inativo
        
        # Remova o temporizador da lista
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
                pickle.dump(data_to_save, f)  # Salva apenas os dados essenciais
            print("Timers salvos com sucesso.")
        except Exception as e:
            print(f"Erro ao salvar os timers: {e}")
    
    def load_timers(self):
        try:
            with open('timers.pkl', 'rb') as f:
                saved_timers = pickle.load(f)  # Carrega os dados do ficheiro

            for timer_data in saved_timers:
                # Recriar o timer e os seus widgets a partir dos dados salvos
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
