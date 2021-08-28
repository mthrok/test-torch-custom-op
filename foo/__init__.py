import torch

from . import _foo

torch.ops.load_library(_foo.__file__)

torch.ops.foo.foo()
