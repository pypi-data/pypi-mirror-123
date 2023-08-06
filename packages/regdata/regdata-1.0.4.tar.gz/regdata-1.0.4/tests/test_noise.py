import pytest

def test_noise():
    import regdata as rd
    with pytest.raises(ValueError):
        rd.Step(s_to_n_ratio=2, noise_variance=2)
