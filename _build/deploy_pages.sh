#!/usr/bin/env bash
# Build the site for GitHub Pages (served at /disha_platinum/) and publish it to the gh-pages branch.
# Usage (from the website folder, Git Bash):  bash _build/deploy_pages.sh
# For a custom domain later: set BASE="" and SITE="https://www.yourdomain.com", and add a CNAME file.
set -euo pipefail
REPO="https://github.com/brillbrainstechteam/disha_platinum.git"
BASE="/disha_platinum"
SITE="https://brillbrainstechteam.github.io/disha_platinum"
TMP="$(mktemp -d)"
cp -r assets "$TMP/"
rm -f "$TMP"/assets/css/*.bak
touch "$TMP/.nojekyll"
MSYS_NO_PATHCONV=1 MSYS2_ARG_CONV_EXCL="*" DISHAA_BASE="$BASE" DISHAA_SITE="$SITE" DISHAA_OUT="$TMP" python _build/build.py >/dev/null
cd "$TMP"
git init -q -b gh-pages
git add -A
git commit -q -m "Deploy Dishaa Platinum site to GitHub Pages ($(date +%F))"
git push -f "$REPO" gh-pages
echo "Deployed: $SITE/"
