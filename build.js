// Inlines assets/*.jpg into poster.html as data URIs -> poster-standalone.html
// Edit poster.html; run `node build.js` to regenerate the shareable single file.
const fs = require('fs');
const path = require('path');
let html = fs.readFileSync('poster.html', 'utf8');
let n = 0;
html = html.replace(/src="assets\/([^"]+)"/g, (m, file) => {
  const p = path.join('assets', file);
  if (!fs.existsSync(p)) { console.warn('MISSING:', p); return m; }
  const ext = path.extname(file).slice(1).replace('jpg', 'jpeg');
  n++;
  return 'src="data:image/' + ext + ';base64,' + fs.readFileSync(p).toString('base64') + '"';
});
fs.writeFileSync('poster-standalone.html', html);
console.log('inlined', n, 'images ->', (fs.statSync('poster-standalone.html').size / 1048576).toFixed(2), 'MB');
