from .bconfig import Field, Blueprint

#

def _():
    import sys
    from .bconfig import ns

    module = sys.modules[__name__]

    class BconfigModule(module.__class__):
        def __call__(self, cls):
            return ns(cls)
    
    module.__class__ = BconfigModule

_()
del _

#

__all__ = [
    'Field',
    'Blueprint'
]