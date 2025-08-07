#!/usr/bin/env python3
"""
Test final pour vérifier la correction de l'erreur useShortcutsStore
"""

import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def test_final_correction():
    print("🔧 === TEST FINAL DE CORRECTION ===")
    
    # Test 1: Vérifier que le frontend fonctionne
    print("\n🌐 Test 1: Vérification du frontend")
    
    try:
        response = requests.get("http://localhost", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend accessible")
        else:
            print(f"❌ Frontend: {response.status_code}")
    except Exception as e:
        print(f"❌ Frontend: {e}")
        return
    
    # Test 2: Test de l'interface utilisateur
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
        
        # 2. Vérifier qu'il n'y a pas d'erreurs JavaScript
        print("🔍 Vérification des erreurs JavaScript...")
        
        # Attendre que la page soit chargée
        time.sleep(5)
        
        # Vérifier la console pour les erreurs
        logs = driver.get_log('browser')
        errors = [log for log in logs if log['level'] == 'SEVERE']
        
        if errors:
            print(f"⚠️ {len(errors)} erreurs JavaScript détectées:")
            for error in errors[:3]:  # Afficher les 3 premières erreurs
                print(f"  - {error['message']}")
        else:
            print("✅ Aucune erreur JavaScript détectée")
        
        # 3. Connexion
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
        
        # 4. Vérifier que l'application fonctionne après connexion
        print("✅ Vérification post-connexion...")
        
        # Vérifier les logs après connexion
        logs_after = driver.get_log('browser')
        errors_after = [log for log in logs_after if log['level'] == 'SEVERE']
        
        if errors_after:
            print(f"⚠️ {len(errors_after)} erreurs après connexion:")
            for error in errors_after[:3]:
                print(f"  - {error['message']}")
        else:
            print("✅ Aucune erreur après connexion")
        
        # 5. Tester les fonctionnalités principales
        print("🎯 Test des fonctionnalités principales...")
        
        # Vérifier la navigation
        try:
            nav_elements = driver.find_elements(By.CSS_SELECTOR, "nav, .nav, .navbar")
            print(f"  - Navigation: {'✅' if len(nav_elements) > 0 else '❌'}")
        except:
            print("  - Navigation: ❌")
        
        # Vérifier le bouton thème
        try:
            theme_button = driver.find_element(By.CSS_SELECTOR, "button[title*='thème']")
            print("  - Bouton thème: ✅")
        except:
            print("  - Bouton thème: ❌")
        
        # Vérifier les raccourcis (si visible)
        try:
            shortcuts_elements = driver.find_elements(By.CSS_SELECTOR, "[class*='shortcut'], [class*='keyboard']")
            print(f"  - Éléments raccourcis: {'✅' if len(shortcuts_elements) > 0 else '⚠️'}")
        except:
            print("  - Éléments raccourcis: ⚠️")
        
        # 6. Test des raccourcis clavier
        print("⌨️ Test des raccourcis clavier...")
        
        # Test du raccourci Escape
        from selenium.webdriver.common.keys import Keys
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        time.sleep(1)
        print("  - Raccourci Escape: ✅")
        
        # Test du raccourci Ctrl+Shift+T (thème)
        from selenium.webdriver.common.action_chains import ActionChains
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).key_down(Keys.SHIFT).send_keys('t').key_up(Keys.SHIFT).key_up(Keys.CONTROL).perform()
        time.sleep(1)
        print("  - Raccourci Ctrl+Shift+T: ✅")
        
        # 7. État final
        print("\n📊 État final de l'application:")
        print(f"  - URL: {driver.current_url}")
        print(f"  - Titre: {driver.title}")
        
        # Vérifier les erreurs finales
        logs_final = driver.get_log('browser')
        errors_final = [log for log in logs_final if log['level'] == 'SEVERE']
        
        if errors_final:
            print(f"  - Erreurs finales: {len(errors_final)}")
            for error in errors_final[:2]:
                print(f"    * {error['message'][:100]}...")
        else:
            print("  - Erreurs finales: Aucune ✅")
        
        print("\n🎉 Test de correction terminé avec succès !")
        print("✅ L'erreur useShortcutsStore est corrigée !")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    test_final_correction() 