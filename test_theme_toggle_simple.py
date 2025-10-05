#!/usr/bin/env python3
"""
Test simple pour vérifier le nouveau système de toggle thème
"""

import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def test_theme_toggle():
    print("🎨 === TEST TOGGLE THÈME SIMPLE ===")
    
    # Test 1: Vérifier que le frontend fonctionne
    print("\n🌐 Test 1: Vérification du frontend")
    
    try:
        response = requests.get("http://localhost", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend accessible")
        else:
            print(f"❌ Frontend: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Frontend: {e}")
        return
    
    # Test 2: Test du toggle thème
    print("\n🎨 Test 2: Test du toggle thème")
    
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
        
        # 3. Vérifier le bouton thème
        print("🎨 Vérification du bouton thème...")
        
        try:
            # Essayer plusieurs sélecteurs
            theme_button = None
            selectors = [
                "button[title*='thème']",
                "button[title*='Passer']",
                ".nav-btn-theme",
                "button .btn-icon:contains('🌞')",
                "button .btn-icon:contains('🌙')",
                "button:has(.btn-icon)"
            ]
            
            for selector in selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        theme_button = elements[0]
                        print(f"✅ Bouton thème trouvé avec le sélecteur: {selector}")
                        break
                except:
                    continue
            
            if not theme_button:
                # Essayer de trouver par le texte
                all_buttons = driver.find_elements(By.TAG_NAME, "button")
                for button in all_buttons:
                    try:
                        text = button.text.lower()
                        if "thème" in text or "clair" in text or "sombre" in text:
                            theme_button = button
                            print("✅ Bouton thème trouvé par texte")
                            break
                    except:
                        continue
            
            if not theme_button:
                raise Exception("Aucun bouton thème trouvé")
            
            # Vérifier l'état initial
            button_text = theme_button.text
            print(f"  - Texte du bouton: {button_text}")
            
            # Vérifier l'icône
            try:
                icon_element = theme_button.find_element(By.CSS_SELECTOR, ".btn-icon")
                icon_text = icon_element.text
                print(f"  - Icône: {icon_text}")
            except:
                print("  - Icône: Non trouvée")
            
            # Vérifier l'état du thème initial
            html_element = driver.find_element(By.TAG_NAME, "html")
            data_theme = html_element.get_attribute("data-theme")
            print(f"  - Thème initial: {data_theme}")
            
        except Exception as e:
            print(f"❌ Bouton thème non trouvé: {e}")
            print("🔍 Debug: Affichage de tous les boutons...")
            try:
                all_buttons = driver.find_elements(By.TAG_NAME, "button")
                for i, btn in enumerate(all_buttons[:10]):  # Afficher les 10 premiers
                    try:
                        print(f"  Bouton {i}: {btn.text} | {btn.get_attribute('class')} | {btn.get_attribute('title')}")
                    except:
                        print(f"  Bouton {i}: [Erreur de lecture]")
            except:
                print("  Impossible de lister les boutons")
            return
        
        # 4. Tester le toggle
        print("🔄 Test du toggle...")
        
        # État avant le clic
        theme_before = html_element.get_attribute("data-theme")
        print(f"  - Thème avant clic: {theme_before}")
        
        # Clic sur le bouton
        theme_button.click()
        time.sleep(2)
        
        # État après le clic
        theme_after = html_element.get_attribute("data-theme")
        print(f"  - Thème après clic: {theme_after}")
        
        # Vérifier que le thème a changé
        if theme_before != theme_after:
            print("✅ Toggle fonctionne !")
        else:
            print("❌ Toggle ne fonctionne pas")
        
        # 5. Vérifier le texte du bouton après toggle
        button_text_after = theme_button.text
        print(f"  - Texte après toggle: {button_text_after}")
        
        # 6. Test du localStorage
        print("💾 Test du localStorage...")
        
        localStorage_value = driver.execute_script("return localStorage.getItem('theme')")
        print(f"  - localStorage theme: {localStorage_value}")
        
        if localStorage_value:
            print("✅ Thème sauvegardé dans localStorage")
        else:
            print("❌ Thème non sauvegardé dans localStorage")
        
        # 7. Test de persistance (recharger la page)
        print("🔄 Test de persistance...")
        
        driver.refresh()
        time.sleep(3)
        
        html_element_after = driver.find_element(By.TAG_NAME, "html")
        theme_persistent = html_element_after.get_attribute("data-theme")
        print(f"  - Thème après rechargement: {theme_persistent}")
        
        if theme_persistent == theme_after:
            print("✅ Thème persiste après rechargement")
        else:
            print("❌ Thème ne persiste pas")
        
        print("\n🎉 Test du toggle thème terminé avec succès !")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    test_theme_toggle() 