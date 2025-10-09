# 🚀 GitHub Actions Workflows

Ce dossier contient les workflows CI/CD pour automatiser la validation ATS et la publication des releases.

## 📋 Workflows Disponibles

### 1. 🤖 ATS Validation (`ats-validation.yml`)

**Déclencheur** : Push/PR sur `main`

**Objectif** : Vérifier que le CV reste conforme ATS à chaque modification

**Étapes** :
- ✅ Installation de l'environnement (Python + LaTeX)
- ✅ Installation des dépendances ATS
- ✅ Build du CV en PDF
- ✅ Validation ATS complète
- ✅ Tests automatisés
- ✅ Upload des artefacts (PDF + rapport)

**Résultat** : ❌ Bloque le merge si la validation ATS échoue

### 2. 🚀 Release CV (`release.yml`)

**Déclencheur** : Push d'un tag `v*` (ex: `v1.0.0`)

**Objectif** : Générer et publier automatiquement le CV dans une release GitHub

**Étapes** :
- ✅ Build de tous les formats (PDF, HTML, JSON)
- ✅ Validation ATS
- ✅ Génération du rapport ATS
- ✅ Création de la release GitHub
- ✅ Upload de tous les fichiers versionnés

**Fichiers publiés** :
- `Mathéo_Champagne_CV_v1.0.0.pdf`
- `resume_v1.0.0.html`
- `resume_v1.0.0.json`
- `ats-report_v1.0.0.json`
- `resume_complete_v1.0.0.zip` (archive complète)

### 3. 🧪 Tests (`test.yml`)

**Déclencheur** : Push/PR sur `main` ou `develop`

**Objectif** : Tests complets sur plusieurs environnements

**Matrix** :
- OS : Ubuntu, macOS
- Python : 3.9, 3.10, 3.11, 3.12
- Tests : Unit, Integration, Quality

**Qualité** :
- ✅ Formatage (Black)
- ✅ Linting (Ruff)
- ✅ Type checking (MyPy)
- ✅ Coverage (Codecov)

## 🎯 Utilisation

### Pour déclencher une validation ATS :
```bash
git push origin main
# ou créer une PR vers main
```

### Pour créer une release :
```bash
# Créer et pousser un tag
git tag v1.0.0
git push origin v1.0.0
```

### Formats de tags supportés :
- `v1.0.0` ✅
- `v2.1.3` ✅
- `v1.0.0-beta.1` ✅

## 📊 Status Badges

Ajoutez ces badges dans votre README :

```markdown
[![ATS Validation](https://github.com/username/resume/actions/workflows/ats-validation.yml/badge.svg)](https://github.com/username/resume/actions/workflows/ats-validation.yml)
[![Tests](https://github.com/username/resume/actions/workflows/test.yml/badge.svg)](https://github.com/username/resume/actions/workflows/test.yml)
[![Release](https://github.com/username/resume/actions/workflows/release.yml/badge.svg)](https://github.com/username/resume/actions/workflows/release.yml)
```

## 🔧 Configuration

### Secrets requis :
- `GITHUB_TOKEN` (fourni automatiquement)

### Permissions :
- `contents: write` (pour créer les releases)

### Cache :
- Cache pip activé pour accélération des builds
- Cache LaTeX sur macOS (TinyTeX)

## 🚨 Troubleshooting

**Build échoue** : Vérifiez les logs d'installation LaTeX
**Tests échouent** : Vérifiez que resume.yml est valide
**Release échoue** : Vérifiez les permissions du token GitHub

Les workflows sont conçus pour être robustes et informatifs en cas d'erreur. 