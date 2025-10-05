#!/usr/bin/env python3
"""
Test d'intégration du modal de thème
"""

import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_theme_modal_integration():
    print("🎨 === TEST D'INTÉGRATION DU MODAL DE THÈME ===")
    
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
        
        # Test 0: Explorer la page et se connecter
        print("\n📋 Test 0: Exploration de la page")
        try:
            # Aller directement à la page de connexion
            driver.get("http://localhost/login")
            time.sleep(3)
            
            print(f"📄 URL actuelle: {driver.current_url}")
            print(f"📄 Titre de la page: {driver.title}")
            
            # Lister tous les éléments de formulaire
            print("🔍 Éléments de formulaire trouvés:")
            inputs = driver.find_elements(By.CSS_SELECTOR, "input")
            for i, inp in enumerate(inputs):
                input_type = inp.get_attribute("type")
                input_name = inp.get_attribute("name")
                input_placeholder = inp.get_attribute("placeholder")
                print(f"  - Input {i+1}: type={input_type}, name={input_name}, placeholder={input_placeholder}")
            
            # Lister tous les boutons
            print("🔍 Boutons trouvés:")
            buttons = driver.find_elements(By.CSS_SELECTOR, "button")
            for i, btn in enumerate(buttons):
                btn_text = btn.text
                btn_type = btn.get_attribute("type")
                btn_class = btn.get_attribute("class")
                print(f"  - Bouton {i+1}: texte='{btn_text}', type={btn_type}, classe={btn_class}")
            
            # Essayer de se connecter avec les éléments trouvés
            if len(inputs) >= 2:
                email_input = inputs[0]  # Premier input
                password_input = inputs[1]  # Deuxième input
                
                email_input.send_keys("alice@test.com")
                password_input.send_keys("alice123")
                
                # Chercher un bouton de soumission
                submit_button = None
                for btn in buttons:
                    if btn.get_attribute("type") == "submit" or "connecter" in btn.text.lower() or "login" in btn.text.lower():
                        submit_button = btn
                        break
                
                if submit_button:
                    submit_button.click()
                    time.sleep(5)  # Attendre plus longtemps pour la redirection
                    print("✅ Tentative de connexion effectuée")
                    
                    # Gérer l'alerte si elle apparaît
                    try:
                        alert = driver.switch_to.alert
                        alert_text = alert.text
                        print(f"⚠️ Alerte détectée: {alert_text}")
                        alert.accept()
                        time.sleep(2)
                    except:
                        print("✅ Pas d'alerte détectée")
                    
                    # Vérifier si on a été redirigé
                    print(f"📄 URL après connexion: {driver.current_url}")
                    print(f"📄 Titre après connexion: {driver.title}")
                    
                    # Attendre que la page soit chargée
                    time.sleep(3)
                    
                else:
                    print("⚠️ Bouton de soumission non trouvé")
            else:
                print("⚠️ Pas assez d'inputs trouvés pour la connexion")
            
        except Exception as e:
            print(f"❌ Erreur lors de l'exploration: {e}")
            print("🔄 Continuons sans connexion...")
        
        # Test 1: Vérifier le bouton thème dans la navigation
        print("\n📋 Test 1: Vérification du bouton thème")
        try:
            # Attendre que la page soit chargée
            time.sleep(2)
            
            # Chercher le bouton thème avec différents sélecteurs
            theme_button = None
            selectors = [
                "nav-btn-theme",
                "btn-theme",
                "theme-btn",
                "nav-btn[title*='thème']",
                "button[title*='thème']",
                "button[title*='theme']"
            ]
            
            for selector in selectors:
                try:
                    if selector.startswith("nav-btn") or selector.startswith("btn-"):
                        theme_button = driver.find_element(By.CLASS_NAME, selector)
                    else:
                        theme_button = driver.find_element(By.CSS_SELECTOR, selector)
                    print(f"✅ Bouton thème trouvé avec le sélecteur: {selector}")
                    break
                except:
                    continue
            
            if not theme_button:
                # Chercher par texte
                try:
                    theme_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Thème') or contains(text(), 'Theme') or contains(text(), '🎨')]")
                    print("✅ Bouton thème trouvé par texte")
                except:
                    print("❌ Bouton thème non trouvé")
                    print("🔍 Éléments de navigation disponibles:")
                    nav_elements = driver.find_elements(By.CSS_SELECTOR, "nav button, .nav-btn, .btn")
                    for i, elem in enumerate(nav_elements[:5]):
                        try:
                            print(f"  - Élément {i+1}: {elem.text} (classe: {elem.get_attribute('class')})")
                        except:
                            print(f"  - Élément {i+1}: [texte non lisible]")
                    return
            
            print(f"Texte du bouton: {theme_button.text}")
            
        except Exception as e:
            print(f"❌ Erreur lors de la recherche du bouton thème: {e}")
            return
        
        # Test 2: Clic sur le bouton thème pour ouvrir le modal
        print("\n📋 Test 2: Ouverture du modal de thème")
        print("🔄 Clic sur le bouton thème...")
        theme_button.click()
        time.sleep(2)
        
        # Test 3: Vérifier que le modal s'ouvre
        print("\n📋 Test 3: Vérification du modal")
        time.sleep(3)  # Attendre plus longtemps pour l'ouverture du modal
        
        try:
            # Chercher le modal avec différents sélecteurs
            modal = None
            modal_selectors = [
                "theme-modal-overlay",
                "modal-overlay",
                "theme-modal",
                "modal",
                "[class*='modal']",
                "[class*='overlay']"
            ]
            
            for selector in modal_selectors:
                try:
                    if selector.startswith("["):
                        modal = driver.find_element(By.CSS_SELECTOR, selector)
                    else:
                        modal = driver.find_element(By.CLASS_NAME, selector)
                    print(f"✅ Modal trouvé avec le sélecteur: {selector}")
                    break
                except:
                    continue
            
            if not modal:
                print("❌ Modal non trouvé")
                print("🔍 Éléments visibles après clic sur le bouton thème:")
                visible_elements = driver.find_elements(By.CSS_SELECTOR, "div, modal, overlay")
                for i, elem in enumerate(visible_elements[:10]):
                    try:
                        elem_class = elem.get_attribute("class")
                        elem_style = elem.get_attribute("style")
                        if "modal" in elem_class or "overlay" in elem_class or "display: block" in elem_style:
                            print(f"  - Élément {i+1}: classe={elem_class}, style={elem_style}")
                    except:
                        pass
                return
            
            print("✅ Modal de thème ouvert")
            
            # Vérifier les options de thème
            theme_options = driver.find_elements(By.CLASS_NAME, "theme-option")
            print(f"✅ {len(theme_options)} options de thème trouvées")
            
            for i, option in enumerate(theme_options):
                theme_name = option.find_element(By.CLASS_NAME, "theme-name").text
                print(f"  - Option {i+1}: {theme_name}")
                
        except Exception as e:
            print(f"❌ Erreur lors de la vérification du modal: {e}")
            return
        
        # Test 4: Sélectionner le mode sombre
        print("\n📋 Test 4: Sélection du mode sombre")
        try:
            dark_option = driver.find_element(By.XPATH, "//div[contains(@class, 'theme-option') and .//span[contains(text(), 'Mode Sombre')]]")
            dark_option.click()
            time.sleep(1)
            print("✅ Mode sombre sélectionné")
        except Exception as e:
            print(f"❌ Erreur lors de la sélection du mode sombre: {e}")
        
        # Test 5: Appliquer le thème
        print("\n📋 Test 5: Application du thème")
        try:
            apply_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Appliquer')]")
            apply_button.click()
            time.sleep(2)
            print("✅ Bouton Appliquer cliqué")
        except Exception as e:
            print(f"❌ Erreur lors de l'application: {e}")
        
        # Test 6: Vérifier l'état du thème après application
        print("\n📋 Test 6: Vérification de l'état du thème")
        html_element = driver.find_element(By.TAG_NAME, "html")
        final_classes = html_element.get_attribute("class")
        final_data_theme = html_element.get_attribute("data-theme")
        
        print(f"Classes HTML finales: {final_classes}")
        print(f"data-theme final: {final_data_theme}")
        
        # Test 7: Vérifier les couleurs appliquées
        print("\n📋 Test 7: Vérification des couleurs")
        try:
            body_element = driver.find_element(By.TAG_NAME, "body")
            body_style = driver.execute_script("return getComputedStyle(arguments[0]);", body_element)
            
            bg_color = body_style.get('backgroundColor', 'N/A')
            text_color = body_style.get('color', 'N/A')
            
            print(f"Couleur de fond: {bg_color}")
            print(f"Couleur de texte: {text_color}")
        except Exception as e:
            print(f"⚠️ Erreur lors de la vérification des couleurs: {e}")
            bg_color = "N/A"
            text_color = "N/A"
        
        # Test 8: Vérifier localStorage
        print("\n📋 Test 8: Vérification localStorage")
        dark_mode_stored = driver.execute_script("return localStorage.getItem('dark-mode');")
        theme_preference_stored = driver.execute_script("return localStorage.getItem('theme-preference');")
        print(f"localStorage dark-mode: {dark_mode_stored}")
        print(f"localStorage theme-preference: {theme_preference_stored}")
        
        # Test 9: Test API backend
        print("\n📋 Test 9: Test de l'API backend")
        try:
            # Test de l'endpoint de thème
            response = requests.get("http://localhost:8000/api/theme/test-user")
            if response.status_code == 200:
                print("✅ API thème accessible")
                print(f"Réponse API: {response.json()}")
            else:
                print(f"⚠️ API thème retourne {response.status_code}")
        except Exception as e:
            print(f"❌ Erreur API thème: {e}")
        
        # Résumé
        print("\n📊 RÉSUMÉ:")
        has_dark_mode = 'dark-mode' in final_classes or final_data_theme == 'dark'
        has_correct_colors = bg_color != 'rgba(0, 0, 0, 0)'
        modal_works = len(theme_options) > 0
        
        print(f"Modal fonctionnel: {'✅' if modal_works else '❌'}")
        print(f"Mode sombre activé: {'✅' if has_dark_mode else '❌'}")
        print(f"Couleurs appliquées: {'✅' if has_correct_colors else '❌'}")
        
        if modal_works and has_dark_mode and has_correct_colors:
            print("\n🎉 INTÉGRATION DU MODAL DE THÈME RÉUSSIE!")
        else:
            print("\n⚠️ PROBLÈMES DÉTECTÉS")
            if not modal_works:
                print("- Modal non fonctionnel")
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
    test_theme_modal_integration() 