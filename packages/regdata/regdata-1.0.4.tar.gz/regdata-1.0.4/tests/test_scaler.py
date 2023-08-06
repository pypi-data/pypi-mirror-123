import pytest


def test_scaler():
    import regdata as rd
    rd.Step(scaler='minmax').get_data()
    rd.Step(scaler='minmax', scale_y=False, mean_normalize_y=False).get_data()

    rd.Step(scaler='std', mean_normalize_y=True, scale_y=False).get_data()

    with pytest.raises(NotImplementedError):
        rd.Step(scaler='somescaler').get_data()

    with pytest.raises(ValueError):
        rd.Olympic(scaler='std', mean_normalize_y=True,
                   scale_y=True).get_data()
    with pytest.raises(ValueError):
        rd.Olympic(scaler='minmax', mean_normalize_y=True,
                   scale_y=False).get_data()
