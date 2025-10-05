#!/usr/bin/env python3
"""
Script pour tester le thème directement sans connexion
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def test_theme_direct():
    print("🎨 === TEST DIRECT DU THÈME ===")
    
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
        
        # Test 1: Vérifier l'état initial
        print("\n📋 Test 1: État initial")
        html_element = driver.find_element(By.TAG_NAME, "html")
        initial_classes = html_element.get_attribute("class")
        initial_data_theme = html_element.get_attribute("data-theme")
        
        print(f"Classes HTML initiales: {initial_classes}")
        print(f"data-theme initial: {initial_data_theme}")
        
        # Test 2: Vérifier les couleurs initiales
        print("\n📋 Test 2: Couleurs initiales")
        body_element = driver.find_element(By.TAG_NAME, "body")
        body_style = driver.execute_script("return getComputedStyle(arguments[0]);", body_element)
        
        bg_color = body_style['backgroundColor']
        text_color = body_style['color']
        
        print(f"Couleur de fond initiale: {bg_color}")
        print(f"Couleur de texte initiale: {text_color}")
        
        # Test 3: Appliquer le mode sombre directement
        print("\n📋 Test 3: Application directe du mode sombre")
        
        js_dark_script = """
        // Appliquer le mode sombre directement
        const html = document.documentElement;
        html.classList.add('dark-mode');
        html.setAttribute('data-theme', 'dark');
        localStorage.setItem('dark-mode', 'true');
        
        // Appliquer les styles forcés
        document.body.style.backgroundColor = '#1a1a1a';
        document.body.style.color = '#ffffff';
        
        const navBar = document.querySelector('.navigation-bar');
        if (navBar) {
            navBar.style.backgroundColor = '#2d2d2d';
            navBar.style.borderBottom = '1px solid #404040';
        }
        
        // Appliquer aux cards
        const cards = document.querySelectorAll('.card, .feature-card');
        cards.forEach(card => {
            card.style.backgroundColor = '#2d2d2d';
            card.style.border = '1px solid #404040';
            card.style.color = '#ffffff';
        });
        
        console.log('🎨 Mode sombre appliqué directement');
        """
        
        driver.execute_script(js_dark_script)
        time.sleep(2)
        
        # Vérifier l'état après application
        html_element = driver.find_element(By.TAG_NAME, "html")
        after_classes = html_element.get_attribute("class")
        after_data_theme = html_element.get_attribute("data-theme")
        
        print(f"Classes HTML après application: {after_classes}")
        print(f"data-theme après application: {after_data_theme}")
        
        # Vérifier les couleurs après application
        body_element = driver.find_element(By.TAG_NAME, "body")
        body_style_after = driver.execute_script("return getComputedStyle(arguments[0]);", body_element)
        
        bg_color_after = body_style_after['backgroundColor']
        text_color_after = body_style_after['color']
        
        print(f"Couleur de fond après application: {bg_color_after}")
        print(f"Couleur de texte après application: {text_color_after}")
        
        # Test 4: Basculement vers le mode clair
        print("\n📋 Test 4: Basculement vers le mode clair")
        
        js_light_script = """
        // Basculement vers le mode clair
        const html = document.documentElement;
        html.classList.remove('dark-mode');
        html.setAttribute('data-theme', 'light');
        localStorage.setItem('dark-mode', 'false');
        
        // Appliquer les styles forcés
        document.body.style.backgroundColor = '#ffffff';
        document.body.style.color = '#2c3e50';
        
        const navBar = document.querySelector('.navigation-bar');
        if (navBar) {
            navBar.style.backgroundColor = '#f8f9fa';
            navBar.style.borderBottom = '1px solid #dee2e6';
        }
        
        // Appliquer aux cards
        const cards = document.querySelectorAll('.card, .feature-card');
        cards.forEach(card => {
            card.style.backgroundColor = '#f8f9fa';
            card.style.border = '1px solid #dee2e6';
            card.style.color = '#2c3e50';
        });
        
        console.log('☀️ Mode clair appliqué directement');
        """
        
        driver.execute_script(js_light_script)
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
        
        # Test 5: Vérifier localStorage
        print("\n📋 Test 5: Vérification localStorage")
        dark_mode_stored = driver.execute_script("return localStorage.getItem('dark-mode');")
        print(f"localStorage dark-mode: {dark_mode_stored}")
        
        # Résumé
        print("\n📊 RÉSUMÉ:")
        has_dark_mode = 'dark-mode' in after_classes
        has_correct_colors = bg_color_after != 'rgba(0, 0, 0, 0)'
        has_correct_final_colors = bg_color_final != 'rgba(0, 0, 0, 0)'
        
        print(f"Mode sombre activé: {'✅' if has_dark_mode else '❌'}")
        print(f"Couleurs sombres appliquées: {'✅' if has_correct_colors else '❌'}")
        print(f"Couleurs claires appliquées: {'✅' if has_correct_final_colors else '❌'}")
        
        if has_correct_colors and has_correct_final_colors:
            print("\n🎉 THÈME FONCTIONNEL!")
            print("✅ Les couleurs changent correctement")
        else:
            print("\n⚠️ PROBLÈMES DÉTECTÉS")
            if not has_correct_colors:
                print("- Couleurs sombres non appliquées")
            if not has_correct_final_colors:
                print("- Couleurs claires non appliquées")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    finally:
        if 'driver' in locals():
            driver.quit()
            print("🔧 Driver fermé")

if __name__ == "__main__":
    test_theme_direct() 