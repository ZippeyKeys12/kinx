from mistune import BlockLexer as BaseBlockLexer
from mistune import InlineLexer as BaseInlineLexer
from mistune_contrib.math import MathBlockMixin, MathInlineMixin


class InlineLexer(MathInlineMixin, BaseInlineLexer):
    def __init__(self, *args, **kwargs):
        super(InlineLexer, self).__init__(*args, **kwargs)
        self.enable_math()


class BlockLexer(MathBlockMixin, BaseBlockLexer):
    def __init__(self, *args, **kwargs):
        super(BlockLexer, self).__init__(*args, **kwargs)
        self.enable_math()
