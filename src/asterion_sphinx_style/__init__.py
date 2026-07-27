# Copyright 2026 Asterion Robotics
# SPDX-License-Identifier: Apache-2.0

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Author: Thibault Poignonec <t.poignonec@asterion-robotics.com>

"""Asterion Robotics' sphinx style — a plain sphinx extension.

Add it to any project's ``conf.py``::

    extensions = ["asterion_sphinx_style"]

It configures :mod:`sphinx_rtd_theme` rather than shipping a theme of its own,
so everything a reader knows about Read the Docs' navigation still holds.

Three rules govern everything here, because a style is typically installed once
and applied to *every* version of a documentation site, including releases cut
years earlier:

1. **Fill, never clobber.** Every setting is applied only when the project left
   it unset, so a repo's own ``conf.py`` always wins. That is what makes
   overriding the logo a one-liner rather than a style option.
2. **Absolute paths, appended.** Packaged assets are handed to sphinx by
   absolute path and ``html_static_path`` is appended to on ``builder-inited``,
   never assigned, so a project's own ``_static`` survives.
3. **Never warn.** Documentation builds run under ``-W`` more often than not,
   where a single warning on a single old page fails an entire site.

The palette is the brand's, sampled from the logo and the report template.
Every colour clears WCAG AA against both white and its own foreground; the
brand blue clears AAA on white.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # pragma: no cover - typing only, keeps import cost at zero
    from sphinx.application import Sphinx
    from sphinx.config import Config

try:  # pragma: no cover - trivial, and untestable from a source checkout
    from importlib.metadata import PackageNotFoundError, version

    __version__ = version("asterion-sphinx-style")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0"

BRAND_BLUE = "#0832F6"
"""The wordmark blue. 7.51:1 on white — AAA for body text, so it is safe for links."""

DEEP_BLUE = "#030189"
"""``AsterionBlueInner``, the report cover's gradient centre. Brand surfaces."""

NAVY = "#010042"
"""``AsterionBlueOuter``, the gradient edge. Deeper surfaces and hover states."""

ALERT_RED = "#DC0000"
"""The report's confidential stamp. Danger admonitions only."""

THEME = "sphinx_rtd_theme"
SPHINX_DEFAULT_THEME = "alabaster"
"""What ``html_theme`` reads as when a project has not chosen one."""

STATIC_DIR = Path(__file__).parent / "static"
STYLESHEET = "asterion.css"
LOGO = STATIC_DIR / "asterion-logo.png"
"""The white wordmark: the navigation header it sits on is a dark brand block."""
FAVICON = STATIC_DIR / "asterion-favicon.png"


def _apply_defaults(_app: Sphinx, config: Config) -> None:
    """Fill in what the project left unset. Never overwrite a deliberate choice."""
    if config.html_theme in ("", SPHINX_DEFAULT_THEME):
        config.html_theme = THEME
    if not config.html_logo:
        config.html_logo = str(LOGO)
    if not config.html_favicon:
        config.html_favicon = str(FAVICON)

    # Theme options are per-theme, so only touch them when the theme is ours.
    # setdefault, not assignment: a project may have set some of these already.
    if config.html_theme == THEME:
        options: dict[str, Any] = dict(config.html_theme_options or {})
        options.setdefault("style_nav_header_background", DEEP_BLUE)
        config.html_theme_options = options


def _register_static(app: Sphinx) -> None:
    """Append, so a project's own ``_static`` keeps precedence."""
    app.config.html_static_path.append(str(STATIC_DIR))


def setup(app: Sphinx) -> dict[str, Any]:
    app.connect("config-inited", _apply_defaults)
    app.connect("builder-inited", _register_static)
    app.add_css_file(STYLESHEET)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
