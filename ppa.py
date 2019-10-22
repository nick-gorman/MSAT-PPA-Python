import numpy as np
from datetime import timedelta


def calc_by_row(row, price_profile, residual_profiles):
    """
    Calaculate the PPA cost by calling the the calc function and selecting the required data from the scenario row.

    :param row: pandas dataframe, set of all variable for a scenario
    :param price_profile: pandas dataframe, the set of possible wholesale price profiles
    :param residual_profiles: pandas dataframe, the set of residual volume profiles
    :return: float
    """
    cost = calc(row['PPA'], row['PPA_Volume'], row['Wholesale_Exposure_Volume'], row['PPA_Price'],
                row['Excess_RE_Purchase_Price'], row['Excess_RE_Sale_Price'], row['LGC_Volume_Type'],
                row['LGC_Purchase_Volume'], row['LGC_Purchase_Price'], row['Load_MLF'], row['Load_DLF'],
                row['Generator_MLF'], row['Generator_DLF'], row['Target_Period'], row['Yearly_Target_MWh'],
                row['Yearly_Short_Fall_Penalty_MWh'], row['Yearly_LGC_target_LGC'],
                row['Yearly_LGC_short_fall_penalty_LGC'], row['Average_Wholesale_Price'],
                price_profile, residual_profiles)
    return cost


def calc(contract_type, ppa_volume, wholesale_volume, contract_price, excess_buy_price, excess_sell_price,
         lgc_volume_type, lgc_volume, lgc_price, load_mlf, load_dlf, gen_mlf, gen_dlf, penalty_period,
         yearly_target_volume_mwh, penalty_rate_mwh,
         yearly_target_volume_lgc, penalty_rate_lgc, average_wholesale_price, price_profile, residual_profiles):
    """
    Calculate the PPA costs by using the contract type to select the correct calculation method.

    :param lgc_price:
    :param lgc_volume:
    :param lgc_volume_type:
    :param contract_type: string, determines how the PPA costs are calculated should be one of,
                        'Off-site - Contract for Difference', 'Off-site - Tariff Pass Through',
                        'Off-site - Physical Hedge', 'On-site RE Generator' or 'No PPA'
    :param ppa_volume: string, determines how the volume traded through the PPA is calculated on a 30 min basis,
                      should be on of 'RE Uptill Load', 'All RE'
    :param wholesale_volume: string, determines how much volume is purchase at wholesale prices, should be one of
                            'All RE', 'RE Uptill Load', 'All Load' or 'None'
    :param contract_price: float, price paid for ppa volume
    :param excess_buy_price: float, price paid for excess re, only applies under 'On-site RE Generator'
    :param excess_sell_price: float, price excess sold at, only applies when wholesale exposure volume exceeds ppa volume
                             or when the contract type is 'On-site RE Generator'
    :param price_profile: pandas dataframe, the set of possible wholesale price profiles
    :param residual_profiles: pandas dataframe, the set of residual volume profiles
    :return: float
    """
    if contract_type == 'Off-site - Physical Hedge':
        x=1

    scaled_price_profile = price_profile * (average_wholesale_price / np.mean(price_profile))

    ppa_volume_profile = calc_ppa_volume_profile(ppa_volume, residual_profiles, contract_type)

    wholesale_volume_profile = calc_wholesale_volume_profile(wholesale_volume, residual_profiles)

    excess_to_sell = calc_excess_that_could_be_sold(contract_type, ppa_volume, residual_profiles)

    if contract_type in ppa_methods:
        ppa_cost = ppa_methods[contract_type](ppa_volume_profile, scaled_price_profile, contract_price, load_mlf,
                                              load_dlf)
    else:
        ppa_cost = 0.0

    if contract_type in excess_methods:
        excess_cost = excess_methods[contract_type](residual_profiles['Excess RE'], excess_buy_price)
    else:
        excess_cost = 0.0

    if contract_type in wholesale_purchase_methods:
        wholesale_cost = wholesale_purchase_methods[contract_type](wholesale_volume_profile, scaled_price_profile,
                                                                   load_mlf, load_dlf)
    else:
        wholesale_cost = 0.0

    if contract_type in wholesale_sale_methods:
        wholesale_payment = wholesale_sale_methods[contract_type](residual_profiles['RE Generator'],
                                                                  scaled_price_profile, gen_mlf, gen_dlf)
    else:
        wholesale_payment = 0.0

    if contract_type != 'No PPA':
        excess_payment = excess_sale_calc(excess_to_sell, excess_sell_price)
        penalty_payment_mwh = penalty_calc(residual_profiles, penalty_period, yearly_target_volume_mwh,
                                           penalty_rate_mwh)
        penalty_payment_lgc = penalty_calc(residual_profiles, 'Yearly', yearly_target_volume_lgc, penalty_rate_lgc)
        lgc_cost = lgc_cost_calc(lgc_volume_type, lgc_volume, lgc_price, residual_profiles)
    else:
        excess_payment = 0
        penalty_payment_lgc = 0
        penalty_payment_mwh = 0
        lgc_cost = 0

    cost = ppa_cost + wholesale_cost + excess_cost + lgc_cost - excess_payment - wholesale_payment - \
           penalty_payment_mwh - penalty_payment_lgc

    return cost / 1000


