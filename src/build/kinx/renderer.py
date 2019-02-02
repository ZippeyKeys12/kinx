from mistune import Renderer as BaseRenderer
from mistune import escape
from mistune_contrib.highlight import HighlightMixin
from mistune_contrib.math import MathRendererMixin
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name


class Renderer(MathRendererMixin, HighlightMixin, BaseRenderer):
    pass
