#!/bin/sh
# Renders _tools/share-card.html to assets/share-card.jpg (1200x630) with headless Chrome.
set -e
cd "$(dirname "$0")"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless=new --hide-scrollbars --window-size=1200,630 \
  --virtual-time-budget=8000 --screenshot=/tmp/share-card.png "file://$PWD/share-card.html"
python3 -c "from PIL import Image; Image.open('/tmp/share-card.png').convert('RGB').save('../assets/share-card.jpg', quality=85, optimize=True, progressive=True)"
rm -f /tmp/share-card.png
echo "wrote assets/share-card.jpg"
