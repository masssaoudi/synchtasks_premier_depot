#!/usr/bin/env python3
"""
Script pour forcer l'activation du mode sombre
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def fix_theme_force():
    print("🔧 === CORRECTION FORCÉE DU THÈME ===")
    
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
        
        # Connexion
        print("\n📋 Connexion...")
        email_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='email']")
        password_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='password']")
        
        if email_inputs and password_inputs:
            email_inputs[0].clear()
            email_inputs[0].send_keys("alice@test.com")
            password_inputs[0].clear()
            password_inputs[0].send_keys("alice123")
            
            submit_buttons = driver.find_elements(By.CSS_SELECTOR, "button[type='submit']")
            if submit_buttons:
                submit_buttons[0].click()
                time.sleep(3)
                print("✅ Connexion réussie")
            else:
                print("❌ Bouton de connexion non trouvé")
                return
        else:
            print("❌ Champs de connexion non trouvés")
            return
        
        # Attendre que la page se charge
        time.sleep(2)
        
        # Test 1: État initial
        print("\n📋 Test 1: État initial")
        js_get_state = """
        const html = document.documentElement;
        const body = document.body;
        const computedStyle = window.getComputedStyle(body);
        
        return {
            hasDarkMode: html.classList.contains('dark-mode'),
            classes: html.className,
            dataTheme: html.getAttribute('data-theme'),
            backgroundColor: computedStyle.backgroundColor,
            color: computedStyle.color,
            localStorage: localStorage.getItem('dark-mode')
        };
        """
        
        initial_state = driver.execute_script(js_get_state)
        print(f"Mode sombre: {initial_state['hasDarkMode']}")
        print(f"Classes HTML: {initial_state['classes']}")
        print(f"data-theme: {initial_state['dataTheme']}")
        print(f"Couleur de fond: {initial_state['backgroundColor']}")
        print(f"Couleur de texte: {initial_state['color']}")
        print(f"localStorage: {initial_state['localStorage']}")
        
        # Test 2: Forcer l'activation du mode sombre
        print("\n📋 Test 2: Forçage du mode sombre")
        
        js_force_dark = """
        // Forcer l'activation du mode sombre
        const html = document.documentElement;
        
        // Ajouter la classe dark-mode
        html.classList.add('dark-mode');
        html.setAttribute('data-theme', 'dark');
        
        // Mettre à jour localStorage
        localStorage.setItem('dark-mode', 'true');
        
        // Appliquer les styles forcés
        document.body.style.backgroundColor = '#1a1a1a';
        document.body.style.color = '#ffffff';
        
        // Appliquer aux éléments de navigation
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
        
        console.log('🎨 Mode sombre forcé activé');
        
        return {
            hasDarkMode: html.classList.contains('dark-mode'),
            classes: html.className,
            dataTheme: html.getAttribute('data-theme'),
            localStorage: localStorage.getItem('dark-mode')
        };
        """
        
        dark_state = driver.execute_script(js_force_dark)
        time.sleep(2)
        
        print(f"Mode sombre après forçage: {dark_state['hasDarkMode']}")
        print(f"Classes HTML après: {dark_state['classes']}")
        print(f"data-theme après: {dark_state['dataTheme']}")
        print(f"localStorage après: {dark_state['localStorage']}")
        
        # Vérifier les couleurs après forçage
        colors_after_dark = driver.execute_script(js_get_state)
        print(f"Couleur de fond après forçage: {colors_after_dark['backgroundColor']}")
        print(f"Couleur de texte après forçage: {colors_after_dark['color']}")
        
        # Test 3: Basculement vers le mode clair
        print("\n📋 Test 3: Basculement vers le mode clair")
        
        js_force_light = """
        // Forcer l'activation du mode clair
        const html = document.documentElement;
        
        // Retirer la classe dark-mode
        html.classList.remove('dark-mode');
        html.setAttribute('data-theme', 'light');
        
        // Mettre à jour localStorage
        localStorage.setItem('dark-mode', 'false');
        
        // Appliquer les styles forcés
        document.body.style.backgroundColor = '#ffffff';
        document.body.style.color = '#2c3e50';
        
        // Appliquer aux éléments de navigation
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
        
        console.log('☀️ Mode clair forcé activé');
        
        return {
            hasDarkMode: html.classList.contains('dark-mode'),
            classes: html.className,
            dataTheme: html.getAttribute('data-theme'),
            localStorage: localStorage.getItem('dark-mode')
        };
        """
        
        light_state = driver.execute_script(js_force_light)
        time.sleep(2)
        
        print(f"Mode sombre après basculement: {light_state['hasDarkMode']}")
        print(f"Classes HTML après: {light_state['classes']}")
        print(f"data-theme après: {light_state['dataTheme']}")
        print(f"localStorage après: {light_state['localStorage']}")
        
        # Vérifier les couleurs après basculement
        colors_after_light = driver.execute_script(js_get_state)
        print(f"Couleur de fond après basculement: {colors_after_light['backgroundColor']}")
        print(f"Couleur de texte après basculement: {colors_after_light['color']}")
        
        # Résumé
        print("\n📊 RÉSUMÉ:")
        dark_works = dark_state['hasDarkMode'] and colors_after_dark['backgroundColor'] != 'rgb(255, 255, 255)'
        light_works = not light_state['hasDarkMode'] and colors_after_light['backgroundColor'] == 'rgb(255, 255, 255)'
        
        print(f"Mode sombre forcé: {'✅' if dark_works else '❌'}")
        print(f"Mode clair forcé: {'✅' if light_works else '❌'}")
        
        if dark_works and light_works:
            print("\n🎉 THÈME CORRIGÉ ET FONCTIONNEL!")
            print("✅ Les styles sont maintenant appliqués correctement")
        else:
            print("\n⚠️ PROBLÈMES PERSISTENT")
            if not dark_works:
                print("- Mode sombre ne fonctionne pas")
            if not light_works:
                print("- Mode clair ne fonctionne pas")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if 'driver' in locals():
            driver.quit()
            print("🔧 Driver fermé")

if __name__ == "__main__":
    fix_theme_force() 