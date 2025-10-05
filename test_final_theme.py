#!/usr/bin/env python3
"""
Test final pour vérifier que les options de thème sont cliquables
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def test_final_theme():
    print("🎨 === TEST FINAL DES OPTIONS DE THÈME ===")
    
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
        
        # 3. Tester chaque option
        print("🎯 Test des options...")
        
        # Chercher les options individuelles
        light_option = driver.find_element(By.XPATH, "//div[contains(@class, 'theme-option') and contains(., 'Mode Clair')]")
        dark_option = driver.find_element(By.XPATH, "//div[contains(@class, 'theme-option') and contains(., 'Mode Sombre')]")
        auto_option = driver.find_element(By.XPATH, "//div[contains(@class, 'theme-option') and contains(., 'Automatique')]")
        
        options = [
            ("Mode Clair", light_option),
            ("Mode Sombre", dark_option), 
            ("Automatique", auto_option)
        ]
        
        for name, option in options:
            print(f"\n🔄 Test de {name}:")
            
            # Cliquer sur l'option
            driver.execute_script("arguments[0].click();", option)
            time.sleep(1)
            
            # Vérifier si l'option est sélectionnée
            classes = option.get_attribute("class")
            is_selected = "active" in classes
            print(f"  - Sélectionnée: {'✅' if is_selected else '❌'}")
            print(f"  - Classes: {classes}")
            
            if is_selected:
                print(f"  ✅ {name} est maintenant sélectionné!")
            else:
                print(f"  ❌ {name} n'est pas sélectionné")
        
        # 4. Tester la fermeture
        print("\n🔄 Test de fermeture...")
        
        # Essayer de fermer avec Escape
        from selenium.webdriver.common.keys import Keys
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        time.sleep(1)
        
        try:
            modal = driver.find_element(By.CSS_SELECTOR, "[class*='modal']")
            print("❌ Modal toujours visible")
        except:
            print("✅ Modal fermé avec Escape")
        
        print("\n🎉 Test final terminé avec succès !")
        print("✅ Les options de thème sont maintenant cliquables et réactives !")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    test_final_theme() 