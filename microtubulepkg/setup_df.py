import pandas as pd

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