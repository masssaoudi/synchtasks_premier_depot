# 🧪 Guide de Tests et Diagnostic - SyncTasks

## 📋 Vue d'ensemble

Ce guide explique comment tester et diagnostiquer les problèmes de synchronisation et de logique de basculement dans l'application SyncTasks.

## 🚀 Démarrage rapide

### 1. Test automatique complet
```bash
python start_and_test.py
```
Ce script :
- Démarre automatiquement l'API
- Exécute tous les tests
- Génère un rapport complet
- Arrête l'API

### 2. Test manuel
```bash
# Démarrer l'API
python main.py

# Dans un autre terminal, exécuter les tests
python run_tests.py
```

## 📁 Structure des tests

```
tests/
├── test_main_integration.py    # Tests d'intégration complets
├── test_routes.py              # Tests des routes API
├── test_auth.py                # Tests d'authentification
├── test_ia_routes.py           # Tests des routes IA
└── conftest.py                 # Configuration pytest

diagnostic_sync.py              # Script de diagnostic
run_tests.py                    # Exécuteur de tests
start_and_test.py              # Démarrage + tests automatiques
pytest.ini                     # Configuration pytest
```

## 🔍 Tests disponibles

### 1. Tests d'intégration (`test_main_integration.py`)
- **Synchronisation des données** : Teste le flux complet CRUD
- **Navigation entre pages** : Vérifie la cohérence des filtres
- **Synchronisation temps réel** : Teste les WebSockets
- **Transitions de statut** : Vérifie les basculements
- **Opérations en lot** : Teste les suppressions multiples
- **Opérations concurrentes** : Vérifie la résistance
- **Gestion d'erreurs** : Teste la récupération
- **Cohérence des données** : Vérifie l'intégrité

### 2. Diagnostic de synchronisation (`diagnostic_sync.py`)
- **Connectivité API** : Vérifie l'accessibilité
- **Opérations CRUD** : Teste chaque opération
- **Flux de synchronisation** : Vérifie la cohérence
- **Logique de navigation** : Teste les filtres
- **Gestion d'erreurs** : Vérifie les cas d'erreur

## 🎯 Problèmes identifiés et solutions

### Problème 1: Synchronisation des données
**Symptômes** :
- Les modifications ne sont pas visibles immédiatement
- Incohérence entre les vues
- Données obsolètes affichées

**Solutions** :
1. Vérifier les WebSockets dans `ws_manager.py`
2. S'assurer que les broadcasts sont envoyés
3. Vérifier la logique de mise à jour côté client

### Problème 2: Logique de basculement
**Symptômes** :
- Les transitions de statut ne fonctionnent pas
- Incohérence entre `status` et `completed`
- Problèmes de navigation entre pages

**Solutions** :
1. Vérifier la logique dans `services.py`
2. S'assurer que les deux champs sont synchronisés
3. Tester les transitions manuellement

### Problème 3: Filtres et navigation
**Symptômes** :
- Les filtres ne fonctionnent pas correctement
- Navigation entre catégories problématique
- Statistiques incorrectes

**Solutions** :
1. Vérifier les paramètres de requête dans `routes.py`
2. Tester les filtres individuellement
3. Vérifier la logique de statistiques

## 🔧 Outils de diagnostic

### 1. Script de diagnostic
```bash
python diagnostic_sync.py
```
Génère un rapport détaillé des problèmes.

### 2. Tests unitaires
```bash
pytest tests/ -v
```
Exécute tous les tests avec détails.

### 3. Tests spécifiques
```bash
# Tests d'intégration uniquement
pytest tests/test_main_integration.py -v

# Tests de synchronisation uniquement
pytest tests/test_main_integration.py::test_task_synchronization_flow -v
```

## 📊 Interprétation des résultats

### Rapport de diagnostic
Le fichier `diagnostic_report.json` contient :
- **Connectivité** : Statut de l'API
- **CRUD** : Tests des opérations de base
- **Synchronisation** : Tests de cohérence
- **Navigation** : Tests de filtres
- **Erreurs** : Tests de gestion d'erreurs

### Rapport de tests
Le fichier `test_report.json` contient :
- **Résultats pytest** : Détails des tests unitaires
- **Résultats diagnostic** : Résultats du diagnostic
- **Résumé** : Vue d'ensemble des problèmes

## 🚨 Problèmes courants

### 1. API non accessible
**Solution** :
```bash
# Vérifier que le serveur est démarré
python main.py

# Vérifier les logs d'erreur
# Vérifier la configuration dans config.py
```

### 2. Base de données non accessible
**Solution** :
```bash
# Vérifier la connexion MongoDB
# Vérifier les variables d'environnement
# Tester la connexion manuellement
```

### 3. Tests qui échouent
**Solution** :
```bash
# Vérifier les dépendances
pip install pytest pytest-asyncio httpx aiohttp

# Vérifier la configuration
# Relancer les tests
```

## 🔄 Workflow de développement

### 1. Avant chaque commit
```bash
python start_and_test.py
```

### 2. Après modification du code
```bash
python diagnostic_sync.py
```

### 3. Pour tester une fonctionnalité spécifique
```bash
pytest tests/ -k "nom_du_test" -v
```

## 📈 Amélioration continue

### 1. Ajouter de nouveaux tests
1. Créer un fichier dans `tests/`
2. Suivre la convention de nommage
3. Ajouter des assertions claires
4. Documenter le test

### 2. Améliorer le diagnostic
1. Ajouter de nouveaux tests dans `diagnostic_sync.py`
2. Améliorer les messages d'erreur
3. Ajouter des métriques de performance

### 3. Automatiser les tests
1. Intégrer dans CI/CD
2. Ajouter des tests de régression
3. Configurer des alertes

## 📞 Support

En cas de problème :
1. Consulter les logs de l'API
2. Exécuter le diagnostic complet
3. Vérifier la configuration
4. Consulter la documentation

## 🔗 Ressources

- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [Documentation pytest](https://docs.pytest.org/)
- [Documentation MongoDB](https://docs.mongodb.com/)
- [Guide WebSockets](https://websockets.readthedocs.io/) 