# Profile calc functions.


def calc_ppa_volume_profile(ppa_volume, residual_profiles, contract_type):
    if ppa_volume == 'RE Uptill Load' or contract_type == 'On-site RE Generator':
        volume_profile = residual_profiles['Used RE']
    else:
        volume_profile = residual_profiles['RE Generator']
    return volume_profile


def calc_wholesale_volume_profile(wholesale_volume, residual_profiles):
    if wholesale_volume == 'RE Uptill Load':
        volume_profile = residual_profiles['Used RE']
    elif wholesale_volume == 'All RE':
        volume_profile = residual_profiles['RE Generator']
    elif wholesale_volume == 'All Load':
        volume_profile = residual_profiles['Load']
    else:
        volume_profile = residual_profiles['Empty']
    return volume_profile


def calc_excess_that_could_be_sold(contract_type, ppa_volume, residual_profiles):
    if (contract_type in ['Off-site - Contract for Difference', 'Off-site - Tariff Pass Through'] and
            ppa_volume == 'All RE'):
        excess_to_sell = residual_profiles['Excess RE']
    elif contract_type in ['Off-site - Physical Hedge', 'On-site RE Generator']:
        excess_to_sell = residual_profiles['Excess RE']
    else:
        excess_to_sell = residual_profiles['Empty']
    return excess_to_sell


# PPA calc functions


def cfd_calc(ppa_volume_profile, price_profile, contract_price, mlf, dlf):
    cost = np.sum((contract_price - price_profile) * ppa_volume_profile)
    return cost


def flat_rate_calc(ppa_volume_profile, price_profile, contract_price, mlf, dlf):
    cost = np.sum(contract_price * ppa_volume_profile * mlf * dlf)
    return cost


def flat_rate_onsite_calc(ppa_volume_profile, price_profile, contract_price, mlf, dlf):
    cost = np.sum(contract_price * ppa_volume_profile)
    return cost


ppa_methods = {'Off-site - Contract for Difference': cfd_calc,
               'Off-site - Tariff Pass Through': flat_rate_calc,
               'On-site RE Generator': flat_rate_onsite_calc}


# Excess purchasing calc functions


def excess_purchase_calc(excess_profile, excess_purchase_price):
    cost = np.sum(excess_purchase_price * excess_profile)
    return cost


excess_methods = {'On-site RE Generator': excess_purchase_calc}


# Excess sale calc functions


def excess_sale_calc(excess_sale_profile, excess_sale_price):
    cost = np.sum(excess_sale_profile * excess_sale_price)
    return cost


# Wholesale purchasing calc functions


def wholesale(wholesale_volume_profile, price_profile, mlf, dlf):
    cost = np.sum(wholesale_volume_profile * price_profile * mlf * dlf)
    return cost


wholesale_purchase_methods = {'Off-site - Contract for Difference': wholesale,
                              'Off-site - Physical Hedge': wholesale}
wholesale_sale_methods = {'Off-site - Physical Hedge': wholesale}


# Penalty payment calculations


def penalty_calc(generator_profile, period, yearly_target_volume, penalty_rate):
    yearly_target_volume = yearly_target_volume * 1000
    if period == 'Yearly':
        target = yearly_target_volume
        payment = np.maximum((target - np.sum(generator_profile['RE Generator'].sum())), 0) * penalty_rate
    elif period == 'Quarterly':
        target = yearly_target_volume / 4
        payment = np.sum(np.maximum(target - generator_profile.groupby(generator_profile.DateTime.dt.quarter)[
            'RE Generator'].sum(), 0) * penalty_rate)
    elif period == 'Monthly':
        target = yearly_target_volume / 12
        payment = np.sum(np.maximum(target - generator_profile.groupby(generator_profile.dmt.dt.month)[
            'RE Generator'].sum(), 0) * penalty_rate)
    return payment


# LGC Purchase calculations


def lgc_cost_calc(volume_type, volume, price, residual_profiles):
    if volume_type == 'Frac RE':
        cost = residual_profiles['RE Generator'].sum() * volume * price
    elif volume_type == 'Frac Load':
        cost = residual_profiles['Load'].sum() * volume * price
    elif volume_type == 'RE Uptill load':
        cost = min(residual_profiles['RE Generator'].sum(), residual_profiles['Load'].sum()) * price
    elif volume_type == 'Fixed':
        cost = volume * price
    return cost
