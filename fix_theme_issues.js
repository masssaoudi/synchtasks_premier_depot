// Script de correction automatique pour les problèmes de thème
// À copier-coller dans la console du navigateur sur http://localhost

console.log('🔧 === CORRECTION AUTOMATIQUE THÈME ===')

// Fonction pour forcer l'application des variables CSS
function forceApplyTheme() {
    console.log('🔄 Forçage de l\'application du thème...')
    
    const html = document.documentElement
    const isDark = html.classList.contains('dark-mode')
    
    // Forcer l'application des variables CSS
    if (isDark) {
        html.style.setProperty('--bg-primary', '#1a1a1a')
        html.style.setProperty('--bg-secondary', '#2d2d2d')
        html.style.setProperty('--text-primary', '#ffffff')
        html.style.setProperty('--text-secondary', '#b0b0b0')
        html.style.setProperty('--border-color', '#404040')
        console.log('✅ Variables CSS mode sombre appliquées')
    } else {
        html.style.setProperty('--bg-primary', '#ffffff')
        html.style.setProperty('--bg-secondary', '#f8f9fa')
        html.style.setProperty('--text-primary', '#2c3e50')
        html.style.setProperty('--text-secondary', '#6c757d')
        html.style.setProperty('--border-color', '#dee2e6')
        console.log('✅ Variables CSS mode clair appliquées')
    }
}

// Fonction pour forcer le basculement du thème
function forceToggleTheme() {
    console.log('🔄 Forçage du basculement du thème...')
    
    const html = document.documentElement
    const isDark = html.classList.contains('dark-mode')
    
    if (isDark) {
        html.classList.remove('dark-mode')
        html.setAttribute('data-theme', 'light')
        localStorage.setItem('dark-mode', 'false')
        console.log('✅ Passage forcé en mode clair')
    } else {
        html.classList.add('dark-mode')
        html.setAttribute('data-theme', 'dark')
        localStorage.setItem('dark-mode', 'true')
        console.log('✅ Passage forcé en mode sombre')
    }
    
    // Appliquer les variables CSS
    forceApplyTheme()
}

// Fonction pour réinitialiser le thème
function resetTheme() {
    console.log('🔄 Réinitialisation du thème...')
    
    const html = document.documentElement
    
    // Nettoyer les classes et attributs
    html.classList.remove('dark-mode')
    html.removeAttribute('data-theme')
    
    // Nettoyer le localStorage
    localStorage.removeItem('dark-mode')
    localStorage.removeItem('theme-preference')
    
    // Réappliquer les variables par défaut
    html.style.setProperty('--bg-primary', '#ffffff')
    html.style.setProperty('--bg-secondary', '#f8f9fa')
    html.style.setProperty('--text-primary', '#2c3e50')
    html.style.setProperty('--text-secondary', '#6c757d')
    html.style.setProperty('--border-color', '#dee2e6')
    
    console.log('✅ Thème réinitialisé')
}

// Fonction pour forcer le rechargement des styles
function reloadStyles() {
    console.log('🔄 Rechargement des styles...')
    
    // Forcer le rechargement de la page
    console.log('⚠️ Rechargement de la page dans 2 secondes...')
    setTimeout(() => {
        window.location.reload()
    }, 2000)
}

// Fonction pour diagnostiquer et corriger automatiquement
function autoFix() {
    console.log('🔧 Diagnostic et correction automatique...')
    
    const html = document.documentElement
    const themeButton = document.querySelector('.nav-btn-theme')
    const app = document.querySelector('#app')
    
    let issues = []
    
    // Vérifier le bouton thème
    if (!themeButton) {
        issues.push('Bouton thème manquant')
        console.log('❌ Bouton thème non trouvé')
    } else {
        console.log('✅ Bouton thème trouvé')
    }
    
    // Vérifier l'application Vue
    if (!app || !app.__vue_app__) {
        issues.push('Application Vue non fonctionnelle')
        console.log('❌ Application Vue non trouvée')
    } else {
        console.log('✅ Application Vue trouvée')
    }
    
    // Vérifier les variables CSS
    const computedStyle = getComputedStyle(html)
    const bgPrimary = computedStyle.getPropertyValue('--bg-primary')
    if (!bgPrimary || bgPrimary.trim() === '') {
        issues.push('Variables CSS manquantes')
        console.log('❌ Variables CSS manquantes')
        forceApplyTheme()
    } else {
        console.log('✅ Variables CSS trouvées')
    }
    
    // Vérifier le localStorage
    const darkMode = localStorage.getItem('dark-mode')
    if (darkMode === null) {
        issues.push('localStorage non initialisé')
        console.log('❌ localStorage non initialisé')
        localStorage.setItem('dark-mode', 'false')
        console.log('✅ localStorage initialisé')
    } else {
        console.log('✅ localStorage OK')
    }
    
    // Appliquer les corrections
    if (issues.length > 0) {
        console.log('\n🔧 Application des corrections...')
        
        // Forcer l'application des variables CSS
        forceApplyTheme()
        
        // Forcer l'application du thème actuel
        const isDark = html.classList.contains('dark-mode')
        if (isDark) {
            html.setAttribute('data-theme', 'dark')
        } else {
            html.setAttribute('data-theme', 'light')
        }
        
        console.log('✅ Corrections appliquées')
    } else {
        console.log('✅ Aucun problème détecté')
    }
    
    return issues
}

// Fonctions disponibles globalement
window.forceApplyTheme = forceApplyTheme
window.forceToggleTheme = forceToggleTheme
window.resetTheme = resetTheme
window.reloadStyles = reloadStyles
window.autoFix = autoFix

// Exécuter la correction automatique
console.log('\n🚀 Lancement de la correction automatique...')
const issues = autoFix()

console.log('\n📊 Résumé des corrections:')
if (issues.length === 0) {
    console.log('✅ Aucun problème détecté - Thème fonctionnel')
} else {
    console.log(`⚠️ ${issues.length} problème(s) détecté(s):`)
    issues.forEach(issue => console.log(`- ${issue}`))
    console.log('\n🔧 Corrections appliquées')
}

console.log('\n📝 Fonctions disponibles:')
console.log('- forceApplyTheme() : Forcer l\'application des variables CSS')
console.log('- forceToggleTheme() : Forcer le basculement du thème')
console.log('- resetTheme() : Réinitialiser le thème')
console.log('- reloadStyles() : Recharger les styles')
console.log('- autoFix() : Diagnostic et correction automatique')

console.log('\n🎯 === CORRECTION TERMINÉE ===') 