# from canalyst_candas.configuration.config import Config
# from canalyst_candas.settings import CONFIG

# from configuration.config import resolve_config
# from utils import calendar_quarter, df_filter
import yahoo_fin.stock_info as si
import pandas as pd
import numpy as np
import statsmodels.tsa.stattools as ts
import statsmodels.api as sm

from fredapi import Fred
import pandas as pd
import json

import os
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from urllib.request import urlopen, Request

# from nltk.sentiment.vader import SentimentIntensityAnalyzer

web_url = "https://finviz.com/quote.ashx?t="


def get_news_sentiment(ticker_list):
    news_tables = {}

    for tick in ticker_list:
        print(tick)
        url = web_url + tick
        req = Request(url=url, headers={"User-Agent": "Chrome"})
        try:
            response = urlopen(req)
        except:
            continue
        html = BeautifulSoup(response, "html.parser")
        news_table = html.find(id="news-table")
        news_tables[tick] = news_table

    news_list = []

    for file_name, news_table in news_tables.items():
        for i in news_table.findAll("tr"):

            text = i.a.get_text()

            date_scrape = i.td.text.split()

            if len(date_scrape) == 1:
                time = date_scrape[0]

            else:
                date = date_scrape[0]
                time = date_scrape[1]

            tick = file_name.split("_")[0]

            news_list.append([tick, date, time, text])

    vader = SentimentIntensityAnalyzer()

    columns = ["ticker", "date", "time", "headline"]

    news_df = pd.DataFrame(news_list, columns=columns)

    scores = news_df["headline"].apply(vader.polarity_scores).tolist()

    scores_df = pd.DataFrame(scores)

    news_df = news_df.join(scores_df, rsuffix="_right")

    news_df["date"] = pd.to_datetime(news_df.date).dt.date

    return news_df


def get_betas_wide(betas_list):
    list_df = []
    for item in betas_list:

        df = get_price_data(item)
        list_df.append(df)

    df_long = pd.concat(list_df, axis=0).reset_index()
    df_wide = df_long.pivot_table(
        index=["index"], columns="ticker", values="pct_change"
    )
    return df_wide


def get_parallel_betas_from_list(ticker_list, betas_list):
    df_wide = get_betas_wide(betas_list)
    from joblib import Parallel, delayed
    import multiprocessing

    inputs = range(10)

    def processInput(i):
        return i * i

    num_cores = multiprocessing.cpu_count()
    all_df = Parallel(n_jobs=num_cores)(
        delayed(get_beta_data)(ticker, df_wide, betas_list) for ticker in ticker_list
    )
    df_betas = pd.concat(all_df)
    return df_betas


def get_beta_data(ticker, df_wide, betas_list):
    list_out = []
    print(ticker)
    try:
        df = get_price_data(ticker).reset_index()
    except:
        print("failed")
        return

    dataset = pd.merge(df, df_wide, how="inner", left_on="index", right_on="index")

    beta_lens = [60, 90, 252]  # window for betas
    dict_lens = {}
    for beta_len in beta_lens:
        betas = {}
        ns = {}
        r2s = {}
        for col in dataset.columns:
            if col in betas_list:

                df = dataset[["pct_change", col]].dropna()
                # try:
                beta, r2, n = get_betas(df["pct_change"], df[col], beta_len)
                # except:
                #    print("get_betas error")
                #    return
                betas[col] = beta
                ns[col] = n
                r2s[col] = r2
        dict_lens[beta_len] = [betas, ns, r2s]

        df1 = pd.DataFrame.from_dict(
            dict_lens[beta_len][2], orient="index"
        ).reset_index()

        try:
            df1.columns = ["BETA", ticker]
        except:
            print("df columns error")
            return
        df1 = df1.T
        headers = df1.iloc[0]
        df1 = pd.DataFrame(df1.values[1:], columns=headers)
        df1["ticker"] = ticker
        df1["beta_days"] = beta_len
        list_out.append(df1)
    df = pd.concat(list_out)
    return df


