#import matplotlib
#import sys
#if sys.platform == 'linux':
    #matplotlib.use("module://matplotlib-backend-kitty")

import plotly.graph_objects as go
import numpy as np
import scipy
from features.features import add_return, add_volatility
from analysis.anomaly import anomaly_detection
from analysis.fattails import get_kurtosis, get_skewness






def show_candle_stick(df):
    df = df.copy()
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"]
    )])
    fig.update_layout(
        dragmode="pan",
        xaxis_rangeslider_visible=False,
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        template="plotly_dark"
    )
    return fig


def show_returns_volatility(df, rolling=20):
    df = df.copy()
    df = add_return(df)
    df = add_volatility(df, rolling)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df.index,
        y=df["Return"],
        name="Daily Return",
        marker_color=["rgba(0,200,100,0.8)" if r >= 0 else "rgba(220,50,50,0.8)" for r in df["Return"]],
        width=24*60*60*1000  
    ))
    
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["Volatility"],
        name="Rolling Volatility",
        line=dict(color="rgba(255,180,0,0.6)", width=1.5),
        yaxis="y2"
    ))
    
    fig.update_layout(
        dragmode="pan",
        template="plotly_dark",
        xaxis_title="Date",
        yaxis_title="Return",
        yaxis2=dict(
            title="Volatility",
            overlaying="y",
            side="right"
        ),
        legend=dict(x=0, y=1)
    )
    return fig

def show_drawdown(df, rolling=20):
    df = df.copy()
    df = add_return(df)
    df = add_volatility(df, rolling)
    
    data = df['Close']
    df['max_cumclosing'] = data.cummax()
    df['Drawdown'] = (data - df['max_cumclosing']) / df['max_cumclosing']
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['Drawdown'],
        name="Drawdown",
        fill='tozeroy',
        line=dict(color='rgba(220,50,50,0.8)', width=1),
        fillcolor='rgba(220,50,50,0.2)'
    ))
    
    fig.update_layout(
        dragmode="pan",
        template="plotly_dark",
        xaxis_title="Date",
        yaxis_title="Drawdown",
        yaxis=dict(tickformat=".1%")
    )
    return fig

def show_anomaly_detection(df, rolling=20):
    df = df.copy()
    df = add_return(df)
    df = add_volatility(df, rolling)
    df = anomaly_detection(df)
    
    def build_fig(df, flag_col, lower=None, upper=None):
        flagged = df[df[flag_col]]
        normal = df[~df[flag_col]]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df["Return"],
            mode="lines",
            name="Return",
            line=dict(color="rgba(150,150,150,0.4)", width=1),
        ))
        
        fig.add_trace(go.Scatter(
            x=normal.index,
            y=normal["Return"],
            mode="markers",
            name="Normal",
            marker=dict(color="rgba(0,200,100,0.5)", size=4)
        ))
        
        fig.add_trace(go.Scatter(
            x=flagged.index,
            y=flagged["Return"],
            mode="markers",
            name="Anomaly",
            marker=dict(color="rgba(220,50,50,0.9)", size=6, symbol="x")
        ))
        
        if lower is not None:
            fig.add_trace(go.Scatter(
                x=df.index, y=lower,
                name="Lower Bound",
                line=dict(color="rgba(255,180,0,0.4)", dash="dash", width=1)
            ))
        if upper is not None:
            fig.add_trace(go.Scatter(
                x=df.index, y=upper,
                name="Upper Bound",
                line=dict(color="rgba(255,180,0,0.4)", dash="dash", width=1)
            ))
        
        fig.update_layout(
            dragmode="pan",
            template="plotly_dark",
            xaxis_title="Date",
            yaxis_title="Return"
        )
        return fig
    
    lower = df["Rolling_q1"] - 1.5 * df["Rolling_IQR"]
    upper = df["Rolling_q3"] + 1.5 * df["Rolling_IQR"]
    
    charts = {
        "Combined (All Methods)": lambda: build_fig(df, "Flagged"),
        "IQR":                    lambda: build_fig(df, "IQR_flag", lower, upper),
        "Z-Score":                lambda: build_fig(df, "Z_flag"),
        "Isolation Forest":       lambda: build_fig(df, "IF_flag"),
    }
    
    return charts

def show_fat_tails(df):
    df = df.copy()
    df = add_return(df)
    returns = df["Return"].dropna()
    
    mean, std = returns.mean(), returns.std()
    x = np.linspace(mean - 4*std, mean + 4*std, 100)
    y = scipy.stats.norm.pdf(x, mean, std)
    
    kurt_val = get_kurtosis(df)
    skew_val = get_skewness(df)
    
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=returns,
        nbinsx=len(df)//2,
        histnorm="probability density",
        name="Returns",
        marker=dict(color="rgba(0,150,255,0.6)", line=dict(color="black", width=0.5))
    ))
    
    fig.add_trace(go.Scatter(
        x=x, y=y,
        name="Normal Curve",
        line=dict(color="rgba(220,50,50,0.9)", width=2)
    ))
    
    fig.update_layout(
        dragmode="pan",
        template="plotly_dark",
        xaxis_title="Return",
        yaxis_title="Density",
         annotations=[
            dict(x=0.05, y=0.95, xref="paper", yref="paper", showarrow=False,
                    text=f"Kurtosis: {kurt_val:.4f}", font=dict(color="white")),
             dict(x=0.80, y=0.95, xref="paper", yref="paper", showarrow=False,
                 text=f"Skewness: {skew_val:.4f}", font=dict(color="white"))
            ]
        )
    return fig

def show_correlation_heatmap(df, columns, rolling=False, window=20):
    df = df.copy()
    df = add_return(df)
    df = add_volatility(df, window)
    
    data = df['Close']
    df['max_cumclosing'] = data.cummax()
    df['Drawdown'] = (data - df['max_cumclosing']) / df['max_cumclosing']

    if not rolling:
        corr_matrix = df[columns].corr()
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns.tolist(),
            y=corr_matrix.columns.tolist(),
            colorscale="RdBu",
            zmid=0, zmin=-1, zmax=1,
            text=corr_matrix.round(2).values,
            texttemplate="%{text}",
        ))
        fig.update_layout(template="plotly_dark")
    else:
        
        fig = go.Figure()
        pairs = [(columns[i], columns[j]) for i in range(len(columns)) for j in range(i+1, len(columns))]
        for c1, c2 in pairs:
            rolling_corr = df[c1].rolling(window).corr(df[c2])
            fig.add_trace(go.Scatter(
                x=df.index,
                y=rolling_corr,
                mode="lines",
                name=f"{c1} vs {c2}",
                line=dict(width=1.5)
            ))
        fig.add_hline(y=0, line=dict(color="rgba(255,255,255,0.2)", dash="dash"))
        fig.update_layout(
            dragmode="pan",
            template="plotly_dark",
            xaxis_title="Date",
            yaxis_title="Correlation",
            yaxis=dict(range=[-1.1, 1.1])
        )
    return fig