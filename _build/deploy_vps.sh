#!/usr/bin/env bash
# Build the site for the client's own domain and upload it to the VPS (nginx).
# Usage (from the website folder, Git Bash):
#   DOMAIN=www.dishaaplatinum.com VPS=user@1.2.3.4 bash _build/deploy_vps.sh
# Optional: WEBROOT (default /var/www/$DOMAIN), SSH_PORT (default 22)
set -euo pipefail
: "${DOMAIN:?set DOMAIN, e.g. DOMAIN=www.dishaaplatinum.com}"
: "${VPS:?set VPS, e.g. VPS=ubuntu@203.0.113.10}"
WEBROOT="${WEBROOT:-/var/www/$DOMAIN}"
SSH_PORT="${SSH_PORT:-22}"
SITE="https://$DOMAIN"

TMP="$(mktemp -d)"
WTMP="$(cygpath -m "$TMP" 2>/dev/null || echo "$TMP")"   # Windows Python needs a native path
cp -r assets "$TMP/"
rm -f "$TMP"/assets/css/*.bak
# domain root: BASE is empty, canonical/OG/sitemap point at the real domain
MSYS_NO_PATHCONV=1 MSYS2_ARG_CONV_EXCL="*" DISHAA_BASE="" DISHAA_SITE="$SITE" DISHAA_OUT="$WTMP" python _build/build.py >/dev/null
test -f "$TMP/index.html" && test -f "$TMP/about/index.html" || { echo "Build output missing - aborting"; exit 1; }

echo "Uploading to $VPS:$WEBROOT ..."
# upload to a fresh release folder, then swap it in atomically (no half-updated site)
REL="$WEBROOT.release-$(date +%Y%m%d%H%M%S)"
tar -C "$TMP" -czf - . | ssh -p "$SSH_PORT" "$VPS" "set -e; mkdir -p '$REL' && tar -xzf - -C '$REL' && \
  if [ -d '$WEBROOT' ] && [ ! -L '$WEBROOT' ]; then mv '$WEBROOT' '$WEBROOT.pre-deploy-backup'; fi; \
  ln -sfn '$REL' '$WEBROOT.tmp' && mv -T '$WEBROOT.tmp' '$WEBROOT'; \
  ls -1dt '$WEBROOT'.release-* | tail -n +4 | xargs -r rm -rf"
rm -rf "$TMP"
echo "Deployed: $SITE/"
