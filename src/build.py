"""Builds the single-file site: python3 -I build.py <data_dir> <template> <out>"""
import sys, json, base64, glob, os
import numpy as np

data, template, out = sys.argv[1], sys.argv[2], sys.argv[3]
J = lambda n: json.load(open(os.path.join(data, n)))
compact = lambda o: json.dumps(o, separators=(",", ":"), ensure_ascii=False)

# ---- stars: flat ints [ra*100, dec*100, mag*10, bv*10]
stars = []
for f in J("stars.6.json")["features"]:
    ra, dec = f["geometry"]["coordinates"]
    try: bv = float(f["properties"].get("bv") or 0.6)
    except ValueError: bv = 0.6
    stars += [round(ra * 100), round(dec * 100), round(f["properties"]["mag"] * 10), round(bv * 10)]

# ---- constellation lines: list of flat polylines
lines = []
for f in J("constellations.lines.json")["features"]:
    for seg in f["geometry"]["coordinates"]:
        lines.append([round(v * 100) for p in seg for v in p])

# ---- constellation names
names = []
for f in J("constellations.json")["features"]:
    ra, dec = f["geometry"]["coordinates"]
    names.append([f["properties"]["name"], round(ra, 1), round(dec, 1)])

# ---- Milky Way: rasterise nested outline polygons to a 2-degree grid
def vec(lon, lat):
    lon, lat = np.radians(lon), np.radians(lat)
    return np.stack([np.cos(lat) * np.cos(lon), np.cos(lat) * np.sin(lon), np.sin(lat)], -1)

STEP = 2
lons = np.arange(-180 + STEP / 2, 180, STEP)
lats = np.arange(-90 + STEP / 2, 90, STEP)
grid = np.zeros((len(lats), len(lons)))
B = vec(192.8595, 27.1283)  # north galactic pole: certainly outside the band
for f in J("mw.json")["features"]:
    C, D = [], []
    for poly in f["geometry"]["coordinates"]:
        for ring in poly:
            v = vec(np.array(ring)[:, 0], np.array(ring)[:, 1])
            C.append(v[:-1]); D.append(v[1:])
    C, D = np.concatenate(C), np.concatenate(D)
    N2 = np.cross(C, D); CD = C + D
    for i, la in enumerate(lats):
        for j, lo in enumerate(lons):
            A = vec(lo, la)
            N1 = np.cross(A, B)
            c1 = (C @ N1) * (D @ N1) < 0
            c2 = (N2 @ A) * (N2 @ B) < 0
            p = np.cross(N1, N2)
            same = ((p * CD).sum(1) > 0) == ((p @ (A + B)) > 0)
            if np.count_nonzero(c1 & c2 & same) % 2: grid[i, j] += 1

# light blur (lon wraps)
k = np.array([1, 2, 3, 2, 1.0]); k /= k.sum()
g = sum(w * np.roll(grid, s, 1) for w, s in zip(k, range(-2, 3)))
gp = np.pad(g, ((2, 2), (0, 0)), mode="edge")
g = sum(w * gp[s:s + len(lats)] for w, s in zip(k, range(5)))
mw = "".join(str(int(round(v / 5 * 9))) for v in g.flatten())
print("mw levels", {c: mw.count(c) for c in "0123456789"})

def b64(pattern):
    (p,) = glob.glob(os.path.join(data, pattern))
    return base64.b64encode(open(p, "rb").read()).decode()

rep = {
    "STARS": compact(stars), "LINES": compact(lines), "NAMES": compact(names),
    "MW": mw, "MW_W": str(len(lons)), "MW_H": str(len(lats)),
    "ASTRO": open(glob.glob(os.path.join(data, "x_astronomy*/package/astronomy.browser.min.js"))[0]).read(),
    "F_SERIF": b64("x_fontsource-cormorant*/package/files/cormorant-garamond-latin-500-normal.woff2"),
    "F_SERIF_I": b64("x_fontsource-cormorant*/package/files/cormorant-garamond-latin-500-italic.woff2"),
    "F_PLAYFAIR": b64("x_fontsource-playfair*/package/files/playfair-display-latin-500-normal.woff2"),
    "F_SCRIPT": b64("x_fontsource-great*/package/files/great-vibes-latin-400-normal.woff2"),
    "F_SANS": b64("x_fontsource-jost*/package/files/jost-latin-400-normal.woff2"),
}
html = open(template, encoding="utf-8").read()
for k_, v in rep.items():
    assert "{{%s}}" % k_ in html, k_
    html = html.replace("{{%s}}" % k_, v)
open(out, "w", encoding="utf-8").write(html)
print("wrote", out, len(html) // 1024, "KB;", len(stars) // 4, "stars,", len(lines), "lines,", len(names), "names")
