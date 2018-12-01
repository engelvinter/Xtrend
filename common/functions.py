from configparser import ConfigParser


def above_ma(nbr_days, ts):
    ma = ts[-nbr_days:].mean()
    return ts[-1] > ma


def read_fund_groups(full_path):
    """
    Reads groups from an ini-file.
    Each section is the group name together with a list of funds belonging to
    the group.

    For Example:
    [Gold]
    Blackrock Gold Fund
    Xenia Fund
    Gold ETF A

    Parameters
    ----------
    `full_path` : the input full path name

    Returns
    -------
    fund names as keys and group names as values
    """
    config = ConfigParser(allow_no_value=True)
    config.optionxform = str
    config.read(full_path)
    fund_config = {}
    for section in config.sections():
        d = {item[0]: section for item in config.items(section)}
        fund_config.update(d)
    return fund_config