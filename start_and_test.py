#!/usr/bin/env python3
"""
Script de démarrage et test automatique pour SynchTasks
Démarre l'application Docker et lance les tests de validation
"""

import subprocess
import time
import sys
import os

def run_command(command, description, wait=True):
    """Exécute une commande avec gestion d'erreur"""
    print(f"🔄 {description}...")
    try:
        if wait:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            print(f"✅ {description} - Succès")
            return True
        else:
            subprocess.Popen(command, shell=True)
            print(f"✅ {description} - Démarré en arrière-plan")
            return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Échec: {e.stderr}")
        return False

def wait_for_service(url, service_name, max_attempts=30):
    """Attend qu'un service soit disponible"""
    import requests
    
    print(f"⏳ Attente de {service_name}...")
    for attempt in range(max_attempts):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {service_name} est prêt!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        print(f"   Tentative {attempt + 1}/{max_attempts}...")
        time.sleep(2)
    
    print(f"❌ {service_name} n'est pas accessible après {max_attempts} tentatives")
    return False

def main():
    print("🐳 SynchTasks - Démarrage et Test Automatisé")
    print("=" * 50)
    
    # Vérifier que Docker est disponible
    if not run_command("docker --version", "Vérification de Docker", wait=True):
        print("❌ Docker n'est pas disponible. Veuillez l'installer.")
        sys.exit(1)
    
    # Arrêter les conteneurs existants
    print("🧹 Nettoyage des conteneurs existants...")
    subprocess.run("docker compose down", shell=True)
    
    # Démarrer l'application
    print("🚀 Démarrage de l'application SynchTasks...")
    if not run_command("docker compose up -d", "Démarrage des conteneurs", wait=True):
        print("❌ Échec du démarrage des conteneurs")
        sys.exit(1)
    
    # Attendre que les services soient prêts
    print("⏳ Attente du démarrage des services...")
    time.sleep(10)
    
    # Vérifier que les services sont accessibles
    services = [
        ("http://localhost:8000", "Backend API"),
        ("http://localhost", "Frontend"),
        ("http://localhost:8081", "Mongo Express")
    ]
    
    all_services_ready = True
    for url, name in services:
        if not wait_for_service(url, name):
            all_services_ready = False
    
    if not all_services_ready:
        print("⚠️ Certains services ne sont pas prêts, mais on continue...")
    
    # Lancer les tests automatisés
    print("\n🧪 Lancement des tests automatisés...")
    if os.path.exists("test_docker_deployment.py"):
        if run_command("python test_docker_deployment.py", "Tests automatisés", wait=True):
            print("✅ Tests automatisés terminés avec succès!")
        else:
            print("⚠️ Tests automatisés échoués, mais l'application peut fonctionner")
    else:
        print("⚠️ Script de test non trouvé, tests manuels requis")
    
    # Afficher les informations d'accès
    print("\n" + "=" * 50)
    print("🎉 Application SynchTasks démarrée!")
    print("\n🌐 Accès aux services:")
    print("   Frontend: http://localhost")
    print("   Backend API: http://localhost:8000")
    print("   Documentation API: http://localhost:8000/docs")
    print("   Mongo Express: http://localhost:8081")
    print("\n📋 Commandes utiles:")
    print("   Voir les logs: docker compose logs -f")
    print("   Arrêter: docker compose down")
    print("   Redémarrer: docker compose restart")
    print("   Tests manuels: python test_docker_deployment.py")
    
    # Optionnel: ouvrir le navigateur
    try:
        import webbrowser
        print("\n🌐 Ouverture du frontend dans le navigateur...")
        webbrowser.open("http://localhost")
    except:
        pass

if __name__ == "__main__":
    main() 