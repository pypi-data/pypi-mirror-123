from .base import Base

class Jump1D(Base):
    def __init__(self, return_test=True, scale_X = True, scale_y = True, 
                mean_normalize_y=False, test_train_ratio=2, s_to_n_ratio=None,
                noise_variance=None, scaler='std', random_state=0, backend=None):

        synthetic=False
        f = None
        file_name = 'jump1d.csv'
        X, y, X_names, y_names = self.check_download_and_get(file_name)


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