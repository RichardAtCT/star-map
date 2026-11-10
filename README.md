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
- Stereographic projection centred on the zenith; north up, east left. Star positions are precessed to the chosen date, so historic skies are right too.
- Place search uses the free [Open-Meteo geocoding API](https://open-meteo.com/en/docs/geocoding-api) (non-commercial use).
- The place box also accepts pasted coordinates — decimal, degrees/minutes/seconds, or a Google Maps / Apple Maps / OpenStreetMap link. The time zone comes from Open-Meteo and the place name from [BigDataCloud](https://www.bigdatacloud.com/free-api/free-reverse-geocode-to-city-api)'s free client-side reverse geocoder; if either is unreachable the time zone is estimated from longitude.
- Fonts: Cormorant Garamond, Playfair Display, Great Vibes and Jost (SIL OFL), embedded.
- Settings live in the URL, so any map can be shared as a link.
- "Your maps": every map you download or copy a link to is kept in the browser (localStorage, with a small thumbnail), so it can be reopened, tweaked and downloaded again. Nothing is sent anywhere.

## Editing
`index.html` is generated: the readable source is `src/template.html`, and `src/build.py` inlines the data, library and fonts into it.
To rebuild, put the d3-celestial data files (`stars.6.json`, `constellations.json`, `constellations.lines.json`, `mw.json`) and unpacked npm tarballs
(`astronomy-engine`, `@fontsource/cormorant-garamond`, `playfair-display`, `great-vibes`, `jost`, each in an `x_<name>/` folder) in one directory, then run
`python3 src/build.py <data_dir> src/template.html index.html`. Small tweaks can also be made straight in `index.html`.

## Notable skies
Each link opens the live site with that moment loaded.

- [One small step](https://richardatct.github.io/star-map/?date=1969-07-20&time=21%3A56&lat=29.5593&lon=-95.09&tz=America%2FChicago&label=Houston%2C+Texas&title=One+small+step&names=Apollo+11+%C2%B7+First+step+on+the+Moon&theme=midnight&font=classic)
- [RMS Titanic](https://richardatct.github.io/star-map/?date=1912-04-14&time=23%3A40&lat=41.7325&lon=-49.9469&tz=Etc%2FGMT%2B3&label=North+Atlantic&title=RMS+Titanic&names=Iceberg+sighted%2C+11%3A40+pm+ship%27s+time&theme=noir&font=modern)
- [The night the Wall fell](https://richardatct.github.io/star-map/?date=1989-11-09&time=23%3A30&lat=52.5547&lon=13.3984&tz=Europe%2FBerlin&label=Bornholmer+Strasse%2C+Berlin&title=The+night+the+Wall+fell&names=The+first+gate+opens&theme=ivory&font=bold)
- [Galileo looks at Jupiter](https://richardatct.github.io/star-map/?date=1610-01-07&time=19%3A00&lat=45.4064&lon=11.8768&tz=Europe%2FRome&label=Padua%2C+Italy&title=Galileo+looks+at+Jupiter&names=Three+small+stars+beside+a+planet&theme=navy&font=classic)
- [The first satellite](https://richardatct.github.io/star-map/?date=1957-10-04&time=22%3A28&lat=45.92&lon=63.342&tz=Europe%2FMoscow&label=Baikonur+Cosmodrome&title=The+first+satellite&names=Sputnik+1+lifts+off&theme=forest&font=modern)
- [D-Day begins](https://richardatct.github.io/star-map/?date=1944-06-06&time=00%3A16&lat=49.2422&lon=-0.2744&tz=Europe%2FLondon&label=Pegasus+Bridge%2C+Normandy&title=D-Day+begins&names=The+first+gliders+land&theme=noir&font=bold)
- [The year 2000](https://richardatct.github.io/star-map/?date=2000-01-01&time=00%3A00&lat=51.4779&lon=-0.0015&tz=Europe%2FLondon&label=Royal+Observatory%2C+Greenwich&title=The+year+2000&names=Midnight+on+the+prime+meridian&theme=midnight&font=script)
- [The Rumble in the Jungle](https://richardatct.github.io/star-map/?date=1974-10-30&time=04%3A00&lat=-4.3317&lon=15.3139&tz=Africa%2FKinshasa&label=Kinshasa%2C+Zaire&title=The+Rumble+in+the+Jungle&names=Ali+v+Foreman&theme=plum&font=bold)
- [Arabs to Mars](https://richardatct.github.io/star-map/?date=2021-02-09&time=19%3A57&lat=25.2267&lon=55.4621&tz=Asia%2FDubai&label=Dubai%2C+United+Arab+Emirates&title=Arabs+to+Mars&names=Hope+Probe+enters+Mars+orbit&theme=navy&font=modern)

## Licence
MIT — see `LICENSE`. Bundled third-party data, code and fonts keep their own licences, copied in `licenses/`.
