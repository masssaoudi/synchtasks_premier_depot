#!/usr/bin/env python3
"""
Test de debug pour vérifier le localStorage et l'état du thème
"""

import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def test_theme_debug():
    print("🔍 === DEBUG THÈME ===")
    
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
        
        # 3. Debug du localStorage
        print("💾 Debug localStorage...")
        
        # Vérifier tous les items du localStorage
        all_items = driver.execute_script("""
            let items = {};
            for (let i = 0; i < localStorage.length; i++) {
                const key = localStorage.key(i);
                items[key] = localStorage.getItem(key);
            }
            return items;
        """)
        
        print("  - Tous les items localStorage:")
        for key, value in all_items.items():
            print(f"    * {key}: {value}")
        
        # 4. Debug de l'état du thème
        print("🎨 Debug état du thème...")
        
        html_element = driver.find_element(By.TAG_NAME, "html")
        data_theme = html_element.get_attribute("data-theme")
        classes = html_element.get_attribute("class")
        
        print(f"  - data-theme: {data_theme}")
        print(f"  - classes: {classes}")
        
        # 5. Debug du store Vue
        print("🔧 Debug store Vue...")
        
        # Essayer d'accéder au store via la console
        store_state = driver.execute_script("""
            try {
                // Essayer d'accéder au store Pinia
                if (window.__PINIA__) {
                    const stores = window.__PINIA__._s;
                    for (let key in stores) {
                        if (key.includes('theme')) {
                            return stores[key].$state;
                        }
                    }
                }
                return 'Store non trouvé';
            } catch (e) {
                return 'Erreur: ' + e.message;
            }
        """)
        
        print(f"  - État du store: {store_state}")
        
        # 6. Test manuel du toggle
        print("🔄 Test manuel du toggle...")
        
        # Trouver le bouton thème
        theme_button = driver.find_element(By.CSS_SELECTOR, "button[title*='Passer']")
        
        # État avant
        theme_before = html_element.get_attribute("data-theme")
        localStorage_before = driver.execute_script("return localStorage.getItem('theme')")
        
        print(f"  - Avant toggle: data-theme={theme_before}, localStorage={localStorage_before}")
        
        # Clic
        theme_button.click()
        time.sleep(2)
        
        # État après
        theme_after = html_element.get_attribute("data-theme")
        localStorage_after = driver.execute_script("return localStorage.getItem('theme')")
        
        print(f"  - Après toggle: data-theme={theme_after}, localStorage={localStorage_after}")
        
        # 7. Test de rechargement
        print("🔄 Test de rechargement...")
        
        driver.refresh()
        time.sleep(3)
        
        theme_after_reload = driver.find_element(By.TAG_NAME, "html").get_attribute("data-theme")
        localStorage_after_reload = driver.execute_script("return localStorage.getItem('theme')")
        
        print(f"  - Après rechargement: data-theme={theme_after_reload}, localStorage={localStorage_after_reload}")
        
        # 8. Vérifier si l'initialisation se fait
        print("🔧 Vérification de l'initialisation...")
        
        # Forcer l'initialisation
        init_result = driver.execute_script("""
            try {
                // Essayer d'appeler initTheme
                if (window.__PINIA__) {
                    const stores = window.__PINIA__._s;
                    for (let key in stores) {
                        if (key.includes('theme')) {
                            const store = stores[key];
                            if (store.initTheme) {
                                store.initTheme();
                                return 'InitTheme appelé';
                            }
                        }
                    }
                }
                return 'InitTheme non trouvé';
            } catch (e) {
                return 'Erreur: ' + e.message;
            }
        """)
        
        print(f"  - Résultat initTheme: {init_result}")
        
        # État final
        theme_final = driver.find_element(By.TAG_NAME, "html").get_attribute("data-theme")
        print(f"  - État final: data-theme={theme_final}")
        
    except Exception as e:
        print(f"❌ Erreur lors du debug: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    test_theme_debug() 