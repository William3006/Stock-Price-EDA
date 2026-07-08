import pandas as pd
import yfinance as yf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt



def load_new(Name_of_stock, Period):
    ticker = yf.Ticker(Name_of_stock)
    data = ticker.history(period=Period)
    return pd.DataFrame(data)

    
def load_raw(name, i=None, j=None):
    if(i is None or j is None):
        return pd.read_csv(f'csv_saves/{name}.csv')
    
    return pd.read_csv(f'csv_saves/{name}.csv', skiprows=i, nrows=j)


def save(df, name):
    df.to_csv(f'csv_saves/{name}.csv', index=False)
    print(f'Saved Successfully to csv_saves/{name}.csv!')
    

def add_net_profit(raw_data):
    raw_data["Net"] = raw_data["Close"] - raw_data["Open"]
    raw_data["Profit"] = raw_data["Net"] > 0
    return raw_data


def add_rolling(mod1, time_span):
    mod1['Rolling'] = mod1['Close'].rolling(window=time_span).mean()
    return mod1


# just realised there's a built in pandas that does this for me and it uses Bessel's correction😭😭😭

def add_volatility(df, rolling):
    df['Volatility'] = df['Close'].rolling(window=rolling).std()
    return df
    
    
'''
def add_volatility(df, rolling):
    df['diff']=(df['Close']-df['Rolling'])**2
    df['roll_diff']=df['diff'].rolling(window=rolling).sum()
    df['Volatility']=np.sqrt((df['roll_diff']/rolling))
    
    df=df.drop(columns=['diff', 'roll_diff'])

    return df
    '''
#For my current setting of running the code from terminal in Arch, the plt.show method does not work, hence working around it using Agg
def plot(df, columns, i, j):
    subset_df = df[columns].iloc[i:j]

    for col in columns:
        plt.plot(subset_df.index, subset_df[col], label=col)
    
    plt.title('Data points visualised')
    plt.xlabel('Date')
    plt.ylabel(columns)
    plt.legend()
    plt.grid(True)
    
    save_name = input('Enter image name: ')
    plt.savefig(f'Meta_Plots/{save_name}.png')
    
    print("!!![WARNING]!!! Make sure data is scaled before using, entities such as volume are off scale compared to the others.")

    
if __name__ == "__main__":

    #testing load function
    mod = load_raw('NP_META_10y')
    featues=['High', 'Low', 'Close', 'Rolling', 'Volatility']
    plot(mod, featues, 0, 240)
    #save(mod, 'NP_META_10y')
    #print(mod)







