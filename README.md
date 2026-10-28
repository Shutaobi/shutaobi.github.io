# Shutao Bi — Academic homepage

A responsive academic website with an editorial layout, built with plain HTML, CSS, and a small JavaScript audio player. No package manager, external font service, or framework is required. GitHub Actions compiles the CV from LaTeX and deploys the static files; the website itself needs no build step.

## Files

```text
index.html       All content and navigation
styles.css       Typography, layout, mobile, and print styles
script.js        Music controls (playback starts only with the Play button)
assets/          Snowfield background, decorative snowflake SVG, and MP3 audio
assets/fonts/    Self-hosted Source Serif 4 variable font and its license
thesis/          Locally hosted paper PDFs and computational code ZIP archives
code/geometric_realization/  Curated computational source and its own README
Shutao_Bi_CV.tex  Editable CV source (automatically compiled on GitHub)
.github/workflows/deploy.yml  CV compilation and Pages deployment
.nojekyll        Tells GitHub Pages to serve the static files directly
.gitignore       Keeps local system files and environment secrets out of Git
README.md        Editing and local preview instructions
```

The navigation links to Home, Research interests, Papers, CV, Contact, and Music within `index.html`. The fuller research overview, Talks / Notes, and unfilled paper metadata remain in the source with `hidden` attributes. They are omitted from the visible page and accessibility tree until real content is added. All paper, code, CV and audio URLs are preserved.

## Preview locally

In this folder, run:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Open <http://127.0.0.1:8000/>. Stop the server with `Ctrl+C`. You can also open `index.html` directly in a browser. HTML/CSS edits appear after refreshing. For a working local CV link, put a compiled copy of the CV at `cv/Shutao_Bi_CV.pdf`; see below. GitHub creates this file automatically when publishing.

## Edit the homepage

Open `index.html` in any text editor. Edit the name, role, email, and research interests in the `home` section; the interests aside retains the `research` anchor. To add a fuller research overview, fill `research-overview` and remove its `hidden` attribute. For talks and notes, add real entries and remove `hidden` from both the `talks` section and its navigation link. Keep existing section IDs unchanged so previously shared fragment links continue to work.

The color, typeface, and layout settings are in `styles.css`. Media queries adapt the layout to tablets, phones, and print. The footer's update date is manual: update it when you change the content.

## Editorial design

The page uses one paper-white reading surface, mist-blue accents, a running masthead, an opening author/research grid, numbered manuscript entries, and a listening note in the page margin. There are no translucent cards, rounded content containers, shadows, or animations. Manuscript titles have the strongest hierarchy after the author's name; dates, authors and resource links use separate typographic levels.