def get_price_data(ticker, reset=False, rolling_betas=True, rolling_window=60):
    price_data = si.get_data(ticker, start_date="01/01/2009")
    df = pd.DataFrame(price_data)
    df = df[["adjclose"]]
    df["pct_change"] = df.adjclose.pct_change()
    df["log_return"] = np.log(1 + df["pct_change"].astype(float))
    df["ticker"] = ticker
    if reset == True:
        df = df.reset_index()
        df["price_date"] = df["index"]
        df = df.drop(columns=["index"])
    if rolling_betas == True:
        beta = "beta_" + str(rolling_window)
        df["adjclose_plus_5"] = df["adjclose"].shift(-5)
        df["adjclose_plus_10"] = df["adjclose"].shift(-10)

        sp_ticker = "^GSPC"
        sp_data = si.get_data(sp_ticker, start_date="01/01/2009")
        df_sp = pd.DataFrame(sp_data)
        df_sp = df_sp[["adjclose"]]
        df_sp["pct_change"] = df_sp.adjclose.pct_change()
        df_sp["log_return"] = np.log(1 + df_sp["pct_change"].astype(float))
        df_sp["ticker"] = ticker
        df_sp["mkt_change"] = df_sp["pct_change"]
        df_sp = df_sp.reset_index()
        df_sp["price_date"] = df_sp["index"]
        df_sp = df_sp.drop(columns=["index"])
        df_sp["mktclose"] = df_sp["adjclose"]
        df_sp["mkt_plus_5"] = df_sp["mktclose"].shift(-5)
        df_sp["mkt_plus_10"] = df_sp["mktclose"].shift(-10)
        df = pd.merge(
            df,
            df_sp[
                [
                    "ticker",
                    "price_date",
                    "mkt_change",
                    "mktclose",
                    "mkt_plus_5",
                    "mkt_plus_10",
                ]
            ],
        )

        from statsmodels.regression.rolling import RollingOLS

        model = RollingOLS.from_formula(
            "pct_change ~ mkt_change",
            data=df[["pct_change", "mkt_change"]],
            window=rolling_window,
        )
        rres = model.fit()
        df[beta] = rres.params[["mkt_change"]]

        df["plus_5_return"] = df["adjclose_plus_5"] / df["adjclose"] - 1
        df["plus_10_return"] = df["adjclose_plus_10"] / df["adjclose"] - 1
        df["mktclose_plus_5_return"] = df["mkt_plus_5"] / df["mktclose"] - 1
        df["mktclose_plus_10_return"] = df["mkt_plus_10"] / df["mktclose"] - 1
        df["expected_5_day_return"] = df[beta] * df["mktclose_plus_5_return"]
        df["expected_10_day_return"] = df[beta] * df["mktclose_plus_10_return"]
        df["alpha_5_day"] = df["plus_5_return"] - df["expected_5_day_return"]
        df["alpha_10_day"] = df["plus_10_return"] - df["expected_10_day_return"]

    return df


def get_betas(x, y, n=0):
    if n > 0:
        x = x.iloc[
            -n:,
        ]
        y = y.iloc[
            -n:,
        ]
    res = sm.OLS(y, x).fit()
    beta = res.params[0]
    r2 = res.rsquared
    n = len(x)
    return [beta, r2, n]


def get_fred_data(series_list, config):

    end_date = datetime.today().strftime("%Y-%m-%d")
    FRED = Fred(config.fred_key)  # Fred(config.fred_key)

    df_fred = pd.DataFrame()
    for fred_series in series_list:
        s = pd.DataFrame(
            FRED.get_series(
                fred_series, observation_start="2014-09-02", observation_end=end_date
            )
        ).reset_index()
        s.columns = ["end_date", fred_series]
        s = calendar_quarter(s, "end_date")
        s = s.groupby("end_date_CALENDAR_QUARTER").last().reset_index()
        if df_fred.shape[0] > 0:
            s = s.drop(columns="end_date")
            df_fred = pd.merge(
                df_fred,
                s,
                how="inner",
                left_on="end_date_CALENDAR_QUARTER",
                right_on="end_date_CALENDAR_QUARTER",
            )
        else:
            df_fred = s
    return df_fred


