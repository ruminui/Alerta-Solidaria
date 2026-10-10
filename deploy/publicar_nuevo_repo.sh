#!/usr/bin/env bash
set -euo pipefail
# Requires the user to create a NEW independent GitHub repo and authenticate `gh auth login`.
# Use only inside the unzipped ALERTA_SOLIDARIA_2026/ directory.
TARGET="${1:-}"
if [[ ! "$TARGET" =~ ^[a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+$ ]]; then
  echo "Uso: bash deploy/publicar_nuevo_repo.sh USUARIO/REPO_NUEVO"; exit 2
fi
if ! command -v gh >/dev/null; then echo "Instalá GitHub CLI: https://cli.github.com/"; exit 1; fi
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then echo "Error: ejecutá el script fuera de un repositorio preexistente"; exit 1; fi
if gh repo view "$TARGET" >/dev/null 2>&1; then echo "Error: el repositorio ya existe. Evitamos sobrescribir código."; exit 1; fi
git init -b main
git add README.md LICENSE .gitignore app backend tests docs native deploy
if git diff --cached --name-only | grep -E '(^|/)(\.env|[^/]*\.sqlite|[^/]*\.db)$'; then echo "Datos no permitidos"; exit 1; fi
git commit -m 'Initial open-source public safety community pilot'
gh repo create "$TARGET" --public --source=. --remote=origin --push
echo "Repositorio publicado; verificar: https://github.com/$TARGET"
