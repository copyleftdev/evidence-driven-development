# Author handoff

The article is a draft. Nothing has been uploaded or published.

## Files

- `devto.md`: DEV-compatible front matter and article body.
- `preview.html`: local editorial reading copy; contains no third-party assets or scripts.
- `cover.svg` and `cover.png`: original 1000 × 420 artwork for an optional DEV cover.
- `research.md`: primary-source attribution, terminology and retrieval limitations.
- The project root contains the runnable companion and actual evidence directories.

## Before public release

1. Review first-person wording and choose the final author attribution.
2. Choose a distribution license and publish the standalone source repository if desired.
   No public repository URL exists yet. Add that real URL near the article's setup commands.
3. Paste `devto.md` into DEV's Markdown editor with `published: false`. Upload `cover.png`
   if using the cover, then use DEV's returned URL rather than a local filesystem path.
4. Preview code, tables, links and mobile reading in DEV. This project's HTML preview is
   an editorial aid, not a screenshot of DEV's renderer.
5. Publish only after the author's final review. Draft URLs can be shareable; uploading
   a draft is still an external disclosure and has not been performed here.

The tutorial is a fresh teaching example with synthetic task names and new measurements.
Do not add private screenshots, internal hostnames, original product details or copied
operational logs during editorial revisions.

## Rebuild the local reading copy

The app and evidence runner use only Python's standard library. Optional article rendering
uses Python-Markdown; optional SVG-to-PNG conversion uses CairoSVG. The generated HTML
and PNG are included so readers do not need those packages to use the project.

```sh
python3 scripts/render_article.py
```