def append_price_data(df):

    df = calendar_quarter(df, "end_date")

    pd.set_option("mode.chained_assignment", None)
    ticker = df.iloc[0]["ticker"]
    stock_ticker = ticker.split(" ")[0]
    df_prices = get_price_data(stock_ticker)
    df_prices = df_prices.reset_index()
    df_prices = df_prices[["pricing_date", "adjclose"]]
    df_prices.columns = ["end_date", "adjclose"]

    df_prices = calendar_quarter(df_prices, "end_date")
    df_prices = df_prices.sort_values("end_date")
    df_prices = df_prices.groupby("end_date_CALENDAR_QUARTER").last().reset_index()

    # fiscal_quarter
    df = df_filter(df, "period_duration_type", ["fiscal_quarter"])
    dates = list(set(list(df["end_date_CALENDAR_QUARTER"])))
    df_p = df_filter(df_prices, "end_date_CALENDAR_QUARTER", dates)

    df_p.columns = ["end_date_CALENDAR_QUARTER", "end_date", "value"]
    df_p["ticker"] = ticker
    df_p["period"] = ""
    df_p["period_duration_type"] = "fiscal_quarter"
    df_p["category"] = ""
    df_p["type"] = ""
    df_p["row_header"] = "Stock Price"
    df_p["unit"] = "$"
    df_p = df_p.sort_values("end_date")
    df_1 = df_p[
        [
            "ticker",
            "period",
            "period_duration_type",
            "end_date",
            "category",
            "type",
            "row_header",
            "unit",
            "value",
            "end_date_CALENDAR_QUARTER",
        ]
    ]

    df = pd.concat([df, df_1])

    return df


def calendar_quarter(df, col, datetime=True):
    pd.set_option("mode.chained_assignment", None)
    # translate a date into sort-able and group-able YYYY-mm format.
    df[col] = pd.to_datetime(df[col])

    df[col + "shift"] = df[col] + pd.Timedelta(days=-12)

    df[col + "_CALENDAR_QUARTER"] = df[col + "shift"].dt.to_period("Q")

    df = df.drop(columns=[col + "shift"])
    df[col + "_CALENDAR_QUARTER"] = df[col + "_CALENDAR_QUARTER"].astype(str)

    return df


def get_earnings_dates(ticker):
    df = pd.DataFrame.from_dict(si.get_earnings_history(ticker))
    df["earnings_date"] = df["startdatetime"].astype(str)
    df["earnings_date"] = df["earnings_date"].str.split("T").str[0]
    df["earnings_date"] = pd.to_datetime(df["earnings_date"])
    df = df.dropna()

    return df[
        [
            "ticker",
            "companyshortname",
            "earnings_date",
            "epsestimate",
            "epsactual",
            "epssurprisepct",
        ]
    ]


def regress_dataframe(df, y_col, x_col, y_filter):
    import datetime as ddt
    import statsmodels.api as ssm

    if y_filter != "":
        df = df.loc[df[y_col] == y_filter]

    X = df.head(24)[x_col]
    Y = df.head(24)[y_col]

    X = ssm.add_constant(X)  # to add constant value in the model
    ols_model = ssm.OLS(Y.astype(float), X.astype(float)).fit()  # fitting the model
    predictions = ols_model.summary()  # summary of the model
    return predictions


def get_earnings_and_prices(ticker):
    df_earnings = get_earnings_dates(ticker)
    df_prices = get_price_data(
        ticker, reset=True, rolling_betas=True, rolling_window=252
    )
    df = pd.merge(
        df_prices,
        df_earnings,
        how="inner",
        left_on=["ticker", "price_date"],
        right_on=["ticker", "earnings_date"],
    )
    beta = "beta_60"
    if "beta_60" not in df.columns:
        for col in df.columns:
            if "beta" in col:
                beta = col
    df = df[
        [
            "ticker",
            "companyshortname",
            "price_date",
            "earnings_date",
            "epsestimate",
            "epsactual",
            "epssurprisepct",
            "alpha_5_day",
            "alpha_10_day",
            beta,
            "plus_5_return",
            "plus_10_return",
            "mktclose_plus_5_return",
            "mktclose_plus_10_return",
        ]
    ].sort_values("earnings_date", ascending=False)

    return df


