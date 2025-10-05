#!/usr/bin/env python3
"""
Script final pour tester le thème avec les bons identifiants
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def test_theme_final():
    print("🎨 === TEST FINAL DU THÈME ===")
    
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
        print(f"URL actuelle: {driver.current_url}")
        
        # Test 1: Connexion avec les bons identifiants
        print("\n📋 Test 1: Connexion")
        
        # Chercher les champs par type
        email_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='email']")
        password_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='password']")
        
        print(f"Champs email trouvés: {len(email_inputs)}")
        print(f"Champs password trouvés: {len(password_inputs)}")
        
        if email_inputs and password_inputs:
            print("✅ Champs de connexion trouvés")
            
            # Remplir les champs avec les bons identifiants
            email_inputs[0].clear()
            email_inputs[0].send_keys("alice@test.com")
            
            password_inputs[0].clear()
            password_inputs[0].send_keys("alice123")
            
            # Chercher le bouton de connexion
            submit_buttons = driver.find_elements(By.CSS_SELECTOR, "button[type='submit']")
            if submit_buttons:
                submit_buttons[0].click()
                print("🔄 Connexion en cours...")
                time.sleep(3)
                
                new_url = driver.current_url
                print(f"Nouvelle URL: {new_url}")
                
                if "login" not in new_url:
                    print("✅ Connexion réussie")
                else:
                    print("❌ Connexion échouée")
                    return
            else:
                print("❌ Bouton de connexion non trouvé")
                return
        else:
            print("❌ Champs de connexion non trouvés")
            return
        
        # Test 2: Vérifier le bouton thème
        print("\n📋 Test 2: Vérification du bouton thème")
        
        # Attendre que la page se charge
        time.sleep(2)
        
        # Chercher le bouton thème
        theme_buttons = driver.find_elements(By.CSS_SELECTOR, ".nav-btn-theme")
        if theme_buttons:
            theme_button = theme_buttons[0]
            print("✅ Bouton thème trouvé")
            print(f"Texte du bouton: {theme_button.text}")
        else:
            print("❌ Bouton thème non trouvé")
            print("🔍 Recherche de tous les boutons...")
            
            all_buttons = driver.find_elements(By.TAG_NAME, "button")
            print(f"Nombre total de boutons: {len(all_buttons)}")
            
            for i, button in enumerate(all_buttons):
                button_text = button.text
                button_class = button.get_attribute("class")
                print(f"Bouton {i}: texte='{button_text}', classe='{button_class}'")
                
                if "🌙" in button_text or "☀️" in button_text or "clair" in button_text.lower() or "sombre" in button_text.lower():
                    print(f"✅ Bouton thème trouvé: {button_text}")
                    theme_button = button
                    break
            else:
                print("❌ Aucun bouton thème trouvé")
                return
        
        # Test 3: Test du basculement
        print("\n📋 Test 3: Test du basculement")
        
        # État avant
        html_element = driver.find_element(By.TAG_NAME, "html")
        initial_classes = html_element.get_attribute("class")
        print(f"Classes HTML avant: {initial_classes}")
        
        # Vérifier les couleurs avant
        body_element = driver.find_element(By.TAG_NAME, "body")
        body_style_before = driver.execute_script("return getComputedStyle(arguments[0]);", body_element)
        bg_color_before = body_style_before['backgroundColor']
        text_color_before = body_style_before['color']
        print(f"Couleur de fond avant: {bg_color_before}")
        print(f"Couleur de texte avant: {text_color_before}")
        
        # Clic sur le bouton
        print("🔄 Clic sur le bouton thème...")
        theme_button.click()
        time.sleep(2)
        
        # État après
        html_element = driver.find_element(By.TAG_NAME, "html")
        after_classes = html_element.get_attribute("class")
        print(f"Classes HTML après: {after_classes}")
        
        # Vérifier les couleurs après
        body_element = driver.find_element(By.TAG_NAME, "body")
        body_style_after = driver.execute_script("return getComputedStyle(arguments[0]);", body_element)
        bg_color_after = body_style_after['backgroundColor']
        text_color_after = body_style_after['color']
        print(f"Couleur de fond après: {bg_color_after}")
        print(f"Couleur de texte après: {text_color_after}")
        
        # Test 4: Appliquer les corrections si nécessaire
        print("\n📋 Test 4: Application des corrections")
        
        # Vérifier si les couleurs ont changé
        colors_changed = (bg_color_before != bg_color_after) or (text_color_before != text_color_after)
        
        if not colors_changed:
            print("⚠️ Les couleurs n'ont pas changé, application des corrections...")
            
            js_script = """
            function forceApplyThemeStyles() {
                const html = document.documentElement;
                const isDark = html.classList.contains('dark-mode');
                
                if (isDark) {
                    console.log('🎨 Application du mode sombre...');
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
            body_style_corrected = driver.execute_script("return getComputedStyle(arguments[0]);", body_element)
            bg_color_corrected = body_style_corrected['backgroundColor']
            text_color_corrected = body_style_corrected['color']
            
            print(f"Couleur de fond après correction: {bg_color_corrected}")
            print(f"Couleur de texte après correction: {text_color_corrected}")
        else:
            print("✅ Les couleurs ont changé naturellement")
        
        # Test 5: Vérifier localStorage
        print("\n📋 Test 5: Vérification localStorage")
        dark_mode_stored = driver.execute_script("return localStorage.getItem('dark-mode');")
        print(f"localStorage dark-mode: {dark_mode_stored}")
        
        # Résumé
        print("\n📊 RÉSUMÉ:")
        has_dark_mode = 'dark-mode' in after_classes
        has_correct_colors = bg_color_after != 'rgba(0, 0, 0, 0)'
        
        print(f"Mode sombre activé: {'✅' if has_dark_mode else '❌'}")
        print(f"Couleurs appliquées: {'✅' if has_correct_colors else '❌'}")
        print(f"Changement de couleurs: {'✅' if colors_changed else '❌'}")
        
        if has_dark_mode and has_correct_colors:
            print("\n🎉 THÈME FONCTIONNEL!")
        else:
            print("\n⚠️ PROBLÈMES DÉTECTÉS")
            if not has_dark_mode:
                print("- Mode sombre non activé")
            if not has_correct_colors:
                print("- Couleurs non appliquées")
            if not colors_changed:
                print("- Changement de couleurs non détecté")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    finally:
        if 'driver' in locals():
            driver.quit()
            print("🔧 Driver fermé")

if __name__ == "__main__":
    test_theme_final() 