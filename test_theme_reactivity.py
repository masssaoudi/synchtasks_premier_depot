#!/usr/bin/env python3
"""
Script de test pour vérifier la réactivité des options de thème
"""

import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def test_theme_reactivity():
    print("🎨 === TEST DE RÉACTIVITÉ DES OPTIONS DE THÈME ===")
    
    # Configuration Chrome
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # 1. Connexion
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
        
        # 2. Ouvrir le modal de thème
        print("🔄 Ouverture du modal...")
        theme_button = driver.find_element(By.CSS_SELECTOR, "button[title*='thème']")
        theme_button.click()
        time.sleep(3)
        
        # 3. Chercher les options de thème
        print("🔍 Recherche des options...")
        theme_options = driver.find_elements(By.CSS_SELECTOR, "[class*='theme-option'], .theme-option")
        
        if not theme_options:
            print("❌ Aucune option trouvée")
            return
        
        print(f"✅ {len(theme_options)} options trouvées")
        
        # 4. Tester chaque option individuellement
        for i, option in enumerate(theme_options):
            try:
                print(f"\n🎯 Test de l'option {i+1}:")
                
                # Obtenir le texte de l'option
                option_text = option.text.strip()
                print(f"  - Texte: {option_text}")
                
                # Obtenir les classes avant le clic
                classes_before = option.get_attribute("class")
                print(f"  - Classes avant: {classes_before}")
                
                # Cliquer sur l'option
                driver.execute_script("arguments[0].click();", option)
                time.sleep(1)
                
                # Obtenir les classes après le clic
                classes_after = option.get_attribute("class")
                print(f"  - Classes après: {classes_after}")
                
                # Vérifier si quelque chose a changé
                if classes_before != classes_after:
                    print(f"  ✅ Changement détecté!")
                else:
                    print(f"  ⚠️ Aucun changement visuel détecté")
                
                # Vérifier si l'option est maintenant sélectionnée
                is_selected = any(keyword in classes_after.lower() for keyword in ['selected', 'active', 'chosen'])
                print(f"  - Sélectionnée: {'✅' if is_selected else '❌'}")
                
                # Vérifier le style
                style = option.get_attribute("style")
                if style:
                    print(f"  - Style: {style}")
                
                # Vérifier les attributs data
                data_theme = option.get_attribute("data-theme")
                if data_theme:
                    print(f"  - Data-theme: {data_theme}")
                
            except Exception as e:
                print(f"  ❌ Erreur: {e}")
        
        # 5. Tester l'application du thème
        print("\n🔄 Test de l'application du thème...")
        
        # Chercher le bouton Appliquer avec différents sélecteurs
        apply_selectors = [
            "button:contains('Appliquer')",
            "button:contains('Apply')",
            "button[type='submit']",
            ".btn-primary",
            ".apply-button"
        ]
        
        apply_button = None
        for selector in apply_selectors:
            try:
                if "contains" in selector:
                    text = selector.split("'")[1]
                    apply_button = driver.find_element(By.XPATH, f"//button[contains(text(), '{text}')]")
                else:
                    apply_button = driver.find_element(By.CSS_SELECTOR, selector)
                print(f"✅ Bouton Appliquer trouvé avec: {selector}")
                break
            except:
                continue
        
        if apply_button:
            print("🔄 Clic sur Appliquer...")
            apply_button.click()
            time.sleep(2)
            
            # Vérifier que le modal se ferme
            try:
                modal = driver.find_element(By.CSS_SELECTOR, "[class*='modal']")
                print("❌ Modal toujours visible")
            except:
                print("✅ Modal fermé")
        else:
            print("❌ Bouton Appliquer non trouvé")
            
            # Essayer de fermer avec Escape
            print("🔄 Tentative de fermeture avec Escape...")
            from selenium.webdriver.common.keys import Keys
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
            time.sleep(1)
            
            try:
                modal = driver.find_element(By.CSS_SELECTOR, "[class*='modal']")
                print("❌ Modal toujours visible après Escape")
            except:
                print("✅ Modal fermé avec Escape")
        
        # 6. Vérifier l'état final
        print("\n🔍 Vérification de l'état final...")
        
        # Vérifier si un thème a été appliqué
        body_element = driver.find_element(By.TAG_NAME, "body")
        body_theme = body_element.get_attribute("data-theme")
        print(f"  - Thème appliqué au body: {body_theme}")
        
        # Vérifier les styles CSS
        body_style = body_element.get_attribute("style")
        if body_style:
            print(f"  - Style du body: {body_style}")
        
        print("🎉 Test de réactivité terminé !")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    test_theme_reactivity() 