# PPTX → AI Text

> **Educational use only.** This project is published for learning and demonstration.
> Commercial use is not permitted; anyone considering commercial use is solely
> responsible for legal and regulatory compliance in every applicable jurisdiction.
> See [LICENSE](LICENSE).

**Convert .pptx into structured text with full layout fidelity — so an LLM can reproduce the deck instead of hallucinating one.**

LLMs are good at slide *content* and terrible at slide *geometry*. This tool serializes each shape with its position, size, fonts, colors, z-order and grouping into a compact text format an LLM can read — and faithfully write back from.

Typical loop: export deck → hand the structured text + your edits to an LLM → regenerate the deck with layout intact.

> Personal project; no employer code or data. Bring your own .pptx to try it.

## Run it

```bash
# it's a single client-side HTML file — nothing to install, nothing leaves your machine
start "PPT转AI文本.html"     # or just double-click it / open it in any modern browser
python launcher.py           # optional: serve on localhost instead (enables clipboard APIs everywhere)
```

Drag a `.pptx` onto the page; copy the structured text out.
