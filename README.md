# asterion_sphinx_style

Sphinx style for Asterion public documentation.

A plain sphinx extension, usable in any sphinx project:

```python
# conf.py
extensions = ["asterion_sphinx_style"]
```

It configures [sphinx-rtd-theme](https://sphinx-rtd-theme.readthedocs.io/) rather than shipping a theme of its own, so everything a reader already knows about Read the Docs navigation still holds.

## Install

```bash
pip install asterion-sphinx-style
```

If a project already builds its `extensions` list elsewhere, rebind rather than mutate:

```python
extensions = [*extensions, "asterion_sphinx_style"]
```

## Overriding

Everything is applied **only when the project left it unset**, so your `conf.py` always wins:

```python
html_logo = "_static/my-logo.png"   # yours, not Asterion's
html_theme = "furo"                 # the style stops configuring the theme
```

One caveat: `html_theme` reads as `alabaster` when a project has not chosen one, so a project that deliberately picks `alabaster` is indistinguishable from one that picked nothing, and the style will switch it to `sphinx_rtd_theme`. Any other theme is respected.

## Palette

Sampled from the logo wordmark and `AsterionReport.cls`. Contrast is against white, WCAG 2.1.

| Role | Hex | Ratio | |
|---|---|---|---|
| Brand blue | `#0832F6` | 7.51:1 | AAA — safe for links and body text |
| Deep blue | `#030189` | 15.33:1 | navigation header, admonition titles |
| Navy | `#010042` | 19.45:1 | hover and visited states |
| Alert red | `#DC0000` | 5.19:1 | danger and error admonitions only |

## What it does, and what it deliberately does not

Sets, when unset: `html_theme`, `html_logo`, `html_favicon`, and the theme's `style_nav_header_background`. Adds one stylesheet and its own static directory (appended, so your `_static` keeps precedence).

It does **not** repaint the theme's navigation machinery — the current-page tree, expand/collapse states, light/dark alternation. That is a tuned system, and a style that rewrites it ends up fighting the theme on every release. Only surfaces that read as *brand* are touched.

## Design rules

A style is typically installed once and applied to every version of a site, including releases cut years earlier. Three rules follow:

1. **Fill, never clobber** — a project's own settings always win.
2. **Absolute paths, appended** — packaged assets by absolute path; `html_static_path` appended to on `builder-inited`, never assigned.
3. **Never warn** — doc builds commonly run under `-W`, where one warning on one old page fails an entire site.

## Versioning

The git tag is the only version that exists; `pyproject.toml` is `dynamic` via `hatch-vcs`. A release is `git tag vX.Y.Z && git push --tags`.

## License

Apache-2.0. See [LICENSE](LICENSE). The Asterion Robotics logo and name are trademarks of Asterion Robotics and are not covered by that grant.
