from mistune import Renderer as BaseRenderer
from mistune_contrib.highlight import HighlightMixin
from mistune_contrib.math import MathRendererMixin


class Renderer(MathRendererMixin, HighlightMixin, BaseRenderer):
    pass
