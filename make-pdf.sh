#!/usr/bin/env bash
# Regenerate Lumos-Poster-A2.pdf from poster.html.
#
#   ./make-pdf.sh
#
# Needs Google Chrome installed. Everything else is handled here.
set -euo pipefail
cd "$(dirname "$0")"

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
[ -x "$CHROME" ] || CHROME="/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
[ -x "$CHROME" ] || { echo "No Chrome or Edge found. Install Chrome, or use the manual route in README.md."; exit 1; }

PORT=8899

# 1. Inline the screenshots so the PDF is self-contained.
node build.js

# 2. Serve the folder (Chrome will not read local files reliably).
python3 -m http.server "$PORT" >/dev/null 2>&1 &
SERVER=$!
trap 'kill $SERVER 2>/dev/null || true' EXIT
sleep 1

# 3. Print to PDF at true A2.
"$CHROME" --headless --disable-gpu --no-sandbox --no-pdf-header-footer \
  --print-to-pdf="Lumos-Poster-A2.pdf" \
  "http://localhost:$PORT/poster-standalone.html" 2>&1 | tail -1

# 4. Confirm it came out as one A2 page.
python3 - <<'PY'
import re
d = open('Lumos-Poster-A2.pdf', 'rb').read()
box = re.search(rb'/MediaBox\s*\[([^\]]+)\]', d)
w, h = [float(x) for x in box.group(1).split()][2:4]
pages = len(re.findall(rb'/Type\s*/Page[^s]', d))
print("page size : %.1f x %.1f mm  (A2 = 420.0 x 594.0)" % (w * 25.4 / 72, h * 25.4 / 72))
print("pages     : %d  %s" % (pages, "OK" if pages == 1 else "<-- content overflows, see README"))
print("file size : %.2f MB" % (len(d) / 1048576))
PY
