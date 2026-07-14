import matplotlib
import sys
if sys.platform == 'linux':
    matplotlib.use("module://matplotlib-backend-kitty")
from sklearn.ensemble import IsolationForest
#from plots.plots import plot_outlined_data


def flag_point_outlier(df, show_plot=False):
    # Utilizes IQR
    data = df["Return"]
    window_size = 20
    df["Rolling_q1"] = data.rolling(window=window_size).quantile(0.25)
    df["Rolling_q3"] = data.rolling(window=window_size).quantile(0.75)
    df["Rolling_IQR"] = df["Rolling_q3"] - df["Rolling_q1"]

    k = 1.5
    lower_limit=df["Rolling_q1"] - k * df["Rolling_IQR"]
    upper_limit=df["Rolling_q3"] + k * df["Rolling_IQR"]
    
    df["IQR_flag"] = (data < lower_limit) | (
        data > upper_limit
    )
    df['IQR_flag'] = df['IQR_flag'].astype(bool)
    '''
    if show_plot:
        plot_outlined_data(df, 'IQR_flag', lower_limit, upper_limit)
    '''
    return df
    

def z_flag(df, show_plot=False):
    data = df['Return']
    window_size = 20
    df['Rolling_Mean'] = data.rolling(window=window_size).mean()
    df['Rolling_std'] = data.rolling(window=window_size).std()
    df['Rolling_z'] = (data - df['Rolling_Mean'])/df['Rolling_std']

    threshhold = 3.0

    df['Z_flag'] = df['Rolling_z'].abs() > threshhold 
    df['Z_flag'] = df['Z_flag'].astype(bool)
    '''
    if show_plot:
        plot_outlined_data(df, 'Z_flag', None, None)
    '''
    return df

def flag_isolation_forest(df, features, show_plot=False):
    #default_features = ['Return', 'Rolling_std', 'Rolling_Mean']
    if features is None:
        features = ['Return', 'Rolling_std', 'Rolling_Mean']
    X = df[features].dropna()
    clf = IsolationForest(contamination=0.05, random_state=42)
    X['IF_flag'] = clf.fit_predict(X) == -1  # -1 = outlier, 1 = normal
    
    df['IF_flag'] = X['IF_flag']
    df['IF_flag'] = df['IF_flag'].fillna(False)
    df['IF_flag'] = df['IF_flag'].astype(bool)
    
    X = df[features].dropna()
    if len(X) < 20:
        df['IF_flag'] = False
        return df

    '''
    if show_plot:
        plot_outlined_data(df, 'IF_flag', None, None)
    '''
    return df

def anomaly_detection(df, features=None, combined_plot=False, show_individual_plot=False):
    df = flag_point_outlier(df, show_individual_plot)
    df = z_flag(df, show_individual_plot)
    df = flag_isolation_forest(df, features, show_individual_plot)
    
    df['Flag_count'] = df['IQR_flag'].astype(int) + df['Z_flag'].astype(int) + df['IF_flag'].astype(int)
    df['Flagged'] = df['Flag_count'] >= 2
    '''
    if combined_plot:
        plot_outlined_data(df, 'Flagged', None, None)
    '''
    return df