#!/usr/bin/env python3
"""
Script de test automatisé pour le mode sombre/clair
Teste l'application via Selenium WebDriver
"""

import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class ThemeTester:
    def __init__(self, base_url="http://localhost"):  # Changé de 8080 à 80
        self.base_url = base_url
        self.driver = None
        self.results = {
            "tests": [],
            "errors": [],
            "summary": {}
        }
    
    def setup_driver(self):
        """Configure le driver Chrome"""
        print("🔧 Configuration du driver Chrome...")
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Mode sans interface
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-web-security")  # Pour éviter les problèmes CORS
        chrome_options.add_argument("--allow-running-insecure-content")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            print("✅ Driver Chrome configuré")
            return True
        except Exception as e:
            print(f"❌ Erreur configuration driver: {e}")
            return False
    
    def test_application_accessible(self):
        """Test si l'application est accessible"""
        print("\n📋 Test 1: Accessibilité de l'application")
        
        try:
            self.driver.get(self.base_url)
            time.sleep(2)
            
            # Vérifier que la page se charge
            title = self.driver.title
            print(f"✅ Page chargée - Titre: {title}")
            
            # Vérifier la présence d'éléments de base
            app_element = self.driver.find_element(By.ID, "app")
            print("✅ Élément #app trouvé")
            
            self.results["tests"].append({
                "name": "Application accessible",
                "status": "PASS",
                "details": f"Titre: {title}"
            })
            return True
            
        except Exception as e:
            print(f"❌ Erreur accès application: {e}")
            self.results["tests"].append({
                "name": "Application accessible",
                "status": "FAIL",
                "details": str(e)
            })
            return False
    
    def test_theme_button_present(self):
        """Test si le bouton de thème est présent"""
        print("\n📋 Test 2: Présence du bouton thème")
        
        try:
            # Chercher le bouton thème
            theme_button = self.driver.find_element(By.CLASS_NAME, "nav-btn-theme")
            print("✅ Bouton thème trouvé")
            
            # Vérifier le texte et l'icône
            button_text = theme_button.text
            print(f"✅ Texte du bouton: {button_text}")
            
            self.results["tests"].append({
                "name": "Bouton thème présent",
                "status": "PASS",
                "details": f"Texte: {button_text}"
            })
            return True
            
        except NoSuchElementException:
            print("❌ Bouton thème non trouvé")
            self.results["tests"].append({
                "name": "Bouton thème présent",
                "status": "FAIL",
                "details": "Bouton .nav-btn-theme non trouvé"
            })
            return False
        except Exception as e:
            print(f"❌ Erreur recherche bouton: {e}")
            self.results["tests"].append({
                "name": "Bouton thème présent",
                "status": "FAIL",
                "details": str(e)
            })
            return False
    
    def test_initial_theme_state(self):
        """Test l'état initial du thème"""
        print("\n📋 Test 3: État initial du thème")
        
        try:
            html_element = self.driver.find_element(By.TAG_NAME, "html")
            
            # Vérifier les classes
            classes = html_element.get_attribute("class")
            data_theme = html_element.get_attribute("data-theme")
            
            print(f"✅ Classes HTML: {classes}")
            print(f"✅ data-theme: {data_theme}")
            
            # Vérifier le localStorage via JavaScript
            dark_mode_stored = self.driver.execute_script(
                "return localStorage.getItem('dark-mode')"
            )
            theme_preference = self.driver.execute_script(
                "return localStorage.getItem('theme-preference')"
            )
            
            print(f"✅ localStorage dark-mode: {dark_mode_stored}")
            print(f"✅ localStorage theme-preference: {theme_preference}")
            
            self.results["tests"].append({
                "name": "État initial thème",
                "status": "PASS",
                "details": {
                    "classes": classes,
                    "data_theme": data_theme,
                    "localStorage": {
                        "dark_mode": dark_mode_stored,
                        "preference": theme_preference
                    }
                }
            })
            return True
            
        except Exception as e:
            print(f"❌ Erreur vérification état initial: {e}")
            self.results["tests"].append({
                "name": "État initial thème",
                "status": "FAIL",
                "details": str(e)
            })
            return False
    
    def test_theme_toggle(self):
        """Test le basculement du thème"""
        print("\n📋 Test 4: Basculement du thème")
        
        try:
            # État avant
            html_before = self.driver.find_element(By.TAG_NAME, "html")
            classes_before = html_before.get_attribute("class")
            data_theme_before = html_before.get_attribute("data-theme")
            dark_mode_before = self.driver.execute_script(
                "return localStorage.getItem('dark-mode')"
            )
            
            print(f"📊 État avant:")
            print(f"  - Classes: {classes_before}")
            print(f"  - data-theme: {data_theme_before}")
            print(f"  - localStorage: {dark_mode_before}")
            
            # Cliquer sur le bouton thème
            theme_button = self.driver.find_element(By.CLASS_NAME, "nav-btn-theme")
            theme_button.click()
            
            # Attendre un peu pour que le changement s'applique
            time.sleep(1)
            
            # État après
            html_after = self.driver.find_element(By.TAG_NAME, "html")
            classes_after = html_after.get_attribute("class")
            data_theme_after = html_after.get_attribute("data-theme")
            dark_mode_after = self.driver.execute_script(
                "return localStorage.getItem('dark-mode')"
            )
            
            print(f"📊 État après:")
            print(f"  - Classes: {classes_after}")
            print(f"  - data-theme: {data_theme_after}")
            print(f"  - localStorage: {dark_mode_after}")
            
            # Vérifier si un changement a eu lieu
            has_changed = (
                classes_before != classes_after or
                data_theme_before != data_theme_after or
                dark_mode_before != dark_mode_after
            )
            
            if has_changed:
                print("✅ Changement détecté lors du basculement")
                self.results["tests"].append({
                    "name": "Basculement thème",
                    "status": "PASS",
                    "details": {
                        "before": {
                            "classes": classes_before,
                            "data_theme": data_theme_before,
                            "localStorage": dark_mode_before
                        },
                        "after": {
                            "classes": classes_after,
                            "data_theme": data_theme_after,
                            "localStorage": dark_mode_after
                        }
                    }
                })
            else:
                print("❌ Aucun changement détecté")
                self.results["tests"].append({
                    "name": "Basculement thème",
                    "status": "FAIL",
                    "details": "Aucun changement détecté lors du clic"
                })
            
            return has_changed
            
        except Exception as e:
            print(f"❌ Erreur test basculement: {e}")
            self.results["tests"].append({
                "name": "Basculement thème",
                "status": "FAIL",
                "details": str(e)
            })
            return False
    
    def test_css_variables(self):
        """Test les variables CSS"""
        print("\n📋 Test 5: Variables CSS")
        
        try:
            # Exécuter le script de diagnostic JavaScript
            js_script = """
            const html = document.documentElement;
            const computedStyle = getComputedStyle(html);
            return {
                bgPrimary: computedStyle.getPropertyValue('--bg-primary'),
                textPrimary: computedStyle.getPropertyValue('--text-primary'),
                borderColor: computedStyle.getPropertyValue('--border-color'),
                backgroundColor: computedStyle.backgroundColor,
                color: computedStyle.color
            };
            """
            
            css_vars = self.driver.execute_script(js_script)
            
            print("✅ Variables CSS récupérées:")
            for key, value in css_vars.items():
                print(f"  - {key}: {value}")
            
            self.results["tests"].append({
                "name": "Variables CSS",
                "status": "PASS",
                "details": css_vars
            })
            return True
            
        except Exception as e:
            print(f"❌ Erreur variables CSS: {e}")
            self.results["tests"].append({
                "name": "Variables CSS",
                "status": "FAIL",
                "details": str(e)
            })
            return False
    
    def test_console_errors(self):
        """Test les erreurs dans la console"""
        print("\n📋 Test 6: Erreurs console")
        
        try:
            # Récupérer les logs de la console
            logs = self.driver.get_log('browser')
            errors = [log for log in logs if log['level'] == 'SEVERE']
            
            if errors:
                print(f"⚠️ {len(errors)} erreurs trouvées:")
                for error in errors:
                    print(f"  - {error['message']}")
                
                self.results["tests"].append({
                    "name": "Erreurs console",
                    "status": "WARN",
                    "details": errors
                })
            else:
                print("✅ Aucune erreur console détectée")
                self.results["tests"].append({
                    "name": "Erreurs console",
                    "status": "PASS",
                    "details": "Aucune erreur"
                })
            
            return len(errors) == 0
            
        except Exception as e:
            print(f"❌ Erreur vérification console: {e}")
            self.results["tests"].append({
                "name": "Erreurs console",
                "status": "FAIL",
                "details": str(e)
            })
            return False
    
    def run_all_tests(self):
        """Exécute tous les tests"""
        print("🚀 === DÉBUT DES TESTS THÈME ===")
        
        if not self.setup_driver():
            return False
        
        try:
            # Tests séquentiels
            tests = [
                self.test_application_accessible,
                self.test_theme_button_present,
                self.test_initial_theme_state,
                self.test_theme_toggle,
                self.test_css_variables,
                self.test_console_errors
            ]
            
            passed = 0
            total = len(tests)
            
            for test in tests:
                if test():
                    passed += 1
            
            # Résumé
            self.results["summary"] = {
                "total": total,
                "passed": passed,
                "failed": total - passed,
                "success_rate": (passed / total) * 100 if total > 0 else 0
            }
            
            print(f"\n📊 RÉSUMÉ: {passed}/{total} tests réussis ({self.results['summary']['success_rate']:.1f}%)")
            
            if passed == total:
                print("🎉 TOUS LES TESTS RÉUSSIS!")
            else:
                print("⚠️ Certains tests ont échoué")
            
            return passed == total
            
        finally:
            if self.driver:
                self.driver.quit()
                print("🔧 Driver fermé")
    
    def save_results(self, filename="theme_test_results.json"):
        """Sauvegarde les résultats"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
            print(f"💾 Résultats sauvegardés dans {filename}")
        except Exception as e:
            print(f"❌ Erreur sauvegarde: {e}")

def main():
    """Fonction principale"""
    print("🎨 Test automatisé du mode sombre/clair")
    print("=" * 50)
    
    # Configuration
    base_url = "http://localhost:8080"  # URL de l'application
    
    # Créer et exécuter les tests
    tester = ThemeTester(base_url)
    success = tester.run_all_tests()
    
    # Sauvegarder les résultats
    tester.save_results()
    
    # Code de sortie
    exit_code = 0 if success else 1
    print(f"\n🏁 Code de sortie: {exit_code}")
    return exit_code

if __name__ == "__main__":
    main() 