def regress_dataframe_groups(
    df_data, y_name="alpha_10_day", return_grouped=True, n_periods=12
):

    import statsmodels.api as ssm
    import numpy as np

    # return df_data
    df_data = df_data[df_data[y_name].notna()]
    df_data = df_data[df_data["value"].notna()]

    def extract_lr(x, y_name):
        Y = x[y_name].astype(float).tail(n_periods)
        y_len = Y.shape[0]

        X = x[["value"]].tail(n_periods)

        X = ssm.add_constant(X)
        X = X.astype(float)

        model = ssm.OLS(Y, X).fit()
        preds = model.predict(X)

        x["preds"] = preds
        x["rsquared"] = model.rsquared

        return pd.DataFrame(x)

    grouped = df_data.groupby("time_series_name")  # group by each time series name
    grouped = grouped.apply(
        lambda x: extract_lr(x, "alpha_10_day")
    )  # apply the model to the dataframe groups
    if return_grouped == True:
        df_output = (
            grouped.reset_index()
            .groupby(["time_series_name", "category"])
            .mean()
            .reset_index()
            .sort_values("rsquared", ascending=False)
        )
        return df_output[
            [
                "name_index",
                "time_series_description",
                "time_series_name",
                "category",
                "rsquared",
            ]
        ]
    else:
        return grouped


def format_borders(plot, colors):
    plot.spines["top"].set_visible(False)
    plot.spines["left"].set_visible(False)
    plot.spines["left"].set_color(colors["grey"])
    plot.spines["bottom"].set_color(colors["grey"])


def plot_prices_against_time_series(
    df_data, df_prices, time_series_name, value_name="value"
):
    ticker = df_data.iloc[0]["ticker"]
    df_filter = df_data.loc[df_data["time_series_name"] == time_series_name]
    df_plot = pd.merge(
        df_prices[["adjclose", "price_date"]],
        df_filter[["time_series_name", "earnings_date", value_name]],
        how="outer",
        left_on="price_date",
        right_on="earnings_date",
    )
    df_plot = df_plot.loc[df_plot["price_date"] > "2020-01-01"]
    import matplotlib.pyplot as plt

    df_plot["row_num"] = np.arange(len(df_plot))
    markers_on = df_plot.dropna()

    markers_on = list(markers_on["row_num"])

    colors = {
        "red": "#ff207c",
        "grey": "#42535b",
        "blue": "#207cff",
        "orange": "#ffa320",
        "green": "#00ec8b",
    }
    plt.rc("figure", figsize=(10, 7))

    config_ticks = {"size": 14, "color": colors["grey"], "labelcolor": colors["grey"]}
    config_title = {"size": 18, "color": colors["grey"], "ha": "left", "va": "baseline"}

    fig, axes = plt.subplots(2, 1, gridspec_kw={"height_ratios": [3, 1]})
    fig.tight_layout(pad=3)

    date = df_plot["price_date"]
    close = df_plot["adjclose"]
    vol = df_plot[value_name]

    plot_price = axes[0]
    plot_price.plot(
        date,
        close,
        color=colors["blue"],
        linewidth=2,
        label="Price",
        marker="*",
        ms=10,
        markevery=markers_on,
        markerfacecolor="black",
    )

    plot_vol = axes[1]
    plot_vol.bar(date, vol, width=15, color="darkgrey")
    plot_vol.set_ylabel(time_series_name, fontsize=14)
    plot_vol.yaxis.set_label_position("left")
    plot_vol.yaxis.label.set_color(colors["grey"])

    plot_price.yaxis.tick_right()
    plot_price.tick_params(axis="both", **config_ticks)
    plot_price.set_ylabel("Price (in USD)", fontsize=14)
    plot_price.yaxis.set_label_position("right")
    plot_price.yaxis.label.set_color(colors["grey"])
    plot_price.grid(axis="y", color="gainsboro", linestyle="-", linewidth=0.5)
    plot_price.set_axisbelow(True)

    format_borders(plot_price, colors)
    format_borders(plot_vol, colors)

    return  # plt.show()


