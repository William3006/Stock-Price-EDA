from data.loader import load_raw, load_new, save
from features.features import add_return, add_rolling, add_volatility, add_net_profit
from analysis.anomaly import anomaly_detection, flag_point_outlier
from analysis.fattails import show_fattails, add_Correlation_matrix, plot_heatmap
from analysis.drawdown import drawdown_analysis
from plots.plots import plot, plot_outlined_data, show_candle_stick




if __name__ == "__main__":

    mod = load_raw("NP_META_10y")
    add_return(mod)
    add_rolling(mod, 20)
    add_volatility(mod, 20)
    add_net_profit(mod)
    print(mod)
    plot(mod, ['Close', 'Rolling'], 0, 100)
    show_fattails(mod, 50)
    matrix = add_Correlation_matrix(mod, ['Return', 'Volatility', 'Rolling'])
    plot_heatmap(matrix)
    show_candle_stick(mod.iloc[0:60])
    anomaly_detection(mod, combined_plot=True, show_individual_plot=True)
    drawdown_analysis(mod, show_plot=True)
