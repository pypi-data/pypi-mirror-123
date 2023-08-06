import os
import warnings
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from ..config import set_backend


class Base:
    def __init__(self, X, y, f, file_name, X_names, y_names, return_test, scale_X, scale_y,
                 mean_normalize_y, test_train_ratio, s_to_n_ratio,
                 noise_variance, scaler, random_state, backend, synthetic):

        # Setting all variables as self: https://stackoverflow.com/a/1389304/13330701
        # __dict__ holds and object's attributes
        self.__dict__.update(locals())
        del self.__dict__["self"]  # don't need `self`

        self.N = self.X.shape[0]

        # Assert some rules
        self.check_asserts()

        # Set global backend
        if self.backend is not None:
            set_backend(self.backend)

        # Adding noise to data
        self.add_noise()

        # Set X_test if required
        if self.return_test:
            self.set_X_test()

        # Scale X
        self._scale_X()

        # Scale y
        self._scale_y()

    def set_X_test(self):
        if self.X.shape[1] == 1:
            Min = self.X.min()
            Max = self.X.max()
            Range = Max-Min
            n = self.N*self.test_train_ratio
            self.X_test = np.linspace(Min-Range/10, Max+Range/10, n).reshape(-1, 1)
        elif self.X.shape[1] == 2:
            Min = self.X.min(axis=0)
            Max = self.X.max(axis=0)
            Range = Max-Min
            n = int(self.N**0.5)*self.test_train_ratio
            x1 = np.linspace(Min[0]-Range[0]/10, Max[0] + Range[0]/10, n).reshape(-1, 1)
            x2 = np.linspace(Min[1]-Range[1]/10, Max[1] + Range[1]/10, n).reshape(-1, 1)
            X1, X2 = np.meshgrid(x1, x2)
            self.X_test = np.array([(i,j) for i,j in zip(X1.ravel(), X2.ravel())])
        # For future
        # else:
        #     raise ValueError("X_test generation is unsupported for more than two dimensions")

    def add_noise(self):
        self.y_original = self.y.copy()
        np.random.seed(self.random_state)
        if self.s_to_n_ratio != None and self.noise_variance != None:
            raise ValueError(
                "set either s_to_n_ratio OR noise_variance. Both can't be set.")
        elif self.s_to_n_ratio != None:
            var_y = np.var(self.y)
            noise_std = np.sqrt(var_y/self.s_to_n_ratio)
        elif self.noise_variance != None:
            noise_std = np.sqrt(self.noise_variance)
        else:
            noise_std = 0.
        self.y = self.y + np.random.normal(0, noise_std, (self.N, 1))

    def get_data(self, squeeze_y=True):
        self.y = self.y.squeeze() if squeeze_y else self.y
        returnable = [self.X, self.y]
        if self.return_test:
            returnable.append(self.X_test)
        return map(self.transform, returnable)

    def transform(self, array):
        backend = self.get_backend()
        if backend == 'numpy':
            return array
        elif backend == 'tf':
            import tensorflow as tf
            return tf.convert_to_tensor(array)
        elif backend == 'torch':
            import torch
            return torch.tensor(array)

    def get_backend(self):
        return os.environ['BACKEND']

    def _scale_X(self):
        """
        Scaling X data
        """

        if self.scaler == 'minmax':
            feature_range = (0, 1) if self.scale_X else (
                self.X.min(), self.X.max())
            self.X_scaler = MinMaxScaler(feature_range=feature_range)
        elif self.scaler == 'std':
            with_mean, with_std = (
                True, True) if self.scale_X else (False, False)
            self.X_scaler = StandardScaler(
                with_mean=with_mean, with_std=with_std)
        else:
            # This also handles future error in scale_y
            raise NotImplementedError('scaler: '+self.scaler)

        self.X = self.X_scaler.fit_transform(self.X)
        if self.return_test:
            self.X_test = self.X_scaler.transform(self.X_test)

    def _scale_y(self):
        """
        Scaling y data
        """
        if self.scale_y and self.mean_normalize_y:
            raise ValueError(
                "set either scale_y=True OR mean_normalize_y=True")
        if self.scaler == 'minmax':
            if self.scale_y:
                feature_range = (0, 1)
            elif self.mean_normalize_y:
                raise ValueError("This option is invalid when scaler='minmax'")
            else:
                feature_range = (self.y.min(), self.y.max())
            self.y_scaler = MinMaxScaler(feature_range=feature_range)
        elif self.scaler == 'std':
            if self.scale_y:
                with_mean, with_std = True, True
            elif self.mean_normalize_y:
                with_mean, with_std = True, False
            else:
                with_mean, with_std = False, False
            self.y_scaler = StandardScaler(
                with_mean=with_mean, with_std=with_std)

        self.y = self.y_scaler.fit_transform(self.y)
        self.y_original = self.y_scaler.fit_transform(self.y_original)

    def _plot1D(self, fig, ax, dims, **kwargs):
        if self.synthetic:
            ax.plot(self.X, self.f(self.X), label='True f')
        ax.scatter(self.X, self.y, label='data', **kwargs)
        ax.set_xlabel(self.X_names[dims[0]])
        ax.set_ylabel(self.y_names[0])
        ax.legend()
        return fig, ax

    def _plot2D(self, fig, ax, dims, **kwargs):
        if self.synthetic:
            n = self.X.shape[0]
            X1, X2 = np.meshgrid(self.X[:,dims[0]], self.X[:,dims[1]])
            Z = np.array([self.f(i,j) for i,j in zip(X1.ravel(), X2.ravel())]).reshape(n,n)
            ax.contourf(X1, X2, Z, levels=30, **kwargs)
            ax.set_xlabel(self.X_names[dims[0]])
            ax.set_ylabel(self.X_names[dims[1]])
            return fig, ax
        # For future
        # else:
        #     raise ValueError('2D plotting is currently unsupported for non-synthetic datasets')

    def _plot(self, fig, ax, dims, **kwargs):
        max_dim = self.X.shape[1]
        if dims is None:
            if max_dim == 2:
                return self._plot2D(fig, ax, [0,1], **kwargs)
            elif max_dim == 1:
                return self._plot1D(fig, ax, [0], **kwargs)
            # For future
            # elif max_dim > 2:
            #     raise ValueError("Please specify dims for if data has dimensions more than 2")
        else:
            if len(dims) > 2:
                raise ValueError("More than 2 dimensions are not supported")
            elif len(dims) == 2:
                return self._plot2D(fig, ax, dims, **kwargs)
            elif len(dims) == 1:
                return self._plot1D(fig, ax, dims, **kwargs)
            else:
                raise ValueError("This error should only occur if dims is an empty list")

    def plot(self, fig=None, ax=None, dims=None, **kwargs):
        if fig is not None and ax is not None:
            return self._plot(fig, ax, dims, **kwargs)

        try:
            plt
        except NameError:
            import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        return self._plot(fig, ax, dims, **kwargs)

    def check_download_and_get(self, name):
        if not os.path.exists(os.environ['DATAPATH']+name):
            warnings.warn('data not found. Downloading...')
            path = 'https://raw.githubusercontent.com/patel-zeel/regdata/main/archive/'+name
            data = pd.read_csv(path)
            data.to_csv(os.environ['DATAPATH']+name, index=None)
        else:
            data = pd.read_csv(os.environ['DATAPATH']+name)
        cols = data.columns
        X = data[cols[0]].values.reshape(-1, 1)
        y = data[cols[1]].values.reshape(-1, 1)

        X_names = [cols[0]]
        y_names = [cols[1]]
        return X, y, X_names, y_names

    def check_asserts(self):
        assert len(
            self.X.shape) == 2, "X should have shape (*,*) but has "+str(self.X.shape)
        assert len(
            self.y.shape) == 2, "y should have shape (*,1) but has "+str(self.y.shape)
        assert self.y.shape[1] == 1, "y should have shape (*,1) but has "+str(
            self.y.shape)
        assert self.X.shape[0] == self.y.shape[0], "X and y must be of the same length"
