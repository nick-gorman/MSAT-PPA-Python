import pandas as pd
import numpy as np


def calc(load_profiles, load_id, generator_id):
    """
    'This function takes the full set of load profiles and uses the nominated load and generator profiles to
    calculate the residual profiles.'

    :param load_profiles: pandas dataframe, the full set of input profiles defined, only fixed column name is DateTime
    :param load_id: string, the name of the column in load_profiles to treat as the load
    :param generator_id: string, the name of the column in load_profiles to treat as the RE generator
    :return: residual_profiles: pandas dataframe, with column DateTime, Load, RE Generator, Black, Excess RE, Used RE
    """
    residual_profiles = pd.DataFrame()
    residual_profiles['DateTime'] = load_profiles['DateTime']
    residual_profiles['Load'] = load_profiles[load_id]
    residual_profiles['RE Generator'] = load_profiles[generator_id]
    residual_profiles['Black'] = np.maximum(residual_profiles['Load'] - residual_profiles['RE Generator'], 0)
    residual_profiles['Excess RE'] = np.maximum(residual_profiles['RE Generator'] - residual_profiles['Load'], 0)
    residual_profiles['Used RE'] = residual_profiles['RE Generator'] - residual_profiles['Excess RE']
    return residual_profiles