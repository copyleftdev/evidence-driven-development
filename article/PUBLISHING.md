# DEV.to publishing handoff

The companion repository and two gist assets are public. The DEV.to article itself remains
an unpublished local draft; no article has been uploaded to DEV.to by this workflow.

## Hosted assets

- [Companion repository](https://github.com/copyleftdev/evidence-driven-development): code, synthetic evidence, artwork and prompts.
- [Selected V3 cover](https://raw.githubusercontent.com/copyleftdev/evidence-driven-development/1f03111db02d359b24602992eddae60122d49d74/article/cover-particles-v3.png): public PNG, pinned to the source commit.
- [Experiment contract gist](https://gist.github.com/copyleftdev/01e8f0e2b919392f1a7a1a6fc1fa8665).
- [SQLite implementation gist](https://gist.github.com/copyleftdev/0cf6b00eb0ec5e01f2ab3c5cabee8328).
- `assets.json`: canonical URLs, local source paths and SHA-256 values for the gist mirrors.

The V2 artwork, V3 typography version, their generation prompts and earlier vector cover
are all retained. The article uses V3. Cover art was generated with an image-generation tool.

## Move the draft into DEV

1. Paste `devto.md` into DEV's Markdown editor. Keep `published: false` until ready.
2. The front matter already includes the hosted `cover_image` URL. In the rich editor,
   select the matching cover separately if that editor does not import the front matter.
3. Preview the repository card and both gist embeds in DEV. The article uses the universal
   `{% embed URL %}` syntax supported by the [DEV editor guide](https://dev.to/p/editor_guide).
4. Check code scrolling, tables, cover cropping and mobile reading in DEV's own preview.
5. Review author wording and decide the distribution license before presenting the code
   as licensed open source. A public repository alone does not supply a reuse license.
6. Publish the article only when the author requests it.

The source checkout, cover and recorded results use commit `1f03111db02d359b24602992eddae60122d49d74`. The gist URLs
are editable mirrors, so preserve their published contents; link a new revision when
changing the teaching example. Pinned repository copies remain the reference.

## Local reading copy

`preview.html` uses the local V3 cover and locally rendered snapshots of the gist source.
It loads no third-party scripts or styles. It does not reproduce DEV's renderer. Original
QA files describe the earlier layout; publication QA is recorded separately.

The app and evidence runner use only Python's standard library. Optional article rendering
uses Python-Markdown. Run `python3 scripts/render_article.py` to rebuild the reading copy.
No image conversion package is needed for the selected PNG cover.

Use only this project's synthetic content during editorial changes. Do not add private
screenshots, internal hostnames, unrelated product details or operational logs.
