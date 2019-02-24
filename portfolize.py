import numpy as np
import pandas as pd
from statsmodels.tsa.ar_model import AR
from statsmodels.tsa.ar_model import ARResults
from sklearn.metrics import mean_squared_error

ST_SPX, LT_SPX = 1, 0.9
ST_RUT, LT_RUT = 0.47, 0.81
ST_SPAB, LT_SPAB = 0.59, 1.09
ST_GSCI, LT_GSCI = -0.1, -0.19
ST_JNK, LT_JNK = 0.41, 1.01
ST_EMB, LT_EMB = 0.74, 1.02
ST_EFA, LT_EFA = 0.21, 0.54
ST_DWRSF, LT_DWRSF = 0.4, 0.5
ST_SBERWUU, LT_SBERWUU = 0.37, 0.71
ST_SPBMGPPU, LT_SPBMGPPU = 0.3, 0.4

SPX_FILE_PATH = 'C:\\Users\\ms980\\Documents\\projects\\portfolize\\portfoliodata\\spx.csv'
RUT_FILE_PATH = 'C:\\Users\\ms980\\Documents\\projects\\portfolize\\portfoliodata\\rutnu.csv'
SPAB_FILE_PATH = 'C:\\Users\\ms980\\Documents\\projects\\portfolize\\portfoliodata\\spab.csv'
GSCI_FILE_PATH = 'C:\\Users\\ms980\\Documents\\projects\\portfolize\\portfoliodata\\spgsci.csv'
JNK_FILE_PATH = 'C:\\Users\\ms980\\Documents\\projects\\portfolize\\portfoliodata\\jnk.csv'
EMB_FILE_PATH = 'C:\\Users\\ms980\\Documents\\projects\\portfolize\\portfoliodata\\emb.csv'
EFA_FILE_PATH = 'C:\\Users\\ms980\\Documents\\projects\\portfolize\\portfoliodata\\efa.csv'
DWRSF_FILE_PATH = 'C:\\Users\\ms980\\Documents\\projects\\portfolize\\portfoliodata\\dwrsf.csv'
SBERWUU_FILE_PATH = 'C:\\Users\\ms980\\Documents\\projects\\portfolize\\portfoliodata\\sberwuu.csv'
SPBMGPPU_FILE_PATH = 'C:\\Users\\ms980\\Documents\\projects\\portfolize\\portfoliodata\\spbmgppu.csv'



#main function
def run(budget, term, high_risk):
    portfolio = portfolio_list(budget)
    print(portfolio)
    instrument_list = []
    cardinal_list = []
    prop_list = []
    total_sum = 0

    for i in portfolio:
        filename = i
        adjusted_inc = 0
        instrument_name = get_instrument(filename)
        dateparse = lambda dates: pd.datetime.strptime(dates, '%m/%d/%Y')
        df = pd.read_csv(filename, parse_dates=['date'], index_col='date', date_parser=dateparse, header=0)

        increase = percent_inc(df, term)
        if increase < 0:
            adjusted_inc=0
        elif high_risk:
            adjusted_inc += increase
        else:
            adjusted_inc += sharpe_ratio_multiplier(filename, term, increase)

        total_sum += adjusted_inc
        instrument_list.append(instrument_name)
        cardinal_list.append(adjusted_inc)

    for e in cardinal_list:
        num = e / total_sum
        prop_list.append(num)

    return instrument_list, prop_list


#determines user's list of investment options
def portfolio_list(budget):
    if budget <= 100000:
        return [SPX_FILE_PATH, SPAB_FILE_PATH, RUT_FILE_PATH, GSCI_FILE_PATH, JNK_FILE_PATH]
    elif budget > 100000 and budget <= 1000000:
        return [SPX_FILE_PATH, SPAB_FILE_PATH, RUT_FILE_PATH, GSCI_FILE_PATH, JNK_FILE_PATH, EMB_FILE_PATH, EFA_FILE_PATH, DWRSF_FILE_PATH]
    elif budget > 1000000:
        return [SPX_FILE_PATH, SPAB_FILE_PATH, RUT_FILE_PATH, GSCI_FILE_PATH, JNK_FILE_PATH, EMB_FILE_PATH, EFA_FILE_PATH, DWRSF_FILE_PATH,
                     SPBMGPPU_FILE_PATH, SBERWUU_FILE_PATH]

