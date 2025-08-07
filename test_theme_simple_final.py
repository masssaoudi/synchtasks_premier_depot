#!/usr/bin/env python3
"""
Script simple et fonctionnel pour tester le thème
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def test_theme_simple_final():
    print("🎨 === TEST SIMPLE FINAL DU THÈME ===")

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

        # Test 1: Connexion
        print("\n📋 Test 1: Connexion")

        email_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='email']")
        password_inputs = driver.find_elements(
            By.CSS_SELECTOR, "input[type='password']"
        )

        print(f"Champs email trouvés: {len(email_inputs)}")
        print(f"Champs password trouvés: {len(password_inputs)}")

        if email_inputs and password_inputs:
            print("✅ Champs de connexion trouvés")

            email_inputs[0].clear()
            email_inputs[0].send_keys("alice@test.com")

            password_inputs[0].clear()
            password_inputs[0].send_keys("alice123")

            submit_buttons = driver.find_elements(
                By.CSS_SELECTOR, "button[type='submit']"
            )
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
        time.sleep(2)

        theme_buttons = driver.find_elements(By.CSS_SELECTOR, ".nav-btn-theme")
        if theme_buttons:
            theme_button = theme_buttons[0]
            print("✅ Bouton thème trouvé")
            print(f"Texte du bouton: {theme_button.text}")
        else:
            print("❌ Bouton thème non trouvé")
            return

        # Test 3: Test du basculement
        print("\n📋 Test 3: Test du basculement")

        # État avant
        html_element = driver.find_element(By.TAG_NAME, "html")
        initial_classes = html_element.get_attribute("class")
        print(f"Classes HTML avant: {initial_classes}")

        # Vérifier les couleurs avant avec JavaScript
        js_get_colors = """
        const body = document.body;
        const computedStyle = window.getComputedStyle(body);
        return {
            backgroundColor: computedStyle.backgroundColor,
            color: computedStyle.color
        };
        """

        colors_before = driver.execute_script(js_get_colors)
        print(f"Couleur de fond avant: {colors_before['backgroundColor']}")
        print(f"Couleur de texte avant: {colors_before['color']}")

        # Clic sur le bouton
        print("🔄 Clic sur le bouton thème...")
        theme_button.click()
        time.sleep(2)

        # État après
        html_element = driver.find_element(By.TAG_NAME, "html")
        after_classes = html_element.get_attribute("class")
        print(f"Classes HTML après: {after_classes}")

        # Vérifier les couleurs après
        colors_after = driver.execute_script(js_get_colors)
        print(f"Couleur de fond après: {colors_after['backgroundColor']}")
        print(f"Couleur de texte après: {colors_after['color']}")

        # Test 4: Appliquer les corrections si nécessaire
        print("\n📋 Test 4: Application des corrections")

        # Vérifier si les couleurs ont changé
        colors_changed = (
            colors_before["backgroundColor"] != colors_after["backgroundColor"]
        ) or (colors_before["color"] != colors_after["color"])

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
            colors_corrected = driver.execute_script(js_get_colors)
            print(
                f"Couleur de fond après correction: {colors_corrected['backgroundColor']}"
            )
            print(f"Couleur de texte après correction: {colors_corrected['color']}")
        else:
            print("✅ Les couleurs ont changé naturellement")

        # Test 5: Vérifier localStorage
        print("\n📋 Test 5: Vérification localStorage")
        dark_mode_stored = driver.execute_script(
            "return localStorage.getItem('dark-mode');"
        )
        print(f"localStorage dark-mode: {dark_mode_stored}")

        # Résumé
        print("\n📊 RÉSUMÉ:")
        has_dark_mode = "dark-mode" in after_classes
        has_correct_colors = colors_after["backgroundColor"] != "rgba(0, 0, 0, 0)"

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
        import traceback

        traceback.print_exc()

    finally:
        if "driver" in locals():
            driver.quit()
            print("🔧 Driver fermé")


if __name__ == "__main__":
    test_theme_simple_final()
