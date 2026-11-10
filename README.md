# The Sky That Night

A free star map poster maker: the night sky exactly as it looked at one moment and place, as a print-ready PNG.
Everything is in `index.html` — no build step, no server, no API keys.

## Deploy on GitHub Pages
1. Create a repo and add `index.html` (and this README) to the `main` branch.
2. Repo **Settings → Pages → Build and deployment → Deploy from a branch → `main` / root**.
3. The site appears at `https://<user>.github.io/<repo>/` within a minute or two.

## How it works
- ~5,000 naked-eye stars, constellation lines and Milky Way outlines from [d3-celestial](https://github.com/ofrohn/d3-celestial) (BSD-3-Clause), embedded in the page.
- Moon (with phase) and planets from [astronomy-engine](https://github.com/cosinekitty/astronomy) (MIT), embedded.
- Stereographic projection centred on the zenith; north up, east left.
- Place search uses the free [Open-Meteo geocoding API](https://open-meteo.com/en/docs/geocoding-api) (non-commercial use; coordinates can also be typed in by hand).
- Fonts: Cormorant Garamond, Playfair Display, Great Vibes and Jost (SIL OFL), embedded.
- Settings live in the URL, so any map can be shared as a link.

## Editing
`index.html` is generated: the readable source is `src/template.html`, and `src/build.py` inlines the data, library and fonts into it.
To rebuild, put the d3-celestial data files (`stars.6.json`, `constellations.json`, `constellations.lines.json`, `mw.json`) and unpacked npm tarballs
(`astronomy-engine`, `@fontsource/cormorant-garamond`, `playfair-display`, `great-vibes`, `jost`, each in an `x_<name>/` folder) in one directory, then run
`python3 src/build.py <data_dir> src/template.html index.html`. Small tweaks can also be made straight in `index.html`.
