import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from PIL import Image, ImageTk
import threading
import time

class GameLauncherUI:
    def __init__(self, root, scanner, game_manager):
        self.root = root
        self.scanner = scanner
        self.game_manager = game_manager
        self.games = []
        self.game_frames = {}
        self.current_directory = ""
        
        # Configuration de la fenêtre principale
        self.root.title("Lanceur de Jeux")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Frame principal
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Barre d'outils
        self.toolbar = ttk.Frame(self.main_frame)
        self.toolbar.pack(fill=tk.X, pady=(0, 10))
        
        self.btn_select_dir = ttk.Button(self.toolbar, text="Sélectionner Répertoire", command=self.select_directory)
        self.btn_select_dir.pack(side=tk.LEFT, padx=5)
        
        self.btn_refresh = ttk.Button(self.toolbar, text="Actualiser", command=self.refresh_games)
        self.btn_refresh.pack(side=tk.LEFT, padx=5)
        
        # Affichage du répertoire actuel
        self.dir_var = tk.StringVar(value="Répertoire: Non sélectionné")
        self.dir_label = ttk.Label(self.toolbar, textvariable=self.dir_var, font=("Arial", 9, "italic"))
        self.dir_label.pack(side=tk.LEFT, padx=15)
        
        # Zone de recherche
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda name, index, mode: self.filter_games())
        self.search_entry = ttk.Entry(self.toolbar, textvariable=self.search_var, width=30)
        self.search_entry.pack(side=tk.RIGHT, padx=5)
        ttk.Label(self.toolbar, text="Rechercher:").pack(side=tk.RIGHT)
        
        # Cadre de défilement pour les jeux
        self.canvas = tk.Canvas(self.main_frame)
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Démarrer le thread de vérification des jeux en cours d'exécution
        self.check_thread = threading.Thread(target=self.check_running_games_thread, daemon=True)
        self.check_thread.start()
    
    def select_directory(self):
        """Ouvre une boîte de dialogue pour sélectionner le répertoire des jeux."""
        directory = filedialog.askdirectory(title="Sélectionner le répertoire des jeux")
        if directory:
            self.load_games(directory)
    
    def load_games(self, directory):
        """Charge les jeux depuis le répertoire spécifié."""
        self.current_directory = directory
        self.dir_var.set(f"Répertoire: {directory}")
        self.games = self.scanner.scan_games_directory(directory)
        self.display_games()
    
    def refresh_games(self):
        """Actualise la liste des jeux."""
        if self.current_directory and os.path.isdir(self.current_directory):
            self.load_games(self.current_directory)
        elif self.games:
            # Utiliser le même répertoire que celui actuellement chargé
            directory = os.path.dirname(self.games[0].path)
            while not os.path.isdir(directory):
                directory = os.path.dirname(directory)
            self.load_games(directory)
        else:
            messagebox.showinfo("Information", "Veuillez d'abord sélectionner un répertoire de jeux.")
    
    def display_games(self):
        """Affiche les jeux dans l'interface."""
        # Effacer les anciennes entrées
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.game_frames = {}
        
        if not self.games:
            no_games_label = ttk.Label(self.scrollable_frame, text="Aucun jeu trouvé. Sélectionnez un répertoire contenant des jeux.")
            no_games_label.pack(pady=20)
            return
        
        # Afficher chaque jeu
        for game in self.games:
            self.create_game_frame(game)
    
    def create_game_frame(self, game):
        """Crée un cadre pour afficher un jeu."""
        frame = ttk.Frame(self.scrollable_frame, relief=tk.RAISED, borderwidth=1)
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Image du jeu
        img_frame = ttk.Frame(frame, width=100, height=100)
        img_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        if game.image_path and os.path.exists(game.image_path):
            try:
                img = Image.open(game.image_path)
                img = img.resize((100, 100), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                img_label = ttk.Label(img_frame, image=photo)
                img_label.image = photo  # Garder une référence
            except Exception:
                img_label = ttk.Label(img_frame, text="Image non disponible")
        else:
            img_label = ttk.Label(img_frame, text="Pas d'image")
        
        img_label.pack(fill=tk.BOTH, expand=True)
        
        # Informations sur le jeu
        info_frame = ttk.Frame(frame)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        name_label = ttk.Label(info_frame, text=game.name, font=("Arial", 12, "bold"))
        name_label.pack(anchor="w")
        
        path_label = ttk.Label(info_frame, text=game.path, wraplength=400)
        path_label.pack(anchor="w", pady=(5, 0))
        
        # Boutons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        
        launch_btn = ttk.Button(btn_frame, text="Lancer", command=lambda g=game: self.launch_game(g))
        launch_btn.pack(pady=(0, 5))
        
        close_btn = ttk.Button(btn_frame, text="Fermer", command=lambda g=game: self.close_game(g))
        close_btn.pack()
        close_btn.config(state=tk.DISABLED)  # Désactivé par défaut
        
        # Stocker les références pour mise à jour ultérieure
        self.game_frames[game.name] = {
            'frame': frame,
            'launch_btn': launch_btn,
            'close_btn': close_btn
        }
    
    def launch_game(self, game):
        """Lance un jeu."""
        success = self.game_manager.launch_game(game)
        if success:
            self.update_game_buttons(game)
    
    def close_game(self, game):
        """Ferme un jeu."""
        success = self.game_manager.close_game(game)
        if success:
            self.update_game_buttons(game)
    
    def update_game_buttons(self, game):
        """Met à jour l'état des boutons pour un jeu."""
        if game.name in self.game_frames:
            frame_info = self.game_frames[game.name]
            if game.is_running:
                frame_info['launch_btn'].config(state=tk.DISABLED)
                frame_info['close_btn'].config(state=tk.NORMAL)
            else:
                frame_info['launch_btn'].config(state=tk.NORMAL)
                frame_info['close_btn'].config(state=tk.DISABLED)
    
    def check_running_games_thread(self):
        """Thread pour vérifier périodiquement l'état des jeux en cours d'exécution."""
        while True:
            self.game_manager.check_running_games()
            
            # Mettre à jour l'interface dans le thread principal
            self.root.after(0, self.update_all_game_buttons)
            
            time.sleep(2)  # Vérifier toutes les 2 secondes
    
    def update_all_game_buttons(self):
        """Met à jour tous les boutons de jeu."""
        for game in self.games:
            self.update_game_buttons(game)
    
    def filter_games(self):
        """Filtre les jeux en fonction du texte de recherche."""
        search_text = self.search_var.get().lower()
        
        for game in self.games:
            if game.name in self.game_frames:
                frame = self.game_frames[game.name]['frame']
                if search_text in game.name.lower():
                    frame.pack(fill=tk.X, padx=5, pady=5)
                else:
                    frame.pack_forget()