# Understanding the Lumos poster

Everything on the poster, explained: what each section claims, where every number came
from, and what to say when a judge points at it.

Read the three **Fix before printing** items first. They are the only things on this
page that can lose you points.

---

## Fix before printing

### 1. The two drafts disagree about the test suite

| Source | Claim |
| --- | --- |
| The orange draft | 553 passing, 67 test files, **0 failures** |
| The navy draft | 468 passing in core/renderer/ai/api, plus 320 passing and **25 failing** in web, "the suite is red" |
| The repository, as published today | 133 + 55 + 50 + 230 + 320 = **788 passing, 25 failing** |

The navy draft's 468 is exactly core + renderer + ai + api from the repo, so those two
agree. The orange draft's 553 and its "0 failures" match neither, and a red suite and a
green suite cannot both be true of the same commit.

**The poster currently uses the repository's numbers: 788 passing, 25 failing, CI red.**
If the orange draft's numbers come from newer local work, push it and update the poster.
If they do not, leave the poster as it is. Do not print "0 failures" over a red suite;
a judge who clones the repo will run `pnpm test` and see it exit non-zero.

### 2. The layout benchmark is not in the public repository

Section 3A (89.2% → 14.9%) is the single strongest piece of evidence on the poster. It
is also, right now, **not reproducible by anyone but you**. I searched the repo:

- No benchmark harness, no random-placement baseline, no seed 1337, no trial runner.
- The constraint solver itself **is** there, with real clearance handling
  (`packages/ai/src/solver.ts`, `DEFAULT_CLEARANCE`, `needsFrontClearance`, and a
  `describe("clearance")` block in `solver.test.ts`). So the architecture the poster
  describes is genuine.
- What is missing is the measurement harness that produced the table.

The rules explicitly allow updating the repository before the finals. **Push the
harness.** A judge who scans the QR, clones, and cannot find the thing your headline
number came from will mark you down on Evidence, and rightly.

### 3. One claim in the navy draft I could not verify

The navy draft says lighting is "guarded by pinned screenshot-diff render tests, so a
change that alters pixels fails in CI". I found no screenshot-diff implementation in the
repo, only a mention of the idea in `CLAUDE.md`. The poster therefore lists it under
**not measured** instead. If it does exist somewhere, tell me and I will move it.

---

## The shape of the poster

Seven numbered sections. Five of them carry a judging-pillar tag in the top-right
corner, so a judge scoring "Evidence" can find it in two seconds. Sections 2 and 3
exist to explain the product and the science behind it.

```
Header          Title, team, stack, repo QR, and the illustration
Claim band      The one sentence we are here to prove, plus four headline numbers
1. Problem                          [PROBLEM]
2. Purpose, and how it works        [THE PRODUCT]      <- the four-step strip
3. How the sun calculation works    [SCIENCE & METRICS]
4. The AI is never allowed to say where things go   [APPROACH]
5. Does the layout actually hold together?          [EVIDENCE]
6. The limits that shaped the build                 [CONSTRAINTS]
7. Where it fails, and what we have not checked     [HONESTY & TRAJECTORY]
Footer          QR to all sources, plus commands to run it yourself
```

### The header illustration

A cross-section of a room with a window, showing the same room under a low morning sun
and a high midday sun. The low sun throws daylight about four metres into the room; the
high sun lights only the strip by the window.

This is the whole product in one picture, and it is the thing to point at in the first
thirty seconds of judging: which of those two you get depends on your latitude, your
date, and which way the building faces, and that is exactly what the app computes.

---

## Section by section

### Header and claim band

**The claim:** "A browser tool can answer both questions that decide a room, will it fit
and what will the light be like, and we measured both answers instead of asserting them."

This is deliberately modest. The rubric says a modest claim that is convincingly
supported beats a broad claim that is only asserted. We are **not** claiming novel
science. Real solar geometry already exists in professional CAD (Chief Architect,
SketchUp with a sun extension) and in analysis tools (Shadowmap). What we claim is the
combination, in a browser, verified.

**The four headline numbers:**

| Number | Means |
| --- | --- |
| 0.219° | Worst disagreement between our sun and NOAA's reference model, all of 2026, three latitudes |
| 89 → 15% | Share of furniture placements breaking at least one hard rule: random placement versus our placer |
| 788 | Unit tests passing |
| 25 | Unit tests **failing**. CI is red. |

Putting the failure count in the headline row is deliberate. It signals honesty before a
judge has to dig for it, and Honesty is a full fifth of the score.

### 1. Problem

Four questions a listing photo cannot answer, then outside evidence that this costs real
money and affects real health:

