import customtkinter as ctk
import threading
import time

class SplashScreen:
    def __init__(self, duration=2):
        self.duration = duration
        self.root = ctk.CTk()
        self.root.title("")
        self.root.geometry("400x300")
        self.root.overrideredirect(True)  # Remove barra de título
        self.root.configure(fg_color="#202020")
        
        # Centralizar na tela
        self.center_window()
        
        # Logo/Título
        title = ctk.CTkLabel(
            self.root,
            text="🎬",
            font=("Segoe UI", 80)
        )
        title.pack(pady=(60, 10))
        
        app_name = ctk.CTkLabel(
            self.root,
            text="Valentina's Video Downloader",
            font=("Segoe UI", 20, "bold"),
            text_color="#ffc2dd"
        )
        app_name.pack()
        
        # Loading bar
        self.progress = ctk.CTkProgressBar(
            self.root,
            width=300,
            mode="indeterminate"
        )
        self.progress.pack(pady=40)
        self.progress.start()
        
        status = ctk.CTkLabel(
            self.root,
            text="Carregando...",
            font=("Segoe UI", 11),
            text_color="#ffc2dd"
        )
        status.pack()
        
    def center_window(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        width = 400
        height = 300
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def show(self):
        """Mostra o splash por X segundos"""
        self.root.after(self.duration * 1000, self.root.destroy)
        self.root.mainloop()