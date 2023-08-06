import numpy as np
from .base import Base


class NonStat2D(Base):
    def __init__(self, return_test=True, scale_X=True, scale_y=True,
                 mean_normalize_y=False, test_train_ratio=2,
                 s_to_n_ratio=None, noise_variance=0.025**2, scaler='std',
                 min=-0.5, max=1, samples=121, random_state=0, backend=None):

        synthetic = True
        file_name = None
        def f(x1, x2): 
            b = np.pi * (2*x1 + 0.5*x2 + 1)
            return 0.1 * (np.sin(b*x1) + np.sin(b*x2))
        x1 = np.linspace(min, max, int(samples**0.5)).reshape(-1, 1)
        x2 = np.linspace(min, max, int(samples**0.5)).reshape(-1, 1)
        X1, X2 = np.meshgrid(x1, x2)
        X = np.array([(i,j) for i,j in zip(X1.ravel(), X2.ravel())])
        y = np.array([f(i,j) for i,j in zip(X1.ravel(), X2.ravel())]).reshape(-1,1)

        X_names = ['X1', 'X2']
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
