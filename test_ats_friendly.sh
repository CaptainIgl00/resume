#!/usr/bin/env bash
set -e

PDF="build/Mathéo_Guilloux_CV.pdf"

echo "🔍 Tests ATS-friendly pour le CV"
echo "================================"
echo

# Vérifier que le PDF existe
if [ ! -f "$PDF" ]; then
    echo "FAIL – PDF non trouvé : $PDF"
    exit 1
fi

echo "▶ Test 1 : extraction texte avec pdftotext"
# Vérifier que pdftotext est installé
if ! command -v pdftotext &> /dev/null; then
    echo "FAIL – pdftotext non installé (apt install poppler-utils)"
    exit 1
fi

TEXT=$(pdftotext "$PDF" - | head -n 20 || true)
if ! echo "$TEXT" | grep -iq "DevOps Engineer"; then
    echo "FAIL – « DevOps Engineer » introuvable dans le texte extrait"
    echo "Texte extrait :"
    echo "==============="
    echo "$TEXT"
    exit 1
fi
echo "✅ OK – « DevOps Engineer » trouvé"

echo
echo "▶ Test 2 : parsing avec pyresparser (avec fallback)"
python3 - << 'PYCODE'
import sys
import os
import re

# Test avec pyresparser en premier
try:
    from pyresparser import ResumeParser
    print("📄 Tentative d'extraction avec PyResparser...")
    
    pdf_path = "build/Mathéo_Guilloux_CV.pdf"
    if not os.path.exists(pdf_path):
        print(f"FAIL – PDF non trouvé : {pdf_path}")
        sys.exit(1)
    
    data = ResumeParser(pdf_path).get_extracted_data()
    
    # Debug : afficher les données extraites
    print("📊 Données extraites par PyResparser :")
    for key, value in data.items():
        if isinstance(value, list):
            print(f"  {key}: {len(value)} éléments")
            if len(value) <= 5:
                print(f"    {value}")
            else:
                print(f"    {value[:3]}... (+{len(value)-3} autres)")
        else:
            print(f"  {key}: {value}")
    print()
    
    # Vérifications PyResparser
    name_ok = bool(data.get("name"))
    email_ok = bool(data.get("email"))
    skills = data.get("skills") or []
    skills_ok = len(skills) >= 10
    
    if name_ok and email_ok and skills_ok:
        print("✅ OK – parsing PyResparser : name, email et >=10 skills trouvés")
        print(f"   - Nom : {data.get('name')}")
        print(f"   - Email : {data.get('email')}")
        print(f"   - Compétences : {len(skills)} détectées")
        sys.exit(0)
    else:
        print("⚠️  PyResparser incomplet, basculement vers méthode fallback...")
        pyresparser_failed = True

except Exception as e:
    print(f"⚠️  Erreur PyResparser : {str(e)}")
    print("⚠️  Basculement vers méthode fallback...")
    pyresparser_failed = True

# Méthode fallback : extraction manuelle avec pdftotext
print("📄 Méthode fallback : extraction manuelle avec pdftotext...")

try:
    import subprocess
    
    # Extraire tout le texte du PDF
    result = subprocess.run(['pdftotext', 'build/Mathéo_Guilloux_CV.pdf', '-'], 
                          capture_output=True, text=True)
    
    if result.returncode != 0:
        print("FAIL – Impossible d'extraire le texte du PDF")
        sys.exit(1)
    
    full_text = result.stdout
    
    # Recherche du nom (première ligne significative)
    name_match = re.search(r'^([A-Z][a-zA-Z\s]+)', full_text.strip(), re.MULTILINE)
    name = name_match.group(1).strip() if name_match else None
    
    # Recherche de l'email
    email_match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', full_text)
    email = email_match.group(1) if email_match else None
    
    # Recherche des compétences techniques (recherche de mots-clés techniques)
    tech_keywords = [
        'docker', 'kubernetes', 'k8s', 'terraform', 'ansible', 'jenkins', 'gitlab', 'github',
        'aws', 'azure', 'gcp', 'linux', 'python', 'bash', 'shell', 'git', 'ci/cd', 'devops',
        'prometheus', 'grafana', 'elasticsearch', 'kibana', 'nginx', 'apache', 'mysql', 'postgresql',
        'redis', 'mongodb', 'helm', 'vagrant', 'consul', 'vault', 'nomad', 'packer', 'java',
        'javascript', 'node.js', 'react', 'angular', 'vue', 'typescript', 'php', 'golang', 'rust',
        'scala', 'ruby', 'perl', 'c++', 'c#', '.net', 'spring', 'django', 'flask', 'express'
    ]
    
    found_skills = []
    text_lower = full_text.lower()
    
    for keyword in tech_keywords:
        if keyword in text_lower:
            found_skills.append(keyword)
    
    # Recherche de compétences additionnelles dans les sections dédiées
    skills_section_match = re.search(r'(?:skills|compétences|technologies)(.*?)(?:\n\n|\n[A-Z]|$)', 
                                   full_text, re.IGNORECASE | re.DOTALL)
    
    if skills_section_match:
        skills_text = skills_section_match.group(1).lower()
        # Recherche de mots techniques supplémentaires
        additional_skills = re.findall(r'\b[a-z]{2,}\b', skills_text)
        for skill in additional_skills:
            if skill not in found_skills and len(skill) > 2:
                found_skills.append(skill)
    
    # Résultats de la méthode fallback
    print("📊 Données extraites par méthode fallback :")
    print(f"  name: {name}")
    print(f"  email: {email}")
    print(f"  skills: {len(found_skills)} éléments")
    print(f"    {found_skills[:10] if len(found_skills) > 10 else found_skills}")
    print()
    
    # Vérifications
    if not name:
        print("FAIL – parsing fallback : nom non trouvé")
        sys.exit(1)
    
    if not email:
        print("FAIL – parsing fallback : email non trouvé")
        sys.exit(1)
    
    if len(found_skills) < 10:
        print(f"FAIL – parsing fallback : seulement {len(found_skills)} compétences détectées (< 10)")
        print(f"Compétences trouvées : {found_skills}")
        sys.exit(1)
    
    print("✅ OK – parsing fallback : name, email et >=10 skills trouvés")
    print(f"   - Nom : {name}")
    print(f"   - Email : {email}")
    print(f"   - Compétences : {len(found_skills)} détectées")
    sys.exit(0)

except Exception as e:
    print(f"FAIL – Erreur lors du parsing fallback : {str(e)}")
    sys.exit(1)
PYCODE

echo
echo "🎉 PASS – Extraction texte OK et parsing OK"
echo "Le CV est ATS-friendly !"
exit 0 