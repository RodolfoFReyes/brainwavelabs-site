# brainwavelabs.app

The Brainwave Labs website, served by GitHub Pages at https://brainwavelabs.app.

Run `python3 build.py` (no dependencies) after any change and commit the sources and the generated HTML.

- `src/pmconsole-privacy.md`, `src/pmconsole-support.md`: the policy and the support questions. Keep them in step with the copies in the app repo, `docs/app-store/`.
- `build.py`: the product page, home page, and support page layout (they mix text with images and cards), plus the shared header and footer.
- `style.css`: one stylesheet, light and dark. No outside fonts, scripts, analytics, or cookies, on purpose: the site practices what the privacy policy says.
- `img/`: the app icon (`pm-icon.svg` is the App Store icon cropped to its rounded square), the favicon and touch icon PNGs, the link-preview image (`og-pmconsole.jpg`, 1200x630), and screenshots from the app's demo data (`npm run store:screenshots` in the app repo, then 1600px wide JPEGs).

Pages:
- `/`: Brainwave Labs home
- `/pmconsole/`: PM Console product page (the App Store's Marketing URL)
- `/pmconsole/privacy/`: PM Console privacy policy (the App Store's Privacy Policy URL)
- `/pmconsole/support/`: PM Console support (the App Store's Support URL)

When the app goes on sale: replace `AVAILABILITY` in `build.py` ("Coming soon to the Mac App Store") with Apple's official "Download on the Mac App Store" badge linking to the app, using only Apple's badge artwork and following its marketing guidelines.
