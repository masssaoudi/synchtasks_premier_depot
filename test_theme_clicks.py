#!/usr/bin/env python3
"""
Script de test pour vérifier que les options de thème sont cliquables
"""

import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def test_theme_clicks():
    print("🎨 === TEST DES CLICS SUR LES OPTIONS DE THÈME ===")
    
    # Configuration Chrome
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # 1. Aller à l'application
        print("🌐 Accès à l'application...")
        driver.get("http://localhost")
        time.sleep(3)
        
        # 2. Se connecter
        print("🔐 Connexion...")
        driver.get("http://localhost/login")
        time.sleep(2)
        
        # Remplir le formulaire
        email_input = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
        password_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        
        email_input.send_keys("alice@test.com")
        password_input.send_keys("alice123")
        
        # Cliquer sur se connecter
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        time.sleep(5)
        
        # 3. Attendre que la page soit chargée
        print("⏳ Attente du chargement...")
        time.sleep(3)
        
        # 4. Chercher le bouton thème
        print("🔍 Recherche du bouton thème...")
        theme_button = None
        
        # Essayer différents sélecteurs
        selectors = [
            "button[title*='thème']",
            "button[title*='theme']", 
            ".nav-btn-theme",
            ".btn-theme",
            "button:has-text('🎨')",
            "button:has-text('Thème')"
        ]
        
        for selector in selectors:
            try:
                if "has-text" in selector:
                    theme_button = driver.find_element(By.XPATH, f"//button[contains(text(), '🎨') or contains(text(), 'Thème')]")
                else:
                    theme_button = driver.find_element(By.CSS_SELECTOR, selector)
                print(f"✅ Bouton thème trouvé avec: {selector}")
                break
            except:
                continue
        
        if not theme_button:
            print("❌ Bouton thème non trouvé")
            return
        
        # 5. Cliquer sur le bouton thème
        print("🔄 Clic sur le bouton thème...")
        theme_button.click()
        time.sleep(3)
        
        # 6. Vérifier que le modal s'ouvre
        print("🔍 Vérification du modal...")
        modal = None
        
        modal_selectors = [
            ".theme-modal",
            ".modal",
            "[class*='modal']",
            "[class*='overlay']",
            "div[role='dialog']"
        ]
        
        for selector in modal_selectors:
            try:
                modal = driver.find_element(By.CSS_SELECTOR, selector)
                print(f"✅ Modal trouvé avec: {selector}")
                break
            except:
                continue
        
        if not modal:
            print("❌ Modal non trouvé")
            print("🔍 Éléments visibles:")
            elements = driver.find_elements(By.CSS_SELECTOR, "div")
            for elem in elements[:10]:
                try:
                    class_name = elem.get_attribute("class")
                    if "modal" in class_name or "overlay" in class_name:
                        print(f"  - Classe: {class_name}")
                except:
                    pass
            return
        
        # 7. Tester les clics sur les options
        print("🎯 Test des clics sur les options...")
        
        # Chercher les options de thème
        theme_options = driver.find_elements(By.CSS_SELECTOR, ".theme-option, [class*='theme-option']")
        
        if not theme_options:
            print("❌ Aucune option de thème trouvée")
            return
        
        print(f"✅ {len(theme_options)} options trouvées")
        
        # Tester chaque option
        for i, option in enumerate(theme_options):
            try:
                print(f"🔄 Test de l'option {i+1}...")
                
                # Cliquer sur l'option
                option.click()
                time.sleep(1)
                
                # Vérifier si l'option est sélectionnée
                is_selected = "selected" in option.get_attribute("class") or "active" in option.get_attribute("class")
                print(f"  - Option {i+1} cliquée: {'✅' if is_selected else '❌'}")
                
            except Exception as e:
                print(f"  - Erreur lors du clic sur l'option {i+1}: {e}")
        
        # 8. Tester le bouton Appliquer
        print("🔄 Test du bouton Appliquer...")
        try:
            apply_button = driver.find_element(By.CSS_SELECTOR, "button:contains('Appliquer'), button:contains('Apply')")
            apply_button.click()
            print("✅ Bouton Appliquer cliqué")
            time.sleep(2)
        except:
            print("❌ Bouton Appliquer non trouvé")
        
        # 9. Vérifier que le modal se ferme
        print("🔍 Vérification de la fermeture du modal...")
        try:
            modal_after = driver.find_element(By.CSS_SELECTOR, ".theme-modal, .modal")
            print("❌ Modal toujours visible")
        except:
            print("✅ Modal fermé")
        
        print("🎉 Test terminé avec succès !")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    test_theme_clicks() 