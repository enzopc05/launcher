import logging
import os
import sys
import traceback
from datetime import datetime

class Logger:
    """Classe pour gérer la journalisation des événements et erreurs."""
    
    def __init__(self, log_dir="logs"):
        """
        Initialise le système de journalisation.
        
        Args:
            log_dir (str): Le répertoire où stocker les fichiers de log.
        """
        # Créer le répertoire de logs s'il n'existe pas
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Configurer le nom du fichier de log avec la date et l'heure
        log_file = os.path.join(log_dir, f"launcher_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        
        # Configurer le logger
        self.logger = logging.getLogger("launcher")
        self.logger.setLevel(logging.DEBUG)
        
        # Handler pour le fichier
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # Handler pour la console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Formateur
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Ajouter les handlers au logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        self.logger.info("Logger initialisé")
    
    def info(self, message):
        """Enregistre un message d'information."""
        self.logger.info(message)
    
    def debug(self, message):
        """Enregistre un message de débogage."""
        self.logger.debug(message)
    
    def warning(self, message):
        """Enregistre un avertissement."""
        self.logger.warning(message)
    
    def error(self, message, exc_info=False):
        """Enregistre une erreur."""
        self.logger.error(message, exc_info=exc_info)
    
    def exception(self, message):
        """Enregistre une exception avec sa trace complète."""
        self.logger.exception(message)

# Créer une instance globale du logger
logger = Logger()

def log_exception_hook(exc_type, exc_value, exc_traceback):
    """
    Hook pour capturer les exceptions non gérées.
    Cette fonction remplace sys.excepthook.
    """
    if issubclass(exc_type, KeyboardInterrupt):
        # Ne pas capturer les interruptions clavier (Ctrl+C)
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    logger.error(
        "Exception non gérée: %s",
        ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    )

# Remplacer le gestionnaire d'exceptions par défaut
sys.excepthook = log_exception_hook