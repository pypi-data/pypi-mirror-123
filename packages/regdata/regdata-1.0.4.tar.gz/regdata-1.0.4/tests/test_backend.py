import pytest

def test_backend():
    import os
    import regdata as rd
    rd.set_backend('tf')
    assert os.environ['BACKEND'] == 'tf'
    rd.set_backend('torch')
    assert os.environ['BACKEND'] == 'torch'
    rd.set_backend('numpy')
    assert os.environ['BACKEND'] == 'numpy'
    with pytest.raises(NotImplementedError):
        rd.set_backend('thisdoesnotexist')
