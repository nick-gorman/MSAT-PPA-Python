import numpy as np
from datetime import datetime, time, timedelta


def calc_tou_set(tou_set, load_profiles, contract_type, wholesale_volume):
    """"
    Calculates the cost of retail tariffs taking into consideration the PPA contract type and wholesale exposure.

    :param tou_set: pandas dataframe with columns Charge Type, Volume Type, Rate, MLF, DLF, Start Month, End Month,
                    Start Weekday, End Weekday, Start Hour, End Hour
    :param load_profiles: pandas dataframe with columns DateTime, Load, RE Generator, Excess RE, Black, Used RE, Empty
    :param contract_type: string, should be 'Off-site - Contract for Difference', 'Off-site - Tariff Pass Through',
                          'Off-site - Physical Hedge', 'On-site RE Generator' or 'No PPA'
    :param wholesale_volume: string, should be 'All RE', 'RE Uptill Load', 'All Load', or 'None'
    :return tout_set_cost: this is the same as tou_set with the additional columns Cost and Alt Load ID
    """
    # Return a new version of the tou_set not a modified version.
    tou_set = tou_set.copy()

    # Determine the volume profile that each charge applies to.
    if (contract_type in ['Off-site - Contract for Difference', 'Off-site - Physical Hedge'] and
            wholesale_volume in ['All RE', 'RE Uptill Load']):
        tou_set['Alt Load ID'] = np.where(tou_set['Charge Type'] == 'Energy', 'Black', 'Load')
    elif (contract_type in ['Off-site - Contract for Difference', 'Off-site - Physical Hedge'] and
          wholesale_volume == 'All Load'):
        tou_set['Alt Load ID'] = np.where(tou_set['Charge Type'] == 'Energy', 'Empty', 'Load')
    elif contract_type == 'Off-site - Tariff Pass Through':
        tou_set['Alt Load ID'] = np.where(tou_set['Charge Type'] == 'Energy', 'Black', 'Load')
    elif contract_type == 'On-site RE Generator':
        tou_set['Alt Load ID'] = 'Black'
    else:
        tou_set['Alt Load ID'] = 'Load'

    # Apply the tou_calc function to the tou_set to find the cost of each charge.
    vector_tou_calc = np.vectorize(tou_calc, excluded=['load_profiles'])
    tou_set['Cost'] = vector_tou_calc(volume_type=tou_set['Volume Type'], rate=tou_set['Rate'], mlf=tou_set['MLF'],
                                      dlf=tou_set['DLF'], start_month=tou_set['Start Month'],
                                      end_month=tou_set['End Month'], start_weekday=tou_set['Start Weekday'],
                                      end_weekday=tou_set['End Weekday'], start_hour=tou_set['Start Hour'],
                                      end_hour=tou_set['End Hour'], load_profiles=load_profiles,
                                      load_id=tou_set['Alt Load ID'])

    return tou_set


def tou_calc(volume_type, rate, mlf, dlf, start_month, end_month, start_weekday, end_weekday, start_hour, end_hour,
             load_profiles, load_id):
    """
    Calculates the cost of tariff charges.

    :param volume_type: string, either 'Energy ($/MWh)' or 'Net RE Feed in Tariff ($/MWh)'
    :param rate: float, the cost per MWh for the tariff
    :param mlf: float, the marginal loss factor at the connection point acts a multiplier on the rate
    :param dlf: float, the marginal loss factor at the connection point acts a multiplier on the rate
    :param start_month: integer, when in the year the tariff starts applying, inclusive
    :param end_month: integer, when in the year the tariff starts applying, inclusive
    :param start_weekday: integer, when in the week the tariff starts applying, inclusive, monday is 1
    :param end_weekday: integer, when in the week the tariff starts applying, inclusive
    :param start_hour: integer, when in the day the tariff starts applying, inclusive, to do whole day start with 0.
           When start_hour comes after end_hour then the tariff applies before end_hour and after start_hour.
    :param end_hour: integer, when in the day the tariff starts applying, inclusive, to do whole day end with 23
    :param load_profiles: pandas dataframe, 'DateTime' column as type timestamp, 'Energy' column as type float
    :param load_id: string, the column to use from the load_profiles dataframe
    :return cost: float, in dollars for whole load profile

    """

    load_profiles['dmt'] = load_profiles.DateTime - timedelta(minutes=15)

    trimmed_load_profile = load_profiles[(load_profiles.dmt.dt.month >= start_month) &
                                         (load_profiles.dmt.dt.month <= end_month) &
                                         (load_profiles.dmt.dt.dayofweek + 1 >= start_weekday) &
                                         (load_profiles.dmt.dt.dayofweek + 1 <= end_weekday) &
                                         (((load_profiles.DateTime.dt.time > time(hour=start_hour)) &
                                           (load_profiles.DateTime.dt.time <= time(hour=end_hour))) |
                                          ((start_hour > end_hour) &
                                           ((load_profiles.DateTime.dt.time > time(hour=start_hour)) |
                                            (load_profiles.DateTime.dt.time <= time(hour=end_hour)))))]

    energy_in_mwh = trimmed_load_profile[load_id].sum() / 1000

    cost = energy_in_mwh * rate * mlf * dlf
    print('hit')
    return cost
