#!/usr/bin/env python3
"""
Script de démarrage robuste pour SyncTasks API
Évite les problèmes de relance en boucle et gère mieux les signaux
"""

import os
import sys
import signal
import uvicorn
from pathlib import Path

def signal_handler(signum, frame):
    """Gestionnaire de signal pour arrêt propre"""
    print(f"\n🛑 Signal {signum} reçu. Arrêt en cours...")
    sys.exit(0)

def main():
    """Fonction principale de démarrage"""
    # Configuration des signaux
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Vérification de l'environnement
    print("🚀 Démarrage de SyncTasks API...")
    
    # Vérifier que nous sommes dans le bon répertoire
    if not Path("main.py").exists():
        print("❌ Erreur: main.py non trouvé. Assurez-vous d'être dans le répertoire du projet.")
        sys.exit(1)
    
    # Configuration uvicorn
    config = uvicorn.Config(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # Désactiver le reload automatique pour éviter les boucles
        log_level="info",
        access_log=True
    )
    
    # Créer et démarrer le serveur
    server = uvicorn.Server(config)
    
    try:
        print("✅ Serveur démarré avec succès!")
        print("📡 API disponible sur: http://localhost:8000")
        print("📚 Documentation: http://localhost:8000/docs")
        print("🛑 Appuyez sur Ctrl+C pour arrêter")
        
        server.run()
        
    except KeyboardInterrupt:
        print("\n🛑 Arrêt demandé par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur lors du démarrage: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 