#!/usr/bin/env python3
"""
Script de nettoyage pour SynchTasks
Nettoie l'environnement Docker et les fichiers temporaires
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description=""):
    """Exécute une commande et affiche le résultat"""
    print(f"🔄 {description}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        if result.returncode == 0:
            print(f"✅ {description} - Succès")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"⚠️ {description} - Erreur: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ {description} - Exception: {e}")
        return False

def cleanup_docker():
    """Nettoie l'environnement Docker"""
    print("\n🐳 === NETTOYAGE DOCKER ===")
    
    # Arrêter tous les conteneurs
    run_command("docker-compose down", "Arrêt des conteneurs")
    
    # Supprimer les conteneurs arrêtés
    run_command("docker container prune -f", "Suppression des conteneurs arrêtés")
    
    # Supprimer les images non utilisées
    run_command("docker image prune -a -f", "Suppression des images non utilisées")
    
    # Supprimer les volumes non utilisés
    run_command("docker volume prune -f", "Suppression des volumes non utilisés")
    
    # Supprimer les réseaux non utilisés
    run_command("docker network prune -f", "Suppression des réseaux non utilisés")
    
    # Nettoyage complet du système Docker
    run_command("docker system prune -a --volumes -f", "Nettoyage complet Docker")

def cleanup_python():
    """Nettoie les fichiers Python temporaires"""
    print("\n🐍 === NETTOYAGE PYTHON ===")
    
    # Supprimer les fichiers __pycache__
    pycache_dirs = list(Path(".").rglob("__pycache__"))
    for pycache in pycache_dirs:
        try:
            shutil.rmtree(pycache)
            print(f"✅ Supprimé: {pycache}")
        except Exception as e:
            print(f"⚠️ Erreur suppression {pycache}: {e}")
    
    # Supprimer les fichiers .pyc
    pyc_files = list(Path(".").rglob("*.pyc"))
    for pyc_file in pyc_files:
        try:
            pyc_file.unlink()
            print(f"✅ Supprimé: {pyc_file}")
        except Exception as e:
            print(f"⚠️ Erreur suppression {pyc_file}: {e}")

def cleanup_node():
    """Nettoie les fichiers Node.js temporaires"""
    print("\n📦 === NETTOYAGE NODE.JS ===")
    
    # Supprimer node_modules dans frontend-vue
    frontend_node_modules = Path("frontend-vue/node_modules")
    if frontend_node_modules.exists():
        try:
            shutil.rmtree(frontend_node_modules)
            print("✅ Supprimé: frontend-vue/node_modules")
        except Exception as e:
            print(f"⚠️ Erreur suppression node_modules: {e}")
    
    # Supprimer les fichiers de build
    dist_dir = Path("frontend-vue/dist")
    if dist_dir.exists():
        try:
            shutil.rmtree(dist_dir)
            print("✅ Supprimé: frontend-vue/dist")
        except Exception as e:
            print(f"⚠️ Erreur suppression dist: {e}")

def cleanup_logs():
    """Nettoie les fichiers de logs"""
    print("\n📝 === NETTOYAGE LOGS ===")
    
    # Supprimer les fichiers .log
    log_files = list(Path(".").rglob("*.log"))
    for log_file in log_files:
        try:
            log_file.unlink()
            print(f"✅ Supprimé: {log_file}")
        except Exception as e:
            print(f"⚠️ Erreur suppression {log_file}: {e}")

def rebuild_docker():
    """Reconstruit les images Docker"""
    print("\n🔨 === RECONSTRUCTION DOCKER ===")
    
    # Construire le backend
    run_command("docker-compose build backend --no-cache", "Construction backend")
    
    # Construire le frontend
    run_command("docker-compose build frontend --no-cache", "Construction frontend")
    
    # Démarrer les services
    run_command("docker-compose up -d", "Démarrage des services")

def main():
    """Fonction principale"""
    print("🧹 === NETTOYAGE SYNCHTASKS ===")
    
    # Vérifier les arguments
    clean_all = "--all" in sys.argv
    
    if clean_all:
        print("🔄 Nettoyage complet activé")
        cleanup_docker()
        cleanup_python()
        cleanup_node()
        cleanup_logs()
        rebuild_docker()
    else:
        print("🔄 Nettoyage Docker uniquement")
        cleanup_docker()
        rebuild_docker()
    
    print("\n🎉 === NETTOYAGE TERMINÉ ===")
    print("📍 Frontend: http://localhost")
    print("📍 Backend: http://localhost:8000")
    print("📍 API Docs: http://localhost:8000/docs")
    print("📍 MongoDB Express: http://localhost:8081")

if __name__ == "__main__":
    main() 