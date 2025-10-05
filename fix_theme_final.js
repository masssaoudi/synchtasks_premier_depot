// Script de correction finale du thème
// À copier-coller dans la console du navigateur sur http://localhost

console.log('🎨 === CORRECTION FINALE DU THÈME ===')

// Fonction pour appliquer le thème
function applyTheme() {
    const html = document.documentElement
    const isDark = html.classList.contains('dark-mode')
    const localStorageTheme = localStorage.getItem('dark-mode')
    
    console.log('Mode sombre actuel:', isDark)
    console.log('localStorage dark-mode:', localStorageTheme)
    
    if (localStorageTheme === 'true' || isDark) {
        console.log('🎨 Application du mode sombre...')
        html.classList.add('dark-mode')
        html.setAttribute('data-theme', 'dark')
        localStorage.setItem('dark-mode', 'true')
        
        document.body.style.backgroundColor = '#1a1a1a'
        document.body.style.color = '#ffffff'
        
        const navBar = document.querySelector('.navigation-bar')
        if (navBar) {
            navBar.style.backgroundColor = '#2d2d2d'
            navBar.style.borderBottom = '1px solid #404040'
        }
        
        console.log('✅ Mode sombre appliqué')
    } else {
        console.log('☀️ Application du mode clair...')
        html.classList.remove('dark-mode')
        html.setAttribute('data-theme', 'light')
        localStorage.setItem('dark-mode', 'false')
        
        document.body.style.backgroundColor = '#ffffff'
        document.body.style.color = '#2c3e50'
        
        const navBar = document.querySelector('.navigation-bar')
        if (navBar) {
            navBar.style.backgroundColor = '#f8f9fa'
            navBar.style.borderBottom = '1px solid #dee2e6'
        }
        
        console.log('✅ Mode clair appliqué')
    }
}

// Fonction pour corriger le bouton thème
function fixThemeButton() {
    console.log('🔧 Correction du bouton thème...')
    
    const themeButton = document.querySelector('.nav-btn-theme')
    if (!themeButton) {
        console.log('❌ Bouton thème non trouvé')
        return
    }
    
    console.log('✅ Bouton thème trouvé')
    
    const newButton = themeButton.cloneNode(true)
    themeButton.parentNode.replaceChild(newButton, themeButton)
    
    newButton.addEventListener('click', function(e) {
        e.preventDefault()
        e.stopPropagation()
        
        console.log('🔄 Clic sur le bouton thème corrigé...')
        
        const html = document.documentElement
        const isDark = html.classList.contains('dark-mode')
        
        if (isDark) {
            html.classList.remove('dark-mode')
            html.setAttribute('data-theme', 'light')
            localStorage.setItem('dark-mode', 'false')
            console.log('☀️ Passage en mode clair')
        } else {
            html.classList.add('dark-mode')
            html.setAttribute('data-theme', 'dark')
            localStorage.setItem('dark-mode', 'true')
            console.log('🎨 Passage en mode sombre')
        }
        
        applyTheme()
        
        setTimeout(() => {
            if (html.classList.contains('dark-mode')) {
                newButton.innerHTML = '☀️<br>Clair'
            } else {
                newButton.innerHTML = '🌙<br>Sombre'
            }
        }, 100)
    })
    
    console.log('✅ Bouton thème corrigé')
}

// Fonction pour forcer la connexion WebSocket
function forceWebSocketConnection() {
    console.log('🔌 Forçage de la connexion WebSocket...')
    
    const user = localStorage.getItem('user')
    if (user) {
        try {
            const userData = JSON.parse(user)
            const userId = userData._id || userData.id
            
            if (userId) {
                console.log('✅ User ID trouvé:', userId)
                
                // Créer une connexion WebSocket manuelle
                const wsUrl = 'ws://localhost:8000/ws'
                console.log('URL WebSocket:', wsUrl)
                
                try {
                    const ws = new WebSocket(wsUrl)
                    
                    ws.onopen = () => {
                        console.log('✅ WebSocket connecté')
                        
                        // Envoyer l'authentification
                        ws.send(JSON.stringify({ type: 'auth', user_id: userId }))
                        console.log('🔐 Authentification WebSocket envoyée')
                        
                        // Appliquer le thème après connexion
                        setTimeout(() => {
                            applyTheme()
                        }, 500)
                    }
                    
                    ws.onmessage = (event) => {
                        try {
                            const data = JSON.parse(event.data)
                            console.log('📨 Message WebSocket reçu:', data)
                        } catch (error) {
                            console.log('📨 Message brut reçu:', event.data)
                        }
                    }
                    
                    ws.onclose = (event) => {
                        console.log('🔌 WebSocket déconnecté:', event.code, event.reason)
                    }
                    
                    ws.onerror = (error) => {
                        console.error('❌ Erreur WebSocket:', error)
                    }
                    
                    // Stocker la connexion
                    window.manualWebSocket = ws
                    
                } catch (error) {
                    console.error('❌ Erreur création WebSocket:', error)
                }
            } else {
                console.log('❌ User ID non trouvé')
            }
        } catch (e) {
            console.error('❌ Erreur parsing user:', e)
        }
    } else {
        console.log('❌ Données utilisateur non trouvées')
    }
}

// Fonction principale de correction
function fixThemeFinal() {
    console.log('🚀 Lancement de la correction finale...')
    
    // 1. Forcer la connexion WebSocket
    forceWebSocketConnection()
    
    // 2. Appliquer le thème
    applyTheme()
    
    // 3. Corriger le bouton thème
    setTimeout(() => {
        fixThemeButton()
    }, 1000)
    
    console.log('✅ Correction finale appliquée')
}

// Exécuter la correction
fixThemeFinal()

// Fonctions disponibles globalement
window.applyTheme = applyTheme
window.fixThemeButton = fixThemeButton
window.forceWebSocketConnection = forceWebSocketConnection
window.fixThemeFinal = fixThemeFinal

console.log('\n📝 Fonctions disponibles:')
console.log('- applyTheme() : Appliquer le thème')
console.log('- fixThemeButton() : Corriger le bouton thème')
console.log('- forceWebSocketConnection() : Forcer la connexion WebSocket')
console.log('- fixThemeFinal() : Correction complète')

console.log('\n🎯 === CORRECTION FINALE TERMINÉE ===')
console.log('✅ Le thème devrait maintenant fonctionner parfaitement!')
console.log('🎨 Testez le bouton thème dans l\'interface') 