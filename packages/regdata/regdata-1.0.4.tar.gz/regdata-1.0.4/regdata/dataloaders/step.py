import numpy as np
from .base import Base


class Step(Base):
    def __init__(self, return_test=True, scale_X=True, scale_y=True,
                 mean_normalize_y=False, test_train_ratio=2, s_to_n_ratio=None,
                 noise_variance=10**-4, scaler='std', Min=-1, Max=1, num_low=25, num_high=25,
                 gap=-0.1, random_state=0, backend=None):

        synthetic = True
        file_name = None
        
        X = np.vstack((np.linspace(Min, -gap/2.0, num_low)[:, np.newaxis],
                       np.linspace(gap/2.0, Max, num_high)[:, np.newaxis]))
        y = np.vstack((np.zeros((num_low, 1)), np.ones((num_high, 1))))
        f = lambda x: y

        X_names = ['X']
        y_names = ['y']
        super().__init__(X=X,
                         y=y,
                         f=f,
                         file_name=file_name,
                         X_names=X_names,
                         y_names=y_names,
                         return_test=return_test,
                         scale_X=scale_X,
                         scale_y=scale_y,
                         mean_normalize_y=mean_normalize_y,
                         test_train_ratio=test_train_ratio,
                         s_to_n_ratio=s_to_n_ratio,
                         noise_variance=noise_variance,
                         scaler=scaler,
                         backend=backend,
                         random_state=random_state,
                         synthetic=synthetic)
