import tkinter as tk
import os
import sys
import scanner
from interface import GameLauncherUI
from game_manager import GameManager
from logger import logger

def ensure_directory_structure():
    """Crée les dossiers requis s'ils n'existent pas."""
    # Vérifier si le dossier models existe
    if not os.path.exists("models"):
        os.makedirs("models")
        # Créer un fichier __init__.py pour que models soit un package Python
        with open(os.path.join("models", "__init__.py"), "w") as f:
            pass

def main():
    """Fonction principale de l'application."""
    # S'assurer que la structure de dossiers existe
    ensure_directory_structure()
    
    # Créer l'instance de gestion des jeux
    game_manager = GameManager()
    
    # Créer la fenêtre principale
    root = tk.Tk()
    root.title("Lanceur de Jeux")
    
    # Définir une icône si elle existe
    if os.path.exists("assets/icon.ico"):
        root.iconbitmap("assets/icon.ico")
    
    # Initialiser l'interface utilisateur
    app = GameLauncherUI(root, scanner.scan_games_directory, game_manager)
    
    # Définir le répertoire de jeux par défaut
    jeux_path = r"C:\Users\User\OneDrive\Bureau\jeu"
    
    # Vérifier si le répertoire existe
    if os.path.exists(jeux_path) and os.path.isdir(jeux_path):
        logger.info(f"Chargement des jeux depuis {jeux_path}")
        # Charger automatiquement les jeux de ce répertoire au démarrage
        app.load_games(jeux_path)
    else:
        logger.warning(f"Le répertoire {jeux_path} n'existe pas. Veuillez sélectionner un répertoire manuellement.")
    
    # Démarrer la boucle d'événements
    root.mainloop()

if __name__ == "__main__":
    main()