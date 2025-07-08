@echo off
REM Script de démarrage pour le Générateur de Scripts Émotionnels (Windows)
REM Usage: start.bat

echo 🚀 Démarrage du Générateur de Scripts Émotionnels...
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé ou n'est pas dans le PATH.
    echo Veuillez installer Python depuis https://python.org
    pause
    exit /b 1
)

REM Vérifier si l'environnement virtuel existe
if not exist "venv" (
    echo 📦 Création de l'environnement virtuel...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Erreur lors de la création de l'environnement virtuel.
        pause
        exit /b 1
    )
)

REM Activer l'environnement virtuel
echo 🔧 Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Installer les dépendances si nécessaire
if not exist "venv\Scripts\pip.exe" (
    echo 📚 Installation des dépendances...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Erreur lors de l'installation des dépendances.
        pause
        exit /b 1
    )
)

REM Vérifier que le fichier principal existe
if not exist "src\main.py" (
    echo ❌ Le fichier src\main.py n'existe pas.
    pause
    exit /b 1
)

echo ✅ Environnement prêt !
echo.
echo 🌐 Démarrage du serveur...
echo 📱 L'application sera accessible à l'adresse : http://localhost:8080
echo.
echo Pour arrêter le serveur, appuyez sur Ctrl+C
echo.

REM Démarrer l'application
python src\main.py

pause

