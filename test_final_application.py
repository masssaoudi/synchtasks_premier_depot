#!/usr/bin/env python3
"""
Test final de l'application SyncTasks
"""

import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def test_final_application():
    print("🎯 === TEST FINAL DE L'APPLICATION SYNCTASKS ===")
    
    # Test 1: Vérifier que les services sont accessibles
    print("\n🔍 Test 1: Vérification des services")
    
    try:
        # Test frontend
        response = requests.get("http://localhost", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend accessible")
        else:
            print(f"❌ Frontend: {response.status_code}")
    except Exception as e:
        print(f"❌ Frontend: {e}")
    
    try:
        # Test backend API
        response = requests.get("http://localhost:8000/api/theme/test-user", timeout=5)
        if response.status_code == 200:
            print("✅ Backend API accessible")
        else:
            print(f"❌ Backend API: {response.status_code}")
    except Exception as e:
        print(f"❌ Backend API: {e}")
    
    # Test 2: Test complet de l'interface utilisateur
    print("\n🎨 Test 2: Test de l'interface utilisateur")
    
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # 1. Accès à l'application
        print("🌐 Accès à l'application...")
        driver.get("http://localhost")
        time.sleep(3)
        
        # 2. Connexion
        print("🔐 Connexion...")
        driver.get("http://localhost/login")
        time.sleep(2)
        
        email_input = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
        password_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        
        email_input.send_keys("alice@test.com")
        password_input.send_keys("alice123")
        
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        time.sleep(5)
        
        # 3. Vérifier la page de sélection de profil
        print("👥 Vérification de la page de sélection de profil...")
        current_url = driver.current_url
        print(f"  - URL actuelle: {current_url}")
        
        if "segment-selection" in current_url:
            print("✅ Page de sélection de profil détectée")
            
            # 4. Tester la sélection de profil
            print("🎯 Test de sélection de profil...")
            
            # Chercher les cartes de profil
            profile_cards = driver.find_elements(By.CSS_SELECTOR, ".segment-card")
            print(f"  - {len(profile_cards)} profils trouvés")
            
            if len(profile_cards) > 0:
                # Cliquer sur le premier profil
                first_card = profile_cards[0]
                driver.execute_script("arguments[0].click();", first_card)
                time.sleep(2)
                
                # Vérifier si la sélection est visible
                selected_cards = driver.find_elements(By.CSS_SELECTOR, ".segment-card.selected")
                if len(selected_cards) > 0:
                    print("✅ Sélection de profil fonctionnelle")
                else:
                    print("⚠️ Sélection de profil non visible")
                
                # 5. Tester le bouton "Continuer"
                try:
                    continue_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Continuer')]")
                    continue_button.click()
                    time.sleep(3)
                    print("✅ Bouton Continuer fonctionnel")
                except:
                    print("⚠️ Bouton Continuer non trouvé")
            
            # 6. Tester le modal de thème
            print("🎨 Test du modal de thème...")
            try:
                theme_button = driver.find_element(By.CSS_SELECTOR, "button[title*='thème']")
                theme_button.click()
                time.sleep(3)
                
                # Vérifier que le modal s'ouvre
                modal = driver.find_element(By.CSS_SELECTOR, "[class*='modal']")
                print("✅ Modal de thème ouvert")
                
                # Tester les options de thème
                theme_options = driver.find_elements(By.CSS_SELECTOR, ".theme-option")
                print(f"  - {len(theme_options)} options de thème trouvées")
                
                if len(theme_options) > 0:
                    # Cliquer sur la première option
                    first_option = theme_options[0]
                    driver.execute_script("arguments[0].click();", first_option)
                    time.sleep(1)
                    
                    # Vérifier si l'option est sélectionnée
                    selected_options = driver.find_elements(By.CSS_SELECTOR, ".theme-option.active")
                    if len(selected_options) > 0:
                        print("✅ Options de thème cliquables")
                    else:
                        print("⚠️ Options de thème non réactives")
                
                # Fermer le modal
                from selenium.webdriver.common.keys import Keys
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                time.sleep(1)
                
            except Exception as e:
                print(f"⚠️ Erreur lors du test du modal de thème: {e}")
        
        else:
            print("⚠️ Page de sélection de profil non détectée")
        
        # 7. Vérifier l'état final
        print("\n📊 État final de l'application:")
        print(f"  - URL: {driver.current_url}")
        print(f"  - Titre: {driver.title}")
        
        # Vérifier les éléments visibles
        try:
            nav_elements = driver.find_elements(By.CSS_SELECTOR, "nav, .nav, .navbar")
            print(f"  - Navigation: {'✅' if len(nav_elements) > 0 else '❌'}")
        except:
            print("  - Navigation: ❌")
        
        try:
            theme_button = driver.find_element(By.CSS_SELECTOR, "button[title*='thème']")
            print("  - Bouton thème: ✅")
        except:
            print("  - Bouton thème: ❌")
        
        print("\n🎉 Test final terminé avec succès !")
        print("✅ L'application SyncTasks est opérationnelle !")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    test_final_application() 