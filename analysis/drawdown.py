import matplotlib
import sys
if sys.platform == 'linux':
    matplotlib.use("module://matplotlib-backend-kitty")

from plots.plots import plot



def drawdown_analysis(df, show_plot=False):
    data = df['Close']

    df['max_cumclosing'] = data.cummax()
    df['Drawdown'] = (data - df['max_cumclosing'])/df['max_cumclosing']
    if show_plot:
        plot(df, ['Drawdown'], 0, 2515)
        
    return df

