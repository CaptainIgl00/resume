# Tests ATS-friendly

Ce document décrit le système de tests automatisés **pytest** pour vérifier que le CV généré est compatible avec les **Applicant Tracking Systems (ATS)** et correspond fidèlement aux données source `resume.yml`.

## 🎯 Objectifs des tests

Les tests ATS valident **automatiquement** :

1. **Extraction de texte** : Vérification que le PDF peut être lu par les outils de parsing standard
2. **Parsing des données** : Extraction et validation des informations clés (nom, email, compétences)
3. **Correspondance avec la source** : Comparaison avec les données de `resume.yml`
4. **Complétude des informations** : Validation que tous les champs essentiels sont présents

## 🚀 Utilisation rapide

```bash
# Générer le CV et tester sa compatibilité ATS
make build-and-test

# Ou tester uniquement (si le CV est déjà généré)
make test-ats

# Installer les dépendances ATS (première fois)
make setup-ats
```

## 📋 Tests effectués (pytest)

### Tests individuels avec pytest

```bash
# Test d'extraction du nom complet
pytest tests/test_ats_compatibility.py::TestATSCompatibility::test_name_extraction -v

# Test des compétences techniques
pytest tests/test_ats_compatibility.py::TestATSCompatibility::test_skills_extraction -v

# Test de complétude globale
pytest tests/test_ats_compatibility.py::TestATSCompatibility::test_data_completeness -v -s
```

### Validation automatique

| Test | Description | Critère de réussite |
|------|-------------|---------------------|
| **PDF exists** | Vérifie la présence du PDF | Fichier `build/Mathéo_Guilloux_CV.pdf` existe |
| **Text extraction** | Extraction de texte robuste | Texte > 100 caractères + "DevOps" trouvé |
| **Name extraction** | Nom complet vs `resume.yml` | "Mathéo Guilloux" extrait correctement |
| **Email extraction** | Email exact vs `resume.yml` | `matheo.guilloux@gmail.com` trouvé |
| **Position extraction** | Poste vs `resume.yml` | "DevOps Engineer" détecté |
| **Skills extraction** | Compétences vs `resume.yml` | ≥ 10 compétences + 70% de couverture |
| **Companies extraction** | Entreprises principales | Continental, Neverhack, Airbus détectées |
| **Data completeness** | Test global de complétude | Tous les champs essentiels présents |

## 🔧 Architecture technique

### CVExtractor (classe principale)

```python
class CVExtractor:
    def __init__(self, pdf_path: str)           # Initialise avec pdfplumber
    def extract_name(self) -> str               # Regex intelligent pour nom complet
    def extract_email(self) -> str              # Extraction email fiable
    def extract_position(self) -> str           # Gère "DEVOPSENGiNEER" → "DevOps Engineer"
    def extract_skills(self) -> List[str]       # 50+ mots-clés techniques
    def extract_companies(self) -> List[str]    # Patterns entreprises avancés
```

### Dépendances requises

- **Python** : `pytest`, `pdfplumber`, `pydantic`, `PyYAML`
- **Système** : `poppler-utils` (pour fallback pdftotext)
- **Modèles** : spaCy `en_core_web_sm`, données NLTK (pour legacy)

## 📊 Résultats actuels : ✅ 8/8 PASS

```
✅ Extraction réussie:
   Nom: Mathéo Guilloux
   Email: matheo.guilloux@gmail.com
   Poste: DevOps Engineer
   Compétences: 36
   Entreprises: 12
```

### Couverture des compétences

Le système détecte automatiquement **36 compétences techniques** depuis le CV, avec une couverture de **100%** des compétences définies dans `resume.yml` :

- **Cloud & IaC** : Terraform, Ansible, OVH, AWS, GCP
- **CI/CD & Orchestration** : GitLab, GitHub, Kubernetes, Docker, Helm
- **Langages** : Python, Go, Java, JavaScript, TypeScript, C++, Rust
- **Monitoring** : Grafana, Prometheus, ELK
- **Méthodologies** : Agile, Scrum, Jira, Confluence

## 🛠️ Scripts et commandes

### Commandes Makefile

```bash
make setup-ats      # Installation automatique des dépendances
make test-ats       # Tests pytest robustes
make test-legacy    # Ancien script shell (fallback)
make build-and-test # Build + test en une seule commande
```

### Tests pytest avancés

```bash
# Tous les tests avec détails
pytest tests/test_ats_compatibility.py -v

# Test spécifique avec output
pytest tests/test_ats_compatibility.py::TestATSCompatibility::test_skills_extraction -v -s

# Mode debug avec extraction complète
pytest tests/test_ats_compatibility.py --tb=long -s
```

## 🔍 Validation vs resume.yml

Le système compare automatiquement :

```yaml
# resume.yml (source de vérité)
basics:
  name: "Mathéo Guilloux"
  email: "matheo.guilloux@gmail.com"
  label: "DevOps Engineer"

skills:
  - name: "Cloud and IaC"
    keywords: ["Terraform", "Ansible", "OVH", "AWS (basic)", "GCP (basic)"]
```

vs

```python
# Extraction automatique du PDF
extracted_data = {
    'name': 'Mathéo Guilloux',           # ✅ Correspond
    'email': 'matheo.guilloux@gmail.com', # ✅ Correspond
    'position': 'DevOps Engineer',        # ✅ Correspond
    'skills': ['terraform', 'ansible', 'ovh', 'aws', 'gcp', ...]  # ✅ 70%+ coverage
}
```

## 🚦 Avantages vs ancien système

| Aspect | 🔴 Ancien (shell) | ✅ Nouveau (pytest) |
|--------|-------------------|----------------------|
| **Nom extrait** | "Math" (partiel) | "Mathéo Guilloux" (complet) |
| **Robustesse** | Fallback constant | Extraction primaire robuste |
| **Validation** | Manuel | Automatique vs resume.yml |
| **Maintenance** | Regex fragiles | Tests structurés |
| **CI/CD ready** | Basique | Intégration pytest native |
| **Debugging** | Limité | Fixtures + assertions détaillées |

## 📈 Recommandations ATS

Le système valide automatiquement que le CV respecte :

1. **✅ Structure claire** : Sections bien définies détectées
2. **✅ Mots-clés techniques** : 36 technologies identifiées
3. **✅ Formats standards** : Police et mise en page lisibles
4. **✅ Information accessible** : Nom et email extraits parfaitement

## 🚦 États de sortie

- **pytest : 8/8 PASS** : CV totalement ATS-compatible ✅
- **pytest : X/8 FAIL** : Problèmes détectés, voir détails ❌

Intégration CI/CD native avec codes de retour pytest standards.

---

## 🔧 Troubleshooting

### Test échoue : extraction nom
```bash
# Debug l'extraction
pytest tests/test_ats_compatibility.py::TestATSCompatibility::test_name_extraction -v -s
```

### Test échoue : compétences insuffisantes
```bash
# Voir les compétences manquantes
pytest tests/test_ats_compatibility.py::TestATSCompatibility::test_skills_extraction -v -s
```

### PDF non trouvé
```bash
# Build d'abord
make pdf
# Puis test
make test-ats
``` 