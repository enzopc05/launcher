import os
import glob
from models.game import Game
from logger import logger

def scan_games_directory(directory_path):
    """Scanne le répertoire spécifié pour trouver les jeux exécutables."""
    games = []
    
    if not os.path.exists(directory_path):
        logger.error(f"Le répertoire {directory_path} n'existe pas.")
        return games
    
    # Extensions de fichiers à considérer comme des jeux exécutables
    executable_extensions = ['.exe', '.lnk', '.bat', '.cmd']
    
    # Parcourir tous les fichiers dans le répertoire
    for ext in executable_extensions:
        for exe_file in glob.glob(os.path.join(directory_path, "**", f"*{ext}"), recursive=True):
            # Extraire le nom du jeu (sans l'extension)
            game_name = os.path.basename(exe_file).replace(ext, "")
            game_dir = os.path.dirname(exe_file)
            
            # Rechercher une image associée (png, jpg, jpeg, ico)
            image_path = None
            image_extensions = ['.png', '.jpg', '.jpeg', '.ico', '.bmp']
            
            # Chercher avec le même nom que l'exécutable
            for img_ext in image_extensions:
                possible_image = os.path.join(game_dir, game_name + img_ext)
                if os.path.exists(possible_image):
                    image_path = possible_image
                    break
            
            # Si aucune image trouvée, chercher dans un sous-dossier "images" s'il existe
            if image_path is None:
                images_dir = os.path.join(game_dir, "images")
                if os.path.exists(images_dir) and os.path.isdir(images_dir):
                    for img_ext in image_extensions:
                        possible_image = os.path.join(images_dir, game_name + img_ext)
                        if os.path.exists(possible_image):
                            image_path = possible_image
                            break
            
            # Si toujours aucune image, chercher une image "icon" ou "logo" dans le dossier
            if image_path is None:
                for img_name in ["icon", "logo", "cover"]:
                    for img_ext in image_extensions:
                        possible_image = os.path.join(game_dir, f"{img_name}{img_ext}")
                        if os.path.exists(possible_image):
                            image_path = possible_image
                            break
                    if image_path:
                        break
            
            # Créer un objet Game et l'ajouter à la liste
            game = Game(game_name, exe_file, image_path)
            games.append(game)
    
    # Tri des jeux par nom
    games.sort(key=lambda g: g.name.lower())
    
    logger.info(f"{len(games)} jeux trouvés dans {directory_path}")
    return games