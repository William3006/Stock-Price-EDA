from data.loader import load_raw, load_new, save
from features.features import add_return, add_rolling, add_volatility, add_net_profit
from analysis.anomaly import anomaly_detection, flag_point_outlier
from analysis.fattails import show_fattails, add_Correlation_matrix, plot_heatmap
from analysis.drawdown import drawdown_analysis
from plots.plots import plot, plot_outlined_data, show_candle_stick




if __name__ == "__main__":
#####################################################FIX IT FOR WINDOWS############################################