#predicts next element on list based on current
def pred(estimator, record):
    estimate = estimator[0]
    for a in range(1, len(estimator)):
        estimate += estimator[a] * record[-a]
    return estimate

#calculates change in value from last element in list
def delta(df):
    delt = list()
    for a in range(1, len(df)):
        new = df[a] - df[a-1]
        delt.append(new)
    return np.array(delt)

#predicts the estimate price at given time and dataset
def tsregress(df, window_size):
    D = delta(df.values)
    length = int(len(D) * 0.8)
    feed = D[0:length]
    test = D[length:]

    ts = AR(feed)
    ts_fit = ts.fit(maxlag=window_size, disp=False)
    lagwindow, estmr = ts_fit.k_ar, ts_fit.params

    record = [feed[a] for a in range(len(feed))]
    predictions = list()
    for t in range(len(test)):
        estimate = pred(estmr, record)
        obs = test[t]
        predictions.append(obs)

    ts_fit.save('ts.pkl')
    np.save('data.npy', D)
    np.save('obs.npy', df.values[-1])

    ts_load = ARResults.load('ts.pkl')
    data = np.load('data.npy')
    last = np.load('obs.npy')

    extrapolation = ts_load.predict(start=window_size, end=len(data))

    output = extrapolation[0] + last[0]

    return output

def get_instrument(filename):
    if filename is SPX_FILE_PATH:
        return 'S&P 500 Index Funds'
    elif filename is RUT_FILE_PATH:
        return 'Russell 2000 Small Cap'
    elif filename is SPAB_FILE_PATH:
        return 'US Aggregate Bonds'
    elif filename is GSCI_FILE_PATH:
        return 'Commodities'
    elif filename is JNK_FILE_PATH:
        return 'Corporate High Yield Bonds'
    elif filename is EMB_FILE_PATH:
        return 'US Emerging Market Bonds'
    elif filename is EFA_FILE_PATH:
        return 'International Equity'
    elif filename is DWRSF_FILE_PATH:
        return 'US Real Estate'
    elif filename is SPBMGPPU_FILE_PATH:
        return 'International Real Estate'
    elif filename is SBERWUU_FILE_PATH:
        return 'International Small Cap Equity'


#calculates percentage increase
def percent_inc(df, window_size):
    percent = 0
    beginning = df.iloc[len(df)-1]['price']
    end = tsregress(df, window_size)
    percent = (end - beginning) / (beginning) * 100
    return percent

#risk adjustment
def sharpe_ratio_multiplier(filename, term, increase):
    return_value = 0
    if filename is SPX_FILE_PATH:
        if term < 101:
            return_value += increase * ST_SPX
        else:
            return_value += increase * LT_SPX
    if filename is RUT_FILE_PATH:
        if term < 101:
            return_value += increase * ST_RUT
        else:
            return_value += increase * LT_RUT
    if filename is SPAB_FILE_PATH:
        if term < 101:
            return_value += increase * ST_SPAB
        else:
            return_value += increase * LT_SPAB
    if filename is GSCI_FILE_PATH:
        if term < 101:
            return_value += increase * ST_GSCI
        else:
            return_value += increase * LT_GSCI
    if filename is JNK_FILE_PATH:
        if term < 101:
            return_value += increase * ST_JNK
        else:
            return_value += increase * LT_JNK
    if filename is EMB_FILE_PATH:
        if term < 101:
            return_value += increase * ST_EMB
        else:
            return_value += increase * LT_EMB
    if filename is EFA_FILE_PATH:
        if term < 101:
            return_value += increase * ST_EFA
        else:
            return_value += increase * LT_EFA
    if filename is DWRSF_FILE_PATH:
        if term < 101:
            return_value += increase * ST_DWRSF
        else:
            return_value += increase * LT_DWRSF
    if filename is SPBMGPPU_FILE_PATH:
        if term < 101:
            return_value += increase * ST_SPBMGPPU
        else:
            return_value += increase * LT_SPBMGPPU
    if filename is SBERWUU_FILE_PATH:
        if term < 101:
            return_value += increase * ST_SBERWUU
        else:
            return_value += increase * LT_SBERWUU
    return return_value
