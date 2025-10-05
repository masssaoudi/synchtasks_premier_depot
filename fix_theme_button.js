// Script pour corriger le bouton thème
// À copier-coller dans la console du navigateur sur http://localhost

console.log('🔧 === CORRECTION DU BOUTON THÈME ===')

// Fonction pour appliquer les styles du thème
function applyThemeStyles() {
    const html = document.documentElement;
    const isDark = html.classList.contains('dark-mode');
    
    if (isDark) {
        console.log('🎨 Application du mode sombre...');
        
        // Appliquer les styles forcés
        document.body.style.backgroundColor = '#1a1a1a';
        document.body.style.color = '#ffffff';
        
        // Navigation bar
        const navBar = document.querySelector('.navigation-bar');
        if (navBar) {
            navBar.style.backgroundColor = '#2d2d2d';
            navBar.style.borderBottom = '1px solid #404040';
        }
        
        // Cards
        const cards = document.querySelectorAll('.card, .feature-card');
        cards.forEach(card => {
            card.style.backgroundColor = '#2d2d2d';
            card.style.border = '1px solid #404040';
            card.style.color = '#ffffff';
        });
        
        console.log('✅ Styles mode sombre appliqués');
    } else {
        console.log('☀️ Application du mode clair...');
        
        // Appliquer les styles forcés
        document.body.style.backgroundColor = '#ffffff';
        document.body.style.color = '#2c3e50';
        
        // Navigation bar
        const navBar = document.querySelector('.navigation-bar');
        if (navBar) {
            navBar.style.backgroundColor = '#f8f9fa';
            navBar.style.borderBottom = '1px solid #dee2e6';
        }
        
        // Cards
        const cards = document.querySelectorAll('.card, .feature-card');
        cards.forEach(card => {
            card.style.backgroundColor = '#f8f9fa';
            card.style.border = '1px solid #dee2e6';
            card.style.color = '#2c3e50';
        });
        
        console.log('✅ Styles mode clair appliqués');
    }
}

// Fonction pour corriger le bouton thème
function fixThemeButton() {
    console.log('🔧 Correction du bouton thème...');
    
    // Chercher le bouton thème
    const themeButton = document.querySelector('.nav-btn-theme');
    if (!themeButton) {
        console.log('❌ Bouton thème non trouvé');
        return;
    }
    
    console.log('✅ Bouton thème trouvé');
    
    // Supprimer l'ancien event listener
    const newButton = themeButton.cloneNode(true);
    themeButton.parentNode.replaceChild(newButton, themeButton);
    
    // Ajouter le nouvel event listener
    newButton.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        console.log('🔄 Clic sur le bouton thème corrigé...');
        
        const html = document.documentElement;
        const isDark = html.classList.contains('dark-mode');
        
        if (isDark) {
            // Passer en mode clair
            html.classList.remove('dark-mode');
            html.setAttribute('data-theme', 'light');
            localStorage.setItem('dark-mode', 'false');
            console.log('☀️ Passage en mode clair');
        } else {
            // Passer en mode sombre
            html.classList.add('dark-mode');
            html.setAttribute('data-theme', 'dark');
            localStorage.setItem('dark-mode', 'true');
            console.log('🎨 Passage en mode sombre');
        }
        
        // Appliquer les styles immédiatement
        applyThemeStyles();
        
        // Mettre à jour le texte du bouton
        setTimeout(() => {
            if (html.classList.contains('dark-mode')) {
                newButton.innerHTML = '☀️<br>Clair';
            } else {
                newButton.innerHTML = '🌙<br>Sombre';
            }
        }, 100);
    });
    
    console.log('✅ Bouton thème corrigé');
}

// Fonction pour forcer l'application des styles actuels
function forceApplyCurrentTheme() {
    console.log('🔄 Application forcée du thème actuel...');
    applyThemeStyles();
}

// Exécuter la correction
console.log('🚀 Lancement de la correction...');
fixThemeButton();
forceApplyCurrentTheme();

// Fonctions disponibles globalement
window.applyThemeStyles = applyThemeStyles;
window.fixThemeButton = fixThemeButton;
window.forceApplyCurrentTheme = forceApplyCurrentTheme;

console.log('\n📝 Fonctions disponibles:')
console.log('- applyThemeStyles() : Appliquer les styles du thème')
console.log('- fixThemeButton() : Corriger le bouton thème')
console.log('- forceApplyCurrentTheme() : Forcer l\'application du thème actuel')

console.log('\n🎯 === CORRECTION TERMINÉE ===')
console.log('✅ Le bouton thème devrait maintenant fonctionner correctement!') 