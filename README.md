# Project Lumos poster, LaunchPad Symposium

A2 portrait (420 x 594 mm), built as HTML so you can edit it and re-export the PDF in
one command.

## Files

| File | What it is |
| --- | --- |
| **`Lumos-Poster-A2.pdf`** | **Print this.** One A2 page, fonts and images embedded. |
| **`POSTER-GUIDE.md`** | **Read this.** Every section and number explained, the 10-minute script, likely judge questions. Starts with three things to fix before printing. |
| `poster.html` | **Edit this.** The source, commented throughout. |
| `site/index.html` | The evidence page the footer QR points at, deployed to Vercel. |
| `poster-standalone.html` | Generated. Same poster with images inlined, for sharing one file. |
| `make-pdf.sh` | Regenerates the PDF and checks it is still one A2 page. |
| `build.js` | Inlines `assets/*.jpg`. Called by `make-pdf.sh`. |
| `crop-assets.py` | Crops the raw screenshots to complete regions. Re-run if you change a crop. |
| `assets/` | The cropped screenshots the poster uses. |

## About the screenshots

They are cropped by `crop-assets.py` to regions that are whole on their own terms: a
full dialog, a full plan view. The poster then shows each one **entire**, at its natural
proportions. Nothing is sliced by CSS.

To change what a screenshot shows, edit its box in `crop-assets.py` (the numbers are
left, top, right, bottom in the 1600x1000 original), then:

```bash
python3 crop-assets.py && ./make-pdf.sh
```

## The sources page

The footer QR points at **https://lumos-evidence.vercel.app**, a public page with every
citation, the full validation method, and all raw numbers. No sharing step, no login:
a judge can scan it and read it immediately. See "The evidence page" at the bottom for
how to edit and redeploy it.

## The edit to PDF loop

1. Edit `poster.html` in any text editor.
2. Run:

```bash
./make-pdf.sh
```

It rebuilds `Lumos-Poster-A2.pdf` and confirms it is still **one A2 page**. If it
reports overflow, you added more than fits; see "When content overflows".

To preview without exporting, open `poster.html` in Chrome. It scales to fit your
screen, and the PDF is always full size.

**By hand instead:** open `poster.html` in Chrome, press Cmd+P, Destination **Save as
PDF**, Paper size **A2**, Margins **None**, tick **Background graphics**, Save.

## Editing

Everything visual is a CSS variable at the top of `poster.html`.

**Type sizes.** These are sized against the NUS COMP STePS poster guideline, which
asks for body text legible at 1.5 m. Raise `--t-body` and the whole poster reflows.

```css
--t-title: 22mm;    /* PROJECT LUMOS */
--t-h2:    7.6mm;   /* section headings */
--t-body:  4.3mm;   /* main body text, about 12 pt */
--t-sm:    4.0mm;   /* the smaller body text used in most sections */
--t-table: 3.8mm;
--t-cap:   3.2mm;   /* figure captions */
```

**Colours.** Change one value and it updates everywhere.

```css
--ink:    #0A1428;  /* dark navy: header, evidence band, footer */
--paper:  #EDF0F4;  /* page background */
--sun:    #C77A16;  /* amber accent on light backgrounds */
--sun-hi: #FFC24B;  /* amber on dark backgrounds only */
--ok:     #2F7D5E;  /* green, "complete" bullets */
--gap-c:  #B4552F;  /* rust, "known gap" bullets */
```

**Poster size.** Swap the two values for landscape.

```css
--poster-w: 420mm;
--poster-h: 594mm;
```

> **Check this with the organisers.** Their email says "A2 poster (37 cm height)".
> True A2 is 420 x 594 mm and 37 cm matches neither dimension. This is built at
> standard A2 portrait. If they really mean a 370 mm height, set `--poster-h: 370mm`
> and re-run `./make-pdf.sh`, but the content will need trimming, so confirm first.

**Content.** Sections are marked with comments matching the judging rubric:

```html
<!-- (1) PROBLEM -->     <!-- (2) APPROACH -->   <!-- (3) EVIDENCE -->
<!-- (4) CONSTRAINTS --> <!-- (5) HONESTY & TRAJECTORY -->
```

Bullet colour comes from a class: `<li class="ok">` green, `<li class="part">` amber,
`<li class="gap">` rust, plain `<li>` uses the accent.

**Swapping a screenshot.** Put the new image in `assets/`, point the `<img src>` at it,
re-run `./make-pdf.sh`. Images are cropped to a 27 mm band. If the wrong part shows,
adjust `object-position` on that figure's class (`.f-map`, `.f-lux`, `.f-day`); first
number is horizontal, second vertical, both percentages.

### When content overflows

The layout is full. Anything you add has to be paid for somewhere. In rough order of
least damage:

1. Shrink the figures: `figure img{ height:27mm }` down to `24mm`.
2. Drop `--t-sm` by 0.1 mm.
3. Tighten `--gap: 4mm` to `3mm`.
4. Cut a bullet.

Do not go below about `--t-body: 4mm` if you want to stay near the NUS readability
guideline.

### Changing where the QR points

Both QR codes are inline SVG, so they need regenerating if a URL changes:

```bash
npm install qrcode
node -e "require('qrcode').toString('YOUR_URL',{type:'svg',margin:0,errorCorrectionLevel:'M'}).then(s=>console.log(s))"
```

Copy the `d` attribute from the `<path stroke=...>` in the output, and paste it over the
matching path in `poster.html`. Keep the `viewBox` in sync: a longer URL produces more
modules (both QRs are currently 29x29).

## Where the numbers came from

The measurement in section 3 is reproducible. Two scripts were added to the Lumos repo
at `scripts/validation/`:

```bash
node scripts/validation/sun-vs-noaa.js
node scripts/validation/sun-direction-error.js
```

They re-implement NOAA's Solar Position Algorithm from the published equations, sharing
no code with the app, and compare against `suncalc@1.9.0` exactly as
`packages/core/src/sunlight.ts` calls it. **Run them before the finals so you can say
you have.** They self-check against two analytic solar-noon values before reporting.

Every other figure comes from the repo's own docs (`README.md`,
`docs/submission/WRITEUP.md`) or a source listed on the citations page.

## The evidence page

`site/index.html` is deployed at **https://lumos-evidence.vercel.app** and is what the
poster's footer QR points at. It carries every citation, the full NOAA validation method
with the equations, all raw numbers behind sections 3 and 5, and the limits we do not
claim.

Redeploy after editing it:

```bash
cd site && vercel deploy --prod --yes
```

The QR is also exported as `assets/qr-evidence.jpg` (1600 x 1600 px, ~1350 dpi at 30 mm)
if you need to drop it into a slide or another document.
