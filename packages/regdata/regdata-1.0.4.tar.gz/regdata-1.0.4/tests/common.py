from .lib import *


def backend_test(func):
    X, y, X_test = func(backend='numpy').get_data()
    assert X.dtype == y.dtype == X_test.dtype == np.float64
    X, y, X_test = func(backend='torch').get_data()
    assert X.dtype == y.dtype == X_test.dtype == torch.float64
    X, y, X_test = func(backend='tf').get_data()
    assert X.dtype == y.dtype == X_test.dtype == tf.float64


def plotting_test_with_plt(func):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    func(backend='numpy', scale_X=False, scale_y=False).plot(fig=fig, ax=ax)
    fig.savefig('figures/'+func.__name__+'.jpg')


def plotting_test_without_plt(func):
    fig, ax = func(backend='numpy', scale_X=False, scale_y=False).plot()
    fig.savefig('figures/'+func.__name__+'.jpg')


def non_syntetic_test(func):
    """
    Non-synthetic data should not have noise by default.
    """
    import pandas as pd
    obj = func(return_test=False, scale_X=False, scale_y=False,
               mean_normalize_y=False, backend='numpy')
    X, y = obj.get_data(squeeze_y=False)
    end_data = np.concatenate([X, y], axis=1)
    start_data = pd.read_csv('archive/'+obj.file_name).values
    assert np.allclose(end_data, start_data)
