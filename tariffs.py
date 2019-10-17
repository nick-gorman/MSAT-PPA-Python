

def tou_calc(volume_type, rate, mlf, dlf, start_month, end_month, start_weekday, end_weekday, start_hour, end_hour,
         load_profile):
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
    :param start_hour: integer, when in the day the tariff starts applying, inclusive, to do whole day start with 0
    :param end_hour: integer, when in the day the tariff starts applying, inclusive, to do whole day end with 23
    :param load_profile: pandas dataframe, 'Datetime' column as type timestamp, 'Energy' column as type float
    :return cost: float, in dollars for whole load profile

    """

    trimmed_load_profile = load_profile[(load_profile.DateTime.dt.month >= start_month) &
                                        (load_profile.DateTime.dt.month <= end_month) &
                                        (load_profile.DateTime.dt.dayofweek + 1 <= start_weekday) &
                                        (load_profile.DateTime.dt.dayofweek + 1 >= end_weekday) &
                                        (((load_profile.DateTime.dt.hour + 1 <= start_hour) &
                                        (load_profile.DateTime.dt.hour + 1 >= end_hour)) |
                                        ((start_hour > end_hour) &
                                        ((load_profile.DateTime.dt.hour + 1 >= start_hour) |
                                        (load_profile.DateTime.dt.hour + 1 <= end_hour))))]

    energy_in_mwh = trimmed_load_profile.Energy.sum()/1000

    cost = energy_in_mwh * rate * mlf * dlf

    return cost