def plot_eps_surprise_data(df):
    import matplotlib.pyplot as plt

    df["z_score_alpha_10_day"] = (df["alpha_10_day"] - df["alpha_10_day"].mean()) / df[
        "alpha_10_day"
    ].std(ddof=0)
    df["z_score_epssurprisepct"] = (
        df["epssurprisepct"] - df["epssurprisepct"].mean()
    ) / df["epssurprisepct"].std(ddof=0)

    df_plot = df

    colors = {
        "red": "#ff207c",
        "grey": "#1d2224",
        "blue": "#207cff",
        "orange": "#ffa320",
        "green": "#00ec8b",
    }
    plt.rc("figure", figsize=(10, 7))

    config_ticks = {"size": 14, "color": colors["grey"], "labelcolor": colors["grey"]}
    config_title = {"size": 18, "color": colors["grey"], "ha": "left", "va": "baseline"}

    # fig, axes = plt#.subplots(, 1, gridspec_kw={"height_ratios": [1, 1]})
    plt.tight_layout(pad=3)

    date = df["price_date"]
    close = df["z_score_alpha_10_day"]
    vol = df_plot["z_score_epssurprisepct"]

    plt.scatter(date, close, color=colors["blue"], label="Alpha 10 Days")

    plt.scatter(date, vol, color="black", label="Eps Surprise")

    plt.gca().yaxis.tick_right()
    plt.gca().tick_params(axis="both", **config_ticks)
    plt.gca().set_ylabel("Standard Deviation", fontsize=14)
    plt.gca().yaxis.set_label_position("right")
    plt.grid(axis="y", color="gainsboro", linestyle="-", linewidth=0.5)
    plt.legend(loc="upper left")
    format_borders(plt.gca(), colors)

    return


def regress_dataframe_time_series_groups(
    df_data=None, y_name="", return_grouped=True, n_periods=16
):
    ticker = df_data.iloc[0]["ticker"]
    import canalyst_candas.candas_datareader as cdr

    df = regress_dataframe_groups(
        df_data, y_name=y_name, return_grouped=return_grouped, n_periods=n_periods
    )

    df["ticker"] = ticker
    df["model_row_number"] = df["model_row_number"].astype(int)
    col_name = "ticker"
    first_col = df.pop(col_name)
    df.insert(0, col_name, first_col)

    return df


def regress_dataframe_groups(df_data, y_name="", return_grouped=True, n_periods=12):

    import statsmodels.api as ssm
    import numpy as np

    # return df_data
    df_data = df_data.sort_values(["time_series_name", "period_end_date"])
    df_data = df_data[df_data[y_name].notna()]
    df_data = df_data[df_data["value"].notna()]
    # return df_data

    def extract_lr(x, y_name):
        Y = x[y_name].astype(float).tail(n_periods)
        y_len = Y.shape[0]

        X = x[["value"]].tail(n_periods)

        X = ssm.add_constant(X)
        X = X.astype(float)
        try:
            model = ssm.OLS(Y, X).fit()
            preds = model.predict(X)

            x["preds"] = preds
            x["rsquared"] = model.rsquared
            x["slope"] = model.params[0]
            x["intercept"] = model.params[1]

            return pd.DataFrame(x)
        except:
            return None

    grouped = df_data.groupby("time_series_name")  # group by each time series name
    grouped = grouped.apply(lambda x: extract_lr(x, y_name))
    if return_grouped == True:
        df_output = (
            grouped.reset_index(drop=True)
            .groupby(
                [
                    "name_index",
                    "time_series_description",
                    "time_series_name",
                    "category",
                ]
            )
            .mean()
            .reset_index()
            .sort_values("rsquared", ascending=False)
        )
        df_output["model_row_number"] = df_output["name_index"]
        return df_output[
            [
                "model_row_number",
                "time_series_description",
                "time_series_name",
                "category",
                "rsquared",
                "slope",
                "intercept",
            ]
        ]
    else:
        return grouped
