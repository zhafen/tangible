"""Usage: python -m tangible [REPO_PATH] > factory.svg"""

import sys

from .render import render_svg

sys.stdout.write(render_svg(sys.argv[1] if len(sys.argv) > 1 else "."))
