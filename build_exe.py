"""
Script pour créer un exécutable Windows du lanceur de jeux.
Nécessite PyInstaller : pip install pyinstaller
"""

import PyInstaller.__main__
import os
import shutil

def build_executable():
    """Construit l'exécutable Windows avec PyInstaller."""
    print("Création de l'exécutable du lanceur de jeux...")
    
    # Assurer que le dossier assets existe
    if not os.path.exists("assets"):
        os.makedirs("assets")
    
    # Créer un dossier dist s'il n'existe pas
    if not os.path.exists("dist"):
        os.makedirs("dist")
    
    # Configurer les options de PyInstaller
    PyInstaller.__main__.run([
        "main.py",               # Script principal
        "--name=LanceurDeJeux",  # Nom de l'exécutable
        "--windowed",            # Application GUI (sans console)
        "--onefile",             # Créer un seul fichier EXE
        "--log-level=INFO",
        "--add-data=assets;assets",  # Inclure le dossier assets
        # Icône de l'application si elle existe
        "--icon=assets/icon.ico" if os.path.exists("assets/icon.ico") else "",
        # Exclure certains modules non nécessaires pour réduire la taille
        "--exclude-module=matplotlib",
        "--exclude-module=numpy",
        "--exclude-module=pandas",
        # Si vous avez des dépendances supplémentaires, ajoutez-les ici
        "--hidden-import=PIL",
        "--hidden-import=tkinter",
        "--hidden-import=psutil",
    ])
    
    print("Exécutable créé avec succès dans le dossier 'dist'")
    print("Vous pouvez maintenant distribuer le fichier 'LanceurDeJeux.exe'")

if __name__ == "__main__":
    build_executable()