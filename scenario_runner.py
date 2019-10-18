import pandas as pd
import residuals
import tariffs


def run_scenario_from_row(scenario_row, load_profiles, charge_set):
    """
    Calculate retail and ppa costs for a given row in the scenario table

    :param scenario_row: pandas DataFrame row with following columns 'PPA', 'Wholesale_Price_ID',
           'Average_Wholesale_Price', 'Wholesale_Exposure_Volume', 'Load_ID', 'Generator_ID', 'PPA_Volume',
           'PPA_Price', 'Excess_RE_Purchase_Price', 'Excess_RE_Sale_Price', 'LGC_Volume_Type', 'LGC_Purhcase_Volume',
           'LGC_Purchase_Price', 'Yearly_Target_MWh', 'Target_Period', 'Yearly_Short_Fall_Penalty_MWh',
           'Yearly_LGC_target_LGC', 'Yearly_LGC_short_fall_penalty_LGC', 'Load_MLF', 'Load_DLF', 'Generator_MLF',
           'Generator_DLF', 'TOU_1', 'TOU_2', 'TOU_3', 'TOU_4', 'TOU_5', 'TOU_6', 'TOU_7', 'TOU_8', 'TOU_9', 'TOU_10',
           'Flat_1', 'Flat_2', 'Flat_3', 'Flat_4', 'Flat_5', 'Flat_6', 'Flat_7', 'Flat_8'
    :param load_profiles: The set of possible load profiles
    :param charge_set: The set of retail charge details
    :return: retail_cost: float
    """

    load_id = scenario_row['Load_ID']
    generator_id = scenario_row['Generator_ID']
    load_profiles['DateTime'] = pd.to_datetime(load_profiles["DateTime"])
    load_profiles[load_id] = pd.to_numeric(load_profiles[load_id])
    load_profiles[generator_id] = pd.to_numeric(load_profiles[generator_id])
    residual_profiles = residuals.calc(load_profiles=load_profiles, load_id=load_id, generator_id=generator_id)
    costs = tariffs.calc_tou_set(tou_set=charge_set, load_profiles=residual_profiles, contract_type=scenario_row['PPA'],
                                 wholesale_volume=scenario_row['Wholesale_Exposure_Volume'])
    retail_cost = costs['Cost'].sum()
    return retail_cost
