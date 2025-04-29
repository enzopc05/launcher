@echo off
title Lanceur de Jeux
echo Démarrage du lanceur de jeux...

:: Vérifier si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python n'est pas installé ou n'est pas dans le PATH.
    echo Veuillez installer Python 3.8 ou supérieur.
    pause
    exit /b 1
)

:: Vérifier si les dépendances sont installées
echo Vérification des dépendances...
python -c "import tkinter, PIL, psutil" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installation des dépendances requises...
    pip install pillow psutil
)

:: Lancer l'application
echo Lancement de l'application...
python main.py

:: Si le programme se termine avec une erreur
if %errorlevel% neq 0 (
    echo Une erreur s'est produite lors de l'exécution du lanceur de jeux.
    echo Veuillez consulter les logs pour plus de détails.
    pause
)