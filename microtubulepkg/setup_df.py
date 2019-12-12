import pandas as pd
from .modeling import gamma_mle

def setup(path, col_names):
    '''
    Inputs: path name, column titles (concentrations)
    Output: tidy dataframe containing sorted times to catastrophe
    '''
    tubulin_df = pd.read_csv(path, skiprows=9)
    tubulin_df = tubulin_df[col_names]

    tub_df=tubulin_df.melt()
    tub_df.columns=['concentration','catastrophe time']
    tub_df=tub_df.dropna()
    conc_ints = []
    tub_df.reset_index(inplace=True)
    for k in range(len(tub_df["concentration"])):
        conc_ints.append(int(tub_df["concentration"][k][:-3]))
        
    tub_df["concentration (int)"]=conc_ints
    return tub_df

def setup_mle_data(tub_df):
    mle_data = pd.DataFrame(index=list(range(0,5)), columns = ["molarity (uM)", "alpha MLE", "beta MLE"])
    mle_data["molarity (uM)"] = [7, 9, 10, 12, 14]

    alpha_mle_list = []
    beta_mle_list = []
    for k in range(len(mle_data)):
        alpha_mle, beta_mle = gamma_mle((tub_df.loc[tub_df["concentration (int)"] == mle_data["molarity (uM)"][k]])["catastrophe time"].values)
        alpha_mle_list.append(alpha_mle)
        beta_mle_list.append(beta_mle)
    mle_data["alpha MLE"] = alpha_mle_list
    mle_data["beta MLE"] = beta_mle_list
    return mle_data