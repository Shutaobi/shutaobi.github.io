# Shutao Bi — Academic homepage

A small, responsive academic website built with plain HTML and CSS. No JavaScript, package manager, external fonts, framework, or build step is required. The site works on GitHub Pages, including under a repository subpath.

## Files

```text
index.html       All content and navigation
styles.css       Typography, layout, mobile, and print styles
thesis/          Locally hosted paper PDFs
.nojekyll        Tells GitHub Pages to serve the static files directly
.gitignore       Keeps local system files and environment secrets out of Git
README.md        Editing and local preview instructions
```

The navigation links to sections within `index.html`: Home, Research, Papers / Preprints, Talks / Notes, CV, and Contact. Research interests appear on the homepage; the fuller Research overview and CV await your text/files. Talks / Notes and Contact are intentionally blank. The email link is in the homepage introduction.

## Preview locally

In this folder, run:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Open <http://127.0.0.1:8000/>. Stop the server with `Ctrl+C`. You can also open `index.html` directly in a browser. Edits appear after refreshing; nothing needs to be compiled.

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

## Add your CV

Create a `cv/` folder and save your PDF as `cv/Shutao_Bi_CV.pdf`. Replace the CV placeholder paragraph with:

```html
<p><a href="cv/Shutao_Bi_CV.pdf">Download CV (PDF)</a></p>
```

## Check after editing

- Open the local preview on desktop and at a narrow mobile width.
- Follow every navigation link and PDF link.
- Confirm the email link has the correct `mailto:` address.
- Check long paper titles for wrapping and keyboard focus visibility with Tab.
- Keep asset paths relative (`thesis/paper.pdf`, not `/thesis/paper.pdf` or a path on your Mac), so repository-based GitHub Pages URLs work.

## GitHub Pages

- GitHub account: `reveavecsolitude-lgtm`
- Repository: `reveavecsolitude-lgtm/reveavecsolitude-lgtm.github.io`
- Website address after deployment: <https://reveavecsolitude-lgtm.github.io/>
- Publishing source: **Deploy from a branch**, **main**, **/ (root)**.

The local repository is prepared on `main`, with `origin` pointing to `https://github.com/reveavecsolitude-lgtm/reveavecsolitude-lgtm.github.io.git`. Initial remote creation, upload, and publication await approval. This address will not serve this website until deployment completes.

For first publication, create the matching public repository without initializing it with a README, license, or `.gitignore`, then push the local `main` branch. In the repository's **Settings → Pages**, select **Deploy from a branch**, choose **main** and **/ (root)**, and save. GitHub supplies the `github.io` address and HTTPS; no custom domain, DNS changes, or `CNAME` file is needed. `.nojekyll` lets GitHub serve the plain static files without a Jekyll build.

After the first deployment, future updates can be published from this folder with:

```sh
git add index.html styles.css README.md thesis/
git commit -m "Update academic homepage"
git push origin main
```

Add any newly created folders, such as `cv/`, explicitly to `git add`. Check `git diff --cached` before committing. GitHub Pages will publish changes pushed to `main` once the publishing source is enabled.

Official setup reference: <https://docs.github.com/en/pages/quickstart>.