| Claim on the poster | Source | Strength |
| --- | --- | --- |
| US$849.9 bn returned in 2025, 15.8% of retail | National Retail Federation and Happy Returns | Industry primary |
| Furniture 15–20%, size mismatch ~58% | Vendor blogs (Eightx, First Chair) | **Weakest source on the poster.** Flagged as indicative on the citations page |
| Sleep onset 22 min earlier, mood 7% higher | Nagare et al. 2021, *Int J Environ Res Public Health* 18(19):9980 | Peer reviewed |
| West-facing units, 2pm–6pm sun | Singapore reporting | Journalism, cited to show the problem is recognised locally |

The orange draft had `[citation needed — team to supply]` here. These fill it.

**If a judge presses on the 58% figure**, say so plainly: it comes from vendor-published
industry compilations rather than audited research, the direction is corroborated by the
NRF data, and the exact percentage should be treated as indicative. Saying that costs
you nothing and gains you credibility.

### 2. Purpose, and how it works

Four screenshots showing the actual loop: draw the room, put it on the map, scrub the
day, read the floor. These are cropped to complete regions by `crop-assets.py`, so each
one is a whole dialog or a whole view. Nothing is sliced through the middle.

The second image is worth pointing at during judging: it shows the privacy rounding
happening live. The readout says `1.29660, 103.87640 · shared as 1.30, 103.88`.

Underneath, the purpose in one sentence, and the feature list.

### 3. How the sun calculation works

The section a technical judge will spend the most time on. Three columns:

**The science.** Latitude, longitude, date and time give exactly one correct sun
position. We compute it from the standard astronomical formulas, then rotate it by the
building's offset from true north. The 3D engine casts shadows from a light pointing
exactly that way, so the shadows are predictions you can check by standing in the room.
Bounced light comes from a photographed 360° panorama of a real apartment, not a flat
grey fill. Floor brightness is real units: `lux = I · cosθ / d²`, summed over daylight
and every fixture, compared against the level a room of that type needs.

**What we considered.** Four options, three rejected with reasons: a mood preset (what
consumer planners do, looks nice and tells you nothing), offline path tracing (best
physics, cannot scrub a day at 60 fps in a browser), baked lighting (correct for one
arrangement, wrong the moment a chair moves). Chosen: real-time shadows on a
geographically derived sun.

**The metrics.** The NOAA comparison, described below.

### 4. Approach

The decision everything follows from: **the AI is never allowed to say where things go.**

Three options were on the table:

1. The model returns coordinates. Rejected: nothing checks it, failures are silent, and
   the same request gives a different room each time.
2. Fixed rules only, no model. Rejected: cannot interpret "cozy", "a reading corner", or
   "under $3,000".
3. The model describes intent, a deterministic placer positions it. **Chosen.**

The placer checks every candidate against every hard rule (inside the room, no overlap,
walkway clear, door can swing) and either returns a checked position or refuses with a
reason. Same request, same room, every time.

Below that, the architectural decision: one plain JSON file is the single source of
truth, every version ships an upgrader so old saves still open, and your address never
enters it.

### 5. Evidence

Two measurements, because the claim has two halves.

**A. Does the layout hold together?**

200 seeded trials, 3 to 6 items each, rooms 3.5 to 7 m wide. The same 885 placement
requests went to our placer and to a random-placement baseline. One checker, written
separately from the placer, graded both.

| Broken rule | Random | Ours |
| --- | --- | --- |
| Any rule broken | 89.2% | 14.9% |
| Outside the room | 50.5% | 0% |
| Overlapping another item | 74.8% | 0% |
| Walkway blocked | 44.6% | 14.9% |
| Door swing blocked | 26.2% | 0% |
| Said no rather than placing badly | 0% | 19.1% |

Three failure types go to zero. The fourth is a genuine defect, kept on the poster
rather than hidden (section 7).

**Say this before a judge says it to you:** the baseline is random placement, not a
language model. It shows these rules are hard to satisfy by chance. It does **not** show
we beat an LLM, and we do not present it as though it does.

**B. Is the sun in the right place?**

We rebuilt NOAA's published sun-position equations independently, sharing no code with
the app, and compared against what Lumos actually renders. Every 10 minutes, all of 2026,
three latitudes, 70,475 daylight readings. Worst disagreement anywhere: **0.219°**.

Why that is small, in terms anyone can check:

- The sun is **0.533° wide** in the sky, so the error is 41% of the width of the sun.
- It moves a shadow **3.8 mm at one metre**.
- Every shadow already has a soft edge (a penumbra) **9.3 mm** wide at that distance,
  because the sun is a disc and not a point.
- So the error is smaller than the blur that is already there. It cannot be seen.

Reproduce it yourself:

```bash
node scripts/validation/sun-direction-error.js
```

The script self-checks first: at solar noon on the June solstice New York must reach
90 − 40.71 + 23.44 = 72.7°, and it computes 72.724°. If that check failed, the numbers
below it would not be trustworthy.

