@echo off
echo 🎨 Lancement du test du mode sombre/clair...
echo.

echo 📋 Étape 1: Ouverture de l'application...
start http://localhost

echo.
echo 📋 Étape 2: Instructions pour le test...
echo.
echo 1. Attendez que l'application se charge
echo 2. Appuyez sur F12 pour ouvrir la console
echo 3. Copiez-collez le contenu de test_theme_real.js
echo 4. Appuyez sur Entree
echo.
echo 📋 Étape 3: Contenu du script à copier-coller:
echo.
type test_theme_real.js
echo.
echo 🎯 Test terminé! Vérifiez les résultats dans la console.
pause 