Source Serif 4 is self-hosted at `assets/fonts/SourceSerif4-Roman.woff2`, with `font-display: swap` and local serif fallbacks. It was obtained from [Adobe's official Source Serif repository](https://github.com/adobe-fonts/source-serif/tree/release/WOFF2/VAR). Its SIL Open Font License is included at `assets/fonts/SourceSerif4-LICENSE.txt`. Interface labels use system sans-serif fonts. No font service is contacted when visiting the site.

## Winter theme and music

The empty snowfield illustration appears as a faded panorama across the opening spread, rather than behind the entire document. The supplied screenshot was edited with the built-in imagegen tool to remove the dialogue panel, controls, video watermark and pet notification, reconstruct snow and footprints, and enhance detail. A further edit removes the central character, leaving the trees, distant mountains and footprints. `assets/images/winter-snowfield-empty.png` preserves the full edited output; the website uses its lighter JPEG copy. Previous illustrations are retained in the repository. The image is 1672 × 941 pixels. Its crop adjusts to screen shape. The small footer snowflake is `assets/snowflake.svg`. Decorations are ignored by assistive technology and omitted when printing.

The track is **恋色空 (Koiiro Sora) — Off Vocal Version**, converted from the supplied Apple Lossless M4A to a 192 kbps MP3 at `assets/audio/koiiro-sora-off-vocal.mp3` (about 9.1 MiB). The original audio file is unchanged. No cover art or embedded source metadata is included in the web copy.

The player is stopped by default and starts only when the visitor presses Play. There is no HTML autoplay attribute or JavaScript startup play call. Volume starts at 25%; the track loops after being started. The player provides play/pause, mute, seeking, and desktop volume controls. Mobile visitors can also use their device's volume controls. There are no global click handlers that unexpectedly restart paused music. Native audio controls remain available when JavaScript is disabled.

To change the track, replace the MP3 and update its source and display title in `index.html`. To remove the theme, remove the music player markup and script reference, then adjust the winter background and decoration rules in `styles.css`. Changes to CSS or JavaScript should also update the version query in the corresponding HTML reference to refresh browser caches.

## Add a paper

1. Copy the PDF into `thesis/`. Prefer a simple filename without spaces.
2. Copy the existing `<article class="paper">…</article>` block inside the `papers` section. Place the newest paper first if desired.
3. Give the copied heading a unique ID, such as `paper-title-3`, and use the same value for the article's `aria-labelledby` attribute. Update its visible `paper-number` ordinal and the manuscript count in the section heading.
4. Update the title, author names, status, date, and both PDF links. Also update the PDF link's `aria-label`.
5. Replace metadata placeholders with real links or a journal citation as available; remove `hidden` from the metadata list only when its remaining rows contain real information.

Example:

```html
<article class="paper" aria-labelledby="paper-title-3">
  <span class="paper-number" aria-hidden="true">03</span>
  <div class="paper-main">
    <p class="paper-status">Preprint · October 2026</p>
    <h3 id="paper-title-3"><a href="thesis/new-paper.pdf">New paper title</a></h3>
    <p class="paper-authors">Shutao Bi</p>
    <div class="paper-resources">
      <a class="pdf-link" href="thesis/new-paper.pdf"
         aria-label="Read New paper title (PDF)">Full text <span class="file-type">PDF</span></a>
    </div>
    <dl class="paper-metadata" hidden>
      <div><dt>arXiv</dt><dd>To be added</dd></div>
      <div><dt>DOI</dt><dd>To be added</dd></div>
      <div><dt>GitHub repository</dt><dd>To be added</dd></div>
      <div><dt>Journal</dt><dd>To be added</dd></div>
    </dl>
  </div>
</article>
```

For a metadata link, replace its `<dd>To be added</dd>` with `<dd><a href="YOUR_FULL_URL">YOUR_LINK_LABEL</a></dd>`, using the actual URL and label. Unavailable metadata stays hidden, so visitors never encounter placeholder text or fake links.

The first paper is a copy of the original thesis PDF. Its public link is `thesis/Wemyss_Semi-Simple_deformation_on_GV_algebras.pdf`. A path on your Mac would not work for website visitors. If you revise the original PDF, copy the updated file into this site's `thesis/` folder again; the files are not automatically synchronized.

Computational code is available from `thesis/thesis_external_files_2026-10-13.zip`, linked as **Computational code** below the paper. To add or update supporting code, copy its ZIP archive into `thesis/` and update the paper's download link in `index.html`. The publishing workflow includes both PDF and ZIP files from this folder.

**Geometric Realization**, by Shutao Bi (October 2026), is a separate manuscript linked from Papers / Preprints. Its PDF is `thesis/Geometric_Realization.pdf`, copied from the main `geometric_realization/` folder of the original research project. When revising it, replace this site's PDF copy and refresh the `v=` version marker in both of that paper's links in `index.html`.

Its **Computational code** download is `thesis/Geometric_Realization_computational_code.zip`. The curated source is maintained in `code/geometric_realization/`: two unchanged Python programs, the zero-quartic verifier's required JSON input, pinned dependency versions, and a concise README mapping the calculations to the manuscript. The ZIP contains only these five files under one top-level folder. Generated results, editorial reports, backups, and the manuscript itself are excluded. When updating this code, rebuild the ZIP from those five source files and refresh its `v=` marker in `index.html`. The deployment workflow already includes ZIP archives under `thesis/`.

## Update your CV

Edit `Shutao_Bi_CV.tex`, either locally in the LaTeX editor or directly in GitHub's file editor. Commit and push to `main`. The **Build CV and deploy website** workflow automatically:

1. Compiles the source with pdfLaTeX using TeX Live 2025.
2. Places the generated PDF at `cv/Shutao_Bi_CV.pdf` in the deployment artifact.
3. Checks the homepage's local links and publishes the static website.

The permanent CV URL is <https://shutaobi.github.io/cv/Shutao_Bi_CV.pdf>. The generated PDF is deployed directly, not committed back to the source branch. Only the `.tex` source needs to be maintained. A failed compilation stops deployment and leaves the previous published website intact.

For a CV-only update:

```sh
git add Shutao_Bi_CV.tex
git commit -m "Update CV"
git push origin main
```

Saving a local file alone does not upload it; a commit and push are required. Editing and committing the file on GitHub also triggers the workflow. You can retry a build in the repository's **Actions** tab, or use **Run workflow** to publish manually.

For local preview, export the PDF from the LaTeX editor, or use your existing local TeX installation to compile it, then copy it to `cv/Shutao_Bi_CV.pdf`. Local CV PDFs, LaTeX auxiliary files, and `_site/` are ignored by Git. The workflow publishes `index.html`, `styles.css`, `script.js`, `.nojekyll`, SVG, MP3, JPEG, PNG, WOFF2 and font-license TXT files under `assets/`, all PDFs and ZIP archives under `thesis/`, and the generated CV. If adding other website assets, include them in the workflow's staging step.

## Check after editing

- Open the local preview on desktop and at a narrow mobile width.
- Follow every navigation link and PDF link.
- Confirm the email link has the correct `mailto:` address.
- Check long paper titles for wrapping and keyboard focus visibility with Tab.
- Keep asset paths relative (`thesis/paper.pdf`, not `/thesis/paper.pdf` or a path on your Mac), so repository-based GitHub Pages URLs work.

## GitHub Pages

- GitHub account: `Shutaobi`
- Repository: `Shutaobi/shutaobi.github.io`
- Website address: <https://shutaobi.github.io/>
- Publishing source: **GitHub Actions**, triggered by pushes to **main**.

The repository uses `main`, with `origin` pointing to `https://github.com/Shutaobi/shutaobi.github.io.git`. GitHub Pages serves the website at the address above after a successful deployment.

The public repository is configured in **Settings → Pages** to use **GitHub Actions**. The workflow is `.github/workflows/deploy.yml`. GitHub supplies the `github.io` address and HTTPS; no custom domain, DNS changes, or `CNAME` file is needed. The website remains plain static HTML/CSS with no Jekyll or npm build. Actions versions are pinned to commits, and the build does not require a personal access token.

After the first deployment, future updates can be published from this folder with:

```sh
git add index.html styles.css script.js assets/ README.md thesis/ Shutao_Bi_CV.tex
git commit -m "Update academic homepage"
git push origin main
```

Add any newly created source files explicitly to `git add`; do not add generated CV PDFs. Check `git diff --cached` before committing. The workflow publishes changes pushed to `main` after CV compilation succeeds.

Official setup reference: <https://docs.github.com/en/pages/quickstart>.
