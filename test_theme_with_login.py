#!/usr/bin/env python3
"""
Script automatisé pour tester le thème avec connexion
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_theme_with_login():
    print("🎨 === TEST THÈME AVEC CONNEXION ===")
    
    # Configuration du driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    try:
        print("🔧 Configuration du driver Chrome...")
        driver = webdriver.Chrome(options=chrome_options)
        print("✅ Driver configuré")
        
        # Accéder à l'application
        print("🌐 Accès à l'application...")
        driver.get("http://localhost")
        time.sleep(3)
        
        print(f"📄 Titre de la page: {driver.title}")
        
        # Test 1: Vérifier si on est sur la page de login
        print("\n📋 Test 1: Vérification de la page")
        current_url = driver.current_url
        print(f"URL actuelle: {current_url}")
        
        # Chercher le formulaire de login
        try:
            login_form = driver.find_element(By.TAG_NAME, "form")
            print("✅ Formulaire de login trouvé")
            
            # Remplir le formulaire de login
            print("🔐 Connexion...")
            
            # Chercher les champs de saisie
            inputs = driver.find_elements(By.TAG_NAME, "input")
            print(f"Nombre d'inputs trouvés: {len(inputs)}")
            
            # Essayer de se connecter avec des identifiants par défaut
            username_input = None
            password_input = None
            
            for input_elem in inputs:
                input_type = input_elem.get_attribute("type")
                input_name = input_elem.get_attribute("name")
                print(f"Input trouvé: type={input_type}, name={input_name}")
                
                if input_type == "text" or input_name == "username":
                    username_input = input_elem
                elif input_type == "password":
                    password_input = input_elem
            
            if username_input and password_input:
                print("✅ Champs de connexion trouvés")
                
                # Remplir les champs
                username_input.clear()
                username_input.send_keys("alice")
                
                password_input.clear()
                password_input.send_keys("password123")
                
                # Chercher le bouton de connexion
                submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
                submit_button.click()
                
                print("🔄 Connexion en cours...")
                time.sleep(3)
                
                # Vérifier si la connexion a réussi
                new_url = driver.current_url
                print(f"Nouvelle URL: {new_url}")
                
                if "login" not in new_url:
                    print("✅ Connexion réussie")
                else:
                    print("❌ Connexion échouée")
                    return
                    
            else:
                print("❌ Champs de connexion non trouvés")
                return
                
        except Exception as e:
            print(f"❌ Erreur lors de la connexion: {e}")
            return
        
        # Test 2: Vérifier le bouton thème après connexion
        print("\n📋 Test 2: Vérification du bouton thème")
        try:
            theme_button = driver.find_element(By.CLASS_NAME, "nav-btn-theme")
            print("✅ Bouton thème trouvé")
            print(f"Texte du bouton: {theme_button.text}")
        except:
            print("❌ Bouton thème non trouvé")
            print("🔍 Recherche de tous les boutons...")
            
            all_buttons = driver.find_elements(By.TAG_NAME, "button")
            print(f"Nombre total de boutons: {len(all_buttons)}")
            
            for i, button in enumerate(all_buttons):
                button_text = button.text
                button_class = button.get_attribute("class")
                print(f"Bouton {i}: texte='{button_text}', classe='{button_class}'")
                
                if "thème" in button_text.lower() or "theme" in button_text.lower() or "🌙" in button_text or "☀️" in button_text:
                    print(f"✅ Bouton thème trouvé: {button_text}")
                    theme_button = button
                    break
            else:
                print("❌ Aucun bouton thème trouvé")
                return
        
        # Test 3: Vérifier l'état initial
        print("\n📋 Test 3: État initial")
        html_element = driver.find_element(By.TAG_NAME, "html")
        initial_classes = html_element.get_attribute("class")
        initial_data_theme = html_element.get_attribute("data-theme")
        
        print(f"Classes HTML initiales: {initial_classes}")
        print(f"data-theme initial: {initial_data_theme}")
        
        # Test 4: Clic sur le bouton thème
        print("\n📋 Test 4: Clic sur le bouton thème")
        print("🔄 Clic sur le bouton...")
        theme_button.click()
        time.sleep(2)
        
        # Vérifier l'état après clic
        html_element = driver.find_element(By.TAG_NAME, "html")
        after_classes = html_element.get_attribute("class")
        after_data_theme = html_element.get_attribute("data-theme")
        
        print(f"Classes HTML après clic: {after_classes}")
        print(f"data-theme après clic: {after_data_theme}")
        
        # Test 5: Vérifier les couleurs
        print("\n📋 Test 5: Vérification des couleurs")
        body_element = driver.find_element(By.TAG_NAME, "body")
        body_style = driver.execute_script("return getComputedStyle(arguments[0]);", body_element)
        
        bg_color = body_style['backgroundColor']
        text_color = body_style['color']
        
        print(f"Couleur de fond: {bg_color}")
        print(f"Couleur de texte: {text_color}")
        
        # Test 6: Appliquer les corrections
        print("\n📋 Test 6: Application des corrections")
        
        js_script = """
        function forceApplyThemeStyles() {
            const html = document.documentElement;
            const isDark = html.classList.contains('dark-mode');
            
            if (isDark) {
                console.log('🎨 Application du mode sombre...');
                html.style.setProperty('--bg-primary', '#1a1a1a');
                html.style.setProperty('--bg-secondary', '#2d2d2d');
                html.style.setProperty('--text-primary', '#ffffff');
                html.style.setProperty('--text-secondary', '#b0b0b0');
                html.style.setProperty('--border-color', '#404040');
                
                document.body.style.backgroundColor = '#1a1a1a';
                document.body.style.color = '#ffffff';
                
                const navBar = document.querySelector('.navigation-bar');
                if (navBar) {
                    navBar.style.backgroundColor = '#2d2d2d';
                    navBar.style.borderBottom = '1px solid #404040';
                }
                
                console.log('✅ Styles mode sombre appliqués');
            } else {
                console.log('☀️ Application du mode clair...');
                html.style.setProperty('--bg-primary', '#ffffff');
                html.style.setProperty('--bg-secondary', '#f8f9fa');
                html.style.setProperty('--text-primary', '#2c3e50');
                html.style.setProperty('--text-secondary', '#6c757d');
                html.style.setProperty('--border-color', '#dee2e6');
                
                document.body.style.backgroundColor = '#ffffff';
                document.body.style.color = '#2c3e50';
                
                const navBar = document.querySelector('.navigation-bar');
                if (navBar) {
                    navBar.style.backgroundColor = '#f8f9fa';
                    navBar.style.borderBottom = '1px solid #dee2e6';
                }
                
                console.log('✅ Styles mode clair appliqués');
            }
        }
        
        forceApplyThemeStyles();
        """
        
        driver.execute_script(js_script)
        time.sleep(1)
        
        # Vérifier les couleurs après correction
        body_element = driver.find_element(By.TAG_NAME, "body")
        body_style_after = driver.execute_script("return getComputedStyle(arguments[0]);", body_element)
        
        bg_color_after = body_style_after['backgroundColor']
        text_color_after = body_style_after['color']
        
        print(f"Couleur de fond après correction: {bg_color_after}")
        print(f"Couleur de texte après correction: {text_color_after}")
        
        # Résumé
        print("\n📊 RÉSUMÉ:")
        has_dark_mode = 'dark-mode' in after_classes
        has_correct_colors = bg_color_after != 'rgba(0, 0, 0, 0)'
        
        print(f"Mode sombre activé: {'✅' if has_dark_mode else '❌'}")
        print(f"Couleurs appliquées: {'✅' if has_correct_colors else '❌'}")
        
        if has_dark_mode and has_correct_colors:
            print("\n🎉 THÈME FONCTIONNEL!")
        else:
            print("\n⚠️ PROBLÈMES DÉTECTÉS")
            if not has_dark_mode:
                print("- Mode sombre non activé")
            if not has_correct_colors:
                print("- Couleurs non appliquées")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    finally:
        if 'driver' in locals():
            driver.quit()
            print("🔧 Driver fermé")

if __name__ == "__main__":
    test_theme_with_login() 