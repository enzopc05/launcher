import subprocess
import psutil
import os
import time
from logger import logger

class GameManager:
    """Classe gérant le lancement et la fermeture des jeux."""
    
    def __init__(self):
        """Initialise le gestionnaire de jeux."""
        self.running_games = {}
    
    def launch_game(self, game):
        """
        Lance un jeu et met à jour son état.
        
        Args:
            game (Game): L'objet Game à lancer.
            
        Returns:
            bool: True si le jeu a été lancé avec succès, False sinon.
        """
        if game.is_running:
            logger.info(f"Le jeu {game.name} est déjà en cours d'exécution.")
            return False
        
        try:
            # Déterminer le répertoire de travail
            working_directory = os.path.dirname(game.path)
            
            # Vérifier si c'est un lien .lnk (raccourci Windows)
            if game.path.lower().endswith('.lnk'):
                # Utiliser la commande start pour ouvrir les raccourcis
                process = subprocess.Popen(f'start "" "{game.path}"', shell=True, cwd=working_directory)
            else:
                # Lancer l'exécutable directement
                process = subprocess.Popen([game.path], cwd=working_directory)
            
            # Attendre un peu pour s'assurer que le processus démarre
            time.sleep(0.5)
            
            game.process = process
            game.is_running = True
            self.running_games[game.name] = game
            logger.info(f"Jeu {game.name} lancé avec succès.")
            return True
        except Exception as e:
            logger.error(f"Erreur lors du lancement du jeu {game.name}: {e}", exc_info=True)
            return False
    
    def close_game(self, game):
        """
        Ferme un jeu en cours d'exécution.
        
        Args:
            game (Game): L'objet Game à fermer.
            
        Returns:
            bool: True si le jeu a été fermé avec succès, False sinon.
        """
        if not game.is_running or game.process is None:
            logger.info(f"Le jeu {game.name} n'est pas en cours d'exécution.")
            return False
        
        try:
            # Tenter de fermer le processus proprement
            try:
                parent = psutil.Process(game.process.pid)
                children = []
                
                # Récupérer tous les processus enfants
                try:
                    children = parent.children(recursive=True)
                except Exception:
                    pass
                
                # Fermer les processus enfants
                for child in children:
                    try:
                        child.terminate()
                    except Exception:
                        pass
                
                # Fermer le processus parent
                parent.terminate()
                
                # Attendre jusqu'à 5 secondes pour la fin des processus
                gone, alive = psutil.wait_procs([parent] + children, timeout=5)
                
                # Si des processus sont encore en vie, les tuer
                for p in alive:
                    try:
                        p.kill()
                    except Exception:
                        pass
            except psutil.NoSuchProcess:
                # Le processus n'existe déjà plus
                pass
            
            game.is_running = False
            game.process = None
            if game.name in self.running_games:
                del self.running_games[game.name]
            
            logger.info(f"Jeu {game.name} fermé avec succès.")
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la fermeture du jeu {game.name}: {e}", exc_info=True)
            return False
    
    def check_running_games(self):
        """Vérifie si les jeux enregistrés sont toujours en cours d'exécution."""
        for game_name in list(self.running_games.keys()):
            game = self.running_games[game_name]
            
            # Vérifier si le processus est toujours en cours d'exécution
            try:
                if game.process is None:
                    # Pas de processus associé
                    game.is_running = False
                    del self.running_games[game_name]
                elif game.process.poll() is not None:
                    # Le processus s'est terminé
                    game.is_running = False
                    game.process = None
                    del self.running_games[game_name]
                # Si on a lancé un raccourci avec "start", le processus peut terminer mais le jeu continue
                elif game.path.lower().endswith('.lnk') and game.process.poll() is not None:
                    # On ne fait rien pour l'instant, on vérifiera lors de la tentative de fermeture
                    pass
            except Exception:
                # En cas d'erreur, considérer que le jeu n'est plus en cours d'exécution
                game.is_running = False
                game.process = None
                if game_name in self.running_games:
                    del self.running_games[game_name]