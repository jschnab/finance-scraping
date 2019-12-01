#!/usr/bin/python3

# script which calculates the rate of return per company


def get_annual_srr(df, company_names="name", closing_value="lastquote"):
    """
    Returns the annual simple rate of return from a dataframe.

    :param pd.DataFrame df: a dataframe containing stock market data
    :param str company_names: name of the column containing company names,
                              optional (defaults to 'name')
    :param str closing_value: name of the column containing stock market
                              closing values, optional (defaults to
                              'lastquote')
    :param bool sort_ascending: whether to sort values by ascending order,
                                optional (defaults to False)
    :returns pd.Series: series containing annualized simple rate of return
    """
    # there are several values per day, we would like to keep the last
    no_dups = df.reset_index().groupby(["name", "timestamp"]).last()

    # we calculate the simple rate of return per company
    no_dups["srr"] = (
        no_dups["lastquote"] / no_dups.groupby("name")["lastquote"].shift(1)
    ) - 1

    # we calculate the annualized simple rate of return
    annual_srr = (
        no_dups.reset_index().groupby("name")["srr"].mean() * 250
    ).sort_values(ascending=False)

    return annual_srr
