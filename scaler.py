from sklearn.preprocessing import RobustScaler, StandardScaler, MinMaxScaler

class scaler:
    def __init__(self, data, scale):
        self.data = data.copy()
        self.scale = scale
        self.scaler = None
        self.scale_info = None


    def set_scaler(self):

        scale_info = {
            self.scale == 'minmax' : MinMaxScaler(),
            self.scale == 'robust' : RobustScaler(),
            self.scale == 'standard' : StandardScaler()
            }
        
        self.scale_info = scale_info

    def fit(self, cols):
        scaler.set_scaler(self)

        self.scaler = self.scale_info[True]

        X = self.data[[cols]]

        fit_scaler = self.scaler.fit(X)
        trans_df = fit_scaler.transform(X)
        self.data.loc[:, cols] = trans_df

        return self.data

if "__name__"=="__main__":
    df = scaler(times, 'minmax').fit('count')