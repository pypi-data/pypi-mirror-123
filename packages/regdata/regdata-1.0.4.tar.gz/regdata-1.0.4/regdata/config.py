import os

def set_backend(backend):
    if backend == 'numpy':
        import numpy        
    elif backend == 'torch':
        import torch
    elif backend == 'tf':
        import tensorflow
    else:
        raise NotImplementedError('backend "'+ backend +'" is not implemented')

    os.environ['BACKEND'] = backend