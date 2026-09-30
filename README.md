# Shutao Bi — Academic homepage

A small, responsive academic website built with plain HTML and CSS. No JavaScript, package manager, external fonts, or framework is required. GitHub Actions compiles the CV from LaTeX and deploys the static files; the HTML and CSS themselves need no build step.

## Files

```text
index.html       All content and navigation
styles.css       Typography, layout, mobile, and print styles
thesis/          Locally hosted paper PDFs
Shutao_Bi_CV.tex  Editable CV source (automatically compiled on GitHub)
.github/workflows/deploy.yml  CV compilation and Pages deployment
.nojekyll        Tells GitHub Pages to serve the static files directly
.gitignore       Keeps local system files and environment secrets out of Git
README.md        Editing and local preview instructions
```

The navigation links to sections within `index.html`: Home, Research, Papers / Preprints, Talks / Notes, CV, and Contact. Research interests appear on the homepage; the fuller Research overview awaits your text. Talks / Notes and Contact are intentionally blank. The email link is in the homepage introduction, and the CV section links to the automatically generated PDF.

## Preview locally

In this folder, run:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Open <http://127.0.0.1:8000/>. Stop the server with `Ctrl+C`. You can also open `index.html` directly in a browser. HTML/CSS edits appear after refreshing. For a working local CV link, put a compiled copy of the CV at `cv/Shutao_Bi_CV.pdf`; see below. GitHub creates this file automatically when publishing.

## Edit the homepage

Open `index.html` in any text editor. The section IDs match the navigation links. Edit the name, role, email, and research interests in the `home` section. Replace the placeholder paragraph in `research` with your overview. Add content below the headings in `talks` and `contact` when ready. Keep each section ID unchanged unless you also update its navigation link.

The color and font settings are at the top of `styles.css`. The two screen-width media queries adapt the layout to tablets and phones. The footer's update date is manual: update it when you change the content.

## Add a paper

1. Copy the PDF into `thesis/`. Prefer a simple filename without spaces.
2. Copy the existing `<article class="paper">…</article>` block inside the `papers` section. Place the newest paper first if desired.
3. Give the copied heading a unique ID, such as `paper-title-2`, and use the same value for the article's `aria-labelledby` attribute.
4. Update the title, author names, status, date, and both PDF links. Also update the PDF link's `aria-label`.
5. Replace the metadata placeholders with real links or a journal citation as available.

Example:

```html
<article class="paper" aria-labelledby="paper-title-2">
  <p class="paper-status">Preprint · October 2026</p>
  <h3 id="paper-title-2"><a href="thesis/new-paper.pdf">New paper title</a></h3>
  <p class="paper-authors">Shutao Bi</p>
  <div class="paper-resources">
    <a class="pdf-link" href="thesis/new-paper.pdf"
       aria-label="Read New paper title (PDF)">Read PDF <span class="file-type">PDF</span></a>
  </div>
  <dl class="paper-metadata">
    <div><dt>arXiv</dt><dd>To be added</dd></div>
    <div><dt>DOI</dt><dd>To be added</dd></div>
    <div><dt>GitHub repository</dt><dd>To be added</dd></div>
    <div><dt>Journal</dt><dd>To be added</dd></div>
  </dl>
</article>
```

For a metadata link, replace its `<dd>To be added</dd>` with `<dd><a href="YOUR_FULL_URL">YOUR_LINK_LABEL</a></dd>`, using the actual URL and label. Unavailable resources are plain text, so visitors never encounter fake links.

The first paper is a copy of the original thesis PDF. Its public link is `thesis/Wemyss_Semi-Simple_deformation_on_GV_algebras.pdf`. A path on your Mac would not work for website visitors. If you revise the original PDF, copy the updated file into this site's `thesis/` folder again; the files are not automatically synchronized.

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

For local preview, export the PDF from the LaTeX editor, or use your existing local TeX installation to compile it, then copy it to `cv/Shutao_Bi_CV.pdf`. Local CV PDFs, LaTeX auxiliary files, and `_site/` are ignored by Git. The workflow publishes `index.html`, `styles.css`, `.nojekyll`, all PDFs under `thesis/`, and the generated CV. If adding other website assets, include them in the workflow's staging step.

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
git add index.html styles.css README.md thesis/ Shutao_Bi_CV.tex
git commit -m "Update academic homepage"
git push origin main
```

Add any newly created source files explicitly to `git add`; do not add generated CV PDFs. Check `git diff --cached` before committing. The workflow publishes changes pushed to `main` after CV compilation succeeds.

Official setup reference: <https://docs.github.com/en/pages/quickstart>.
