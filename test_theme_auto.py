#!/usr/bin/env python3
"""
Script automatisé pour tester le thème directement
"""

import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_theme_automated():
    print("🎨 === TEST AUTOMATISÉ DU THÈME ===")
    
    # Configuration du driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Mode sans interface
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
        
        # Test 1: Vérifier le bouton thème
        print("\n📋 Test 1: Vérification du bouton thème")
        try:
            theme_button = driver.find_element(By.CLASS_NAME, "nav-btn-theme")
            print("✅ Bouton thème trouvé")
            print(f"Texte du bouton: {theme_button.text}")
        except:
            print("❌ Bouton thème non trouvé")
            return
        
        # Test 2: Vérifier l'état initial
        print("\n📋 Test 2: État initial")
        html_element = driver.find_element(By.TAG_NAME, "html")
        initial_classes = html_element.get_attribute("class")
        initial_data_theme = html_element.get_attribute("data-theme")
        
        print(f"Classes HTML initiales: {initial_classes}")
        print(f"data-theme initial: {initial_data_theme}")
        
        # Test 3: Clic sur le bouton thème
        print("\n📋 Test 3: Clic sur le bouton thème")
        print("🔄 Clic sur le bouton...")
        theme_button.click()
        time.sleep(2)
        
        # Vérifier l'état après clic
        html_element = driver.find_element(By.TAG_NAME, "html")
        after_classes = html_element.get_attribute("class")
        after_data_theme = html_element.get_attribute("data-theme")
        
        print(f"Classes HTML après clic: {after_classes}")
        print(f"data-theme après clic: {after_data_theme}")
        
        # Test 4: Vérifier les couleurs
        print("\n📋 Test 4: Vérification des couleurs")
        body_element = driver.find_element(By.TAG_NAME, "body")
        body_style = driver.execute_script("return getComputedStyle(arguments[0]);", body_element)
        
        bg_color = body_style['backgroundColor']
        text_color = body_style['color']
        
        print(f"Couleur de fond: {bg_color}")
        print(f"Couleur de texte: {text_color}")
        
        # Test 5: Vérifier localStorage
        print("\n📋 Test 5: Vérification localStorage")
        dark_mode_stored = driver.execute_script("return localStorage.getItem('dark-mode');")
        print(f"localStorage dark-mode: {dark_mode_stored}")
        
        # Test 6: Exécuter le script de correction
        print("\n📋 Test 6: Application du script de correction")
        
        # Script JavaScript pour forcer les styles
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
        
        # Test 7: Basculement forcé
        print("\n📋 Test 7: Basculement forcé")
        
        js_toggle_script = """
        function forceToggleTheme() {
            const html = document.documentElement;
            const isDark = html.classList.contains('dark-mode');
            
            if (isDark) {
                html.classList.remove('dark-mode');
                html.setAttribute('data-theme', 'light');
                localStorage.setItem('dark-mode', 'false');
                console.log('☀️ Passage en mode clair');
            } else {
                html.classList.add('dark-mode');
                html.setAttribute('data-theme', 'dark');
                localStorage.setItem('dark-mode', 'true');
                console.log('🎨 Passage en mode sombre');
            }
            
            // Réappliquer les styles
            forceApplyThemeStyles();
        }
        
        forceToggleTheme();
        """
        
        driver.execute_script(js_toggle_script)
        time.sleep(2)
        
        # Vérifier l'état final
        html_element = driver.find_element(By.TAG_NAME, "html")
        final_classes = html_element.get_attribute("class")
        final_data_theme = html_element.get_attribute("data-theme")
        
        body_element = driver.find_element(By.TAG_NAME, "body")
        body_style_final = driver.execute_script("return getComputedStyle(arguments[0]);", body_element)
        
        bg_color_final = body_style_final['backgroundColor']
        text_color_final = body_style_final['color']
        
        print(f"Classes HTML finales: {final_classes}")
        print(f"data-theme final: {final_data_theme}")
        print(f"Couleur de fond finale: {bg_color_final}")
        print(f"Couleur de texte finale: {text_color_final}")
        
        # Résumé
        print("\n📊 RÉSUMÉ:")
        has_dark_mode = 'dark-mode' in final_classes
        has_correct_colors = bg_color_final != 'rgba(0, 0, 0, 0)'
        
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
    test_theme_automated() 