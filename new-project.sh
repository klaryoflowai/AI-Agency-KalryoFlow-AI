#!/bin/bash

# ============================================================
# new-project.sh — Creare automată proiect nou AI Agency
# Utilizare: ./new-project.sh "NumeClient" "Descriere scurtă"
# Exemplu:   ./new-project.sh "Restoconcept" "Automatizare comenzi WooCommerce"
# ============================================================

set -e

# --- Validare input ---
if [ -z "$1" ]; then
  echo "❌ Eroare: Specifică numele clientului."
  echo "   Utilizare: ./new-project.sh \"NumeClient\" \"Descriere scurtă\""
  exit 1
fi

CLIENT_NAME="$1"
DESCRIPTION="${2:-Proiect nou}"
DATE=$(date +%Y-%m)
PROJECT_ID="${DATE}_${CLIENT_NAME// /_}"
PROJECT_DIR="projects/${PROJECT_ID}"

# --- Verifică că nu există deja ---
if [ -d "$PROJECT_DIR" ]; then
  echo "❌ Eroare: Proiectul '$PROJECT_DIR' există deja."
  exit 1
fi

echo ""
echo "🚀 Creare proiect nou..."
echo "   Client:     $CLIENT_NAME"
echo "   Descriere:  $DESCRIPTION"
echo "   Folder:     $PROJECT_DIR"
echo ""

# --- Copiază template ---
cp -r projects/template "$PROJECT_DIR"

# --- Personalizează PROJECT.md ---
sed -i.bak \
  -e "s/\[NumeClient\]/$CLIENT_NAME/g" \
  -e "s/\[Descriere scurtă 1 rând\]/$DESCRIPTION/g" \
  -e "s/YYYY-MM_NumeClient/$PROJECT_ID/g" \
  -e "s/\[data azi\]/$(date +%Y-%m-%d)/g" \
  "$PROJECT_DIR/PROJECT.md"

rm -f "$PROJECT_DIR/PROJECT.md.bak"

# --- Personalizează .env.project ---
sed -i.bak \
  -e "s/YYYY-MM_NumeClient/$PROJECT_ID/g" \
  -e "s/CLIENT_NAME=/CLIENT_NAME=$CLIENT_NAME/g" \
  "$PROJECT_DIR/.env.project"

rm -f "$PROJECT_DIR/.env.project.bak"

# --- Asigură ignorarea env-ului proiectului ---
grep -qxF "projects/*/.env.project" .gitignore || echo "projects/*/.env.project" >> .gitignore

# --- Confirmare ---
echo "✅ Proiect creat cu succes!"
echo ""
echo "📁 Structură:"
find "$PROJECT_DIR" -not -name ".gitkeep" | sort | sed 's/^/   /'
echo ""
echo "👉 Pași următori:"
echo "   1. Deschide: $PROJECT_DIR/PROJECT.md"
echo "   2. Completează brieful clientului și parametrii"
echo "   3. Bifează agenții necesari"
echo "   4. Spune-i lui Codex sau Claude Code:"
echo "      'Citește $PROJECT_DIR/PROJECT.md și rulează eval-agent în modul MVP zero API'"
echo ""
