class Game:
    """Classe représentant un jeu."""
    
    def __init__(self, name, path, image_path=None):
        """
        Initialise un nouvel objet Game.
        
        Args:
            name (str): Le nom du jeu.
            path (str): Le chemin vers l'exécutable du jeu.
            image_path (str, optional): Le chemin vers l'image du jeu. Par défaut None.
        """
        self.name = name
        self.path = path
        self.image_path = image_path
        self.process = None
        self.is_running = False
    
    def __str__(self):
        """Représentation textuelle de l'objet Game."""
        return f"Jeu: {self.name} ({self.path})"
    
    def __repr__(self):
        """Représentation de l'objet pour le débogage."""
        return f"Game(name='{self.name}', path='{self.path}', image_path='{self.image_path}')"