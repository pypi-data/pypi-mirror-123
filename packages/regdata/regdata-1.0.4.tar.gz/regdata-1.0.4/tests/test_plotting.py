import pytest

def test_plotting():
    import regdata as rd
    rd.Step().plot(dims=[0])
    rd.NonStat2D().plot(dims=[0,1])
    with pytest.raises(ValueError):
        rd.Step().plot(dims=[0,1,2])

    with pytest.raises(ValueError):
        rd.Step().plot(dims=[])