**One finding worth volunteering.** Near the zenith, the *compass direction* of the sun
becomes unstable: above 89° elevation our azimuth disagrees with NOAA by up to 60°. That
is not a physics error, it is a quirk of the coordinate system. When the sun is almost
directly overhead, its compass bearing swings wildly for a tiny change in actual
direction, and the direction the renderer uses stays accurate to 0.215°. Singapore's sun
passes 88° on 20 days a year, so this is a tropical-latitude issue we measured rather
than assumed. Full per-band numbers are on the citations page.

### 6. Constraints

Five real limits, each with the decision it forced:

- **Speed.** 60 fps target, 300 draw calls, 500,000 triangles. Live meter on F9. Under
  40 fps for ten seconds, lighting quality drops a step automatically.
- **Cost.** The core loop costs nothing: no key, no network. Only photo relighting needs
  a paid model, at 35–90 seconds a call, which is what ruled out most free hosting tiers.
- **Privacy.** Address never enters the file. Coordinates rounded to about 1 km, rounded
  **on the server** so a modified browser cannot bypass it.
- **Abuse.** Image endpoints have no login by design, so a public link without a cap is a
  free image generator on your bill. A daily ceiling and a spend limit contain it.
- **Reliability and reach.** Graphics context loss recovers instead of white-screening.
  Saves are atomic. Panels become bottom sheets on phones.

### 7. Honesty and trajectory

The strongest section on the poster, and the one most teams get wrong by leaving out.

**The defect your own benchmark found.** 14.9% of placements leave a walkway blocked,
which the placer's own documentation says cannot happen. The cause is isolated: the
placer remembers each item's footprint as an obstacle but not the clear space in front of
it, so item 2 can land in the walkway item 1 reserved. All 107 observed violations have
that shape.

The reason this is impressive rather than embarrassing is *how it was found*. The unit
tests all pass, because they check each item against the room as it was when that item
was placed, which is the same blind spot the placer has. Only a checker written
separately, grading the finished room as a whole, could see it.

**Say this line out loud during judging:** "We left it in because the measurement is the
result. Shipping a quiet fix and a clean 0% would have hidden the most useful thing we
learned, which is that a test sharing its subject's assumptions cannot find this class of
bug."

Then the unglamorous list: time zones unverified, suite red, Postgres tested against an
imitation, Docker never run, no LLM benchmarked, **no user study at all**.

---

## The 10-minute session, mapped to the poster

| Time | What to do | Where on the poster |
| --- | --- | --- |
| 0:00–1:00 | Project, user, central claim | Header and claim band |
| 1:00–4:00 | Demo: draw, place on map, scrub the day, read the lux heatmap | Section 2 is the same sequence |
| 4:00–7:00 | The key decision, both measurements, one constraint | Sections 3, 4, 5, 6 |
| 7:00–10:00 | Questions | Section 7 answers most of them |

Have the app already open on the sample room before judging starts. No login, no setup.

---

## Questions a judge will probably ask

**"Is the sun actually right, or does it just look plausible?"**
It is measured. We rebuilt NOAA's published equations independently and compared 70,475
readings across three latitudes and a full year. Worst disagreement 0.219°, which is 41%
of the width of the sun and smaller than the soft edge every shadow already has. The
script is in the repo.

**"Your baseline is random placement. Isn't that a straw man?"**
Yes, and we say so on the poster. It establishes that these constraints are hard to
satisfy by chance. It does not establish that we beat a language model, and we do not
claim it does. Benchmarking a real LLM on the same workload is item four on our two-week
list.

**"Why is your test suite red?"**
A module port is still in progress. 25 tests point at paths that moved. The features
themselves work in the running app. It is the first thing on our two-week list, because
a red suite undermines every other number we are showing you.

**"You found a 14.9% defect and shipped it anyway?"**
We found it with a checker written independently of the placer, and left it in because
the measurement is the result. The root cause is isolated to one line of reasoning: we
register footprints as obstacles but not clearance zones. The fix is specified and the
harness to verify it already exists.

**"What would you do with two more weeks?"**
Fix the walkway defect and re-run this same benchmark, publishing before and after. Add
tests that grade a finished room as a whole. Verify time zones against reference tables.
Then put it in front of five real move-in shoppers, because zero outside users have used
this.

**"Isn't this just IKEA's room planner?"**
Consumer planners give you a lighting *mood*: a warm preset, a brightness slider. That
looks nice and tells you nothing about your flat. Real solar geometry exists, but in
professional CAD and specialist analysis tools, not in the furniture-shopping loop.
We put a measured sun into that loop.

---

## Editing the poster

See `README.md`. In short: edit `poster.html`, run `./make-pdf.sh`, and it rebuilds the
PDF and verifies it is still one A2 page. Type sizes and colours are CSS variables at the
top of the file.

The layout is full. Anything you add has to be paid for somewhere.
