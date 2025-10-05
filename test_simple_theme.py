#!/usr/bin/env python3
"""
Test simple pour vérifier que les options de thème sont cliquables
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def test_simple_theme():
    print("🎨 === TEST SIMPLE DES OPTIONS DE THÈME ===")
    
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
        
        # 2. Ouvrir le modal
        print("🔄 Ouverture du modal...")
        theme_button = driver.find_element(By.CSS_SELECTOR, "button[title*='thème']")
        theme_button.click()
        time.sleep(3)
        
        # 3. Lister toutes les options
        print("🔍 Recherche des options...")
        all_options = driver.find_elements(By.CSS_SELECTOR, ".theme-option")
        
        print(f"✅ {len(all_options)} options trouvées")
        
        for i, option in enumerate(all_options):
            try:
                # Obtenir le texte de l'option
                option_text = option.text.strip()
                print(f"\n🎯 Option {i+1}: {option_text[:50]}...")
                
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
                    print(f"  ⚠️ Aucun changement")
                
                # Vérifier si l'option est sélectionnée
                is_selected = "active" in classes_after
                print(f"  - Sélectionnée: {'✅' if is_selected else '❌'}")
                
            except Exception as e:
                print(f"  ❌ Erreur: {e}")
        
        # 4. Fermer le modal
        print("\n🔄 Fermeture du modal...")
        from selenium.webdriver.common.keys import Keys
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        time.sleep(1)
        
        try:
            modal = driver.find_element(By.CSS_SELECTOR, "[class*='modal']")
            print("❌ Modal toujours visible")
        except:
            print("✅ Modal fermé")
        
        print("\n🎉 Test simple terminé !")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    test_simple_theme() 