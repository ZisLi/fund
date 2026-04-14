import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import akshare as ak
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 持仓基金
## 3.易方达上证科创50ETF联接C（011609）
fund_kc = ak.fund_open_fund_info_em(
    symbol="011609",
    indicator="单位净值走势"
)
fund_kc = fund_kc.rename(
    columns={
        "净值日期": "date", 
        "单位净值": "net_value", 
        "日增长率": "growth_rate(%)"
        }
        )

fund_kc["date"] = pd.to_datetime(fund_kc["date"])
fund_kc = fund_kc[fund_kc["date"] >= "2026-03-11"]
fund_kc.reset_index(drop = True, inplace = True)

plans_kc = [
    {"date": "2026-03-11", "amount": 150.00},
    {"date": "2026-03-19", "amount": 50.00},
    {"date": "2026-03-23", "amount": 20.00},
    {"date": "2026-03-31", "amount": 50.00}
]

plans_kc_df = pd.DataFrame(plans_kc)
plans_kc_df["date"] = pd.to_datetime(plans_kc_df["date"])

fund_kc["daily_invest"] = 0.0

fund_kc = fund_kc.merge(plans_kc_df, on="date", how="left")
fund_kc["amount"] = fund_kc["amount"].fillna(0)

fee_rate_kc = 0
# fund_kc.loc[fund_kc["date"] >= pd.to_datetime("2026-03-24"), "daily_invest"] = 0 * (1 - fee_rate_kc)

fund_kc["daily_invest"] = fund_kc["amount"] + fund_kc["daily_invest"]

total_shares = 0
total_invest = 0

fund_kc["shares"] = 0.0
fund_kc["total_shares"] = 0.0
fund_kc["asset"] = 0.0
fund_kc["total_invest"] = 0.0

for i in range(len(fund_kc)):
    nav = fund_kc.loc[i, "net_value"]
    invest_today = fund_kc.loc[i, "daily_invest"]

    # 买入 / 卖出
    shares = invest_today / nav

    total_shares += shares
    total_invest += invest_today

    fund_kc.loc[i, "shares"] = round(shares, 2)
    fund_kc.loc[i, "total_shares"] = round(total_shares, 2)
    fund_kc.loc[i, "asset"] = round(total_shares * nav, 2)
    fund_kc.loc[i, "total_invest"] = round(total_invest, 2)

fund_kc["profit"] = round(fund_kc["asset"] - fund_kc["total_invest"], 2)
fund_kc["Return Rate (%)"] = round(fund_kc["profit"] / fund_kc["total_invest"] * 100, 2)
fund_kc["Fund"] = "易方达科创50"

fund_kc = fund_kc[["Fund", "date", "net_value", "growth_rate(%)", "daily_invest", "total_shares", "asset", "total_invest", "profit", "Return Rate (%)"]]

## 4.华夏中证电网设备主题ETF联接A（025856）
fund_dw = ak.fund_open_fund_info_em(
    symbol="025856",
    indicator="单位净值走势"
)
fund_dw = fund_dw.rename(
    columns={
        "净值日期": "date", 
        "单位净值": "net_value", 
        "日增长率": "growth_rate(%)"
        }
        )

fund_dw["date"] = pd.to_datetime(fund_dw["date"])
fund_dw = fund_dw[fund_dw["date"] >= "2026-03-12"]
fund_dw.reset_index(drop = True, inplace = True)

fee_rate_dw = 0.0012
plans_dw = [
    {"date": "2026-03-12", "amount": 100.00 * (1 - fee_rate_dw)},
    {"date": "2026-03-16", "amount": 20.00 * (1 - fee_rate_dw)},
    {"date": "2026-03-18", "amount": 25.00 * (1 - fee_rate_dw)},
    {"date": "2026-03-20", "amount": 40.10},
    {"date": "2026-04-02", "amount": (70.00 * (1 - fee_rate_dw)) - 56.97},
    {"date": "2026-04-07", "amount": 20.00 * (1 - fee_rate_dw)},
    {"date": "2026-04-13", "amount": 50.00 * (1 - fee_rate_dw)}
]

plans_dw_df = pd.DataFrame(plans_dw)
plans_dw_df["date"] = pd.to_datetime(plans_dw_df["date"])

fund_dw["daily_invest"] = 0.0

fund_dw = fund_dw.merge(plans_dw_df, on="date", how="left")
fund_dw["amount"] = fund_dw["amount"].fillna(0)

# fund_dw.loc[fund_dw["date"] >= pd.to_datetime("2026-03-24"), "daily_invest"] = 0 * (1 - fee_rate_dw)

fund_dw["daily_invest"] = fund_dw["amount"] + fund_dw["daily_invest"]
fund_dw.head()
total_shares = 0
total_invest = 0

fund_dw["shares"] = 0.0
fund_dw["total_shares"] = 0.0
fund_dw["asset"] = 0.0
fund_dw["total_invest"] = 0.0

for i in range(len(fund_dw)):
    nav = fund_dw.loc[i, "net_value"]
    invest_today = fund_dw.loc[i, "daily_invest"]

    # 买入 / 卖出
    shares = invest_today / nav

    total_shares += shares
    total_invest += invest_today

    fund_dw.loc[i, "shares"] = round(shares, 2)
    fund_dw.loc[i, "total_shares"] = round(total_shares, 2)
    fund_dw.loc[i, "asset"] = round(total_shares * nav, 2)
    fund_dw.loc[i, "total_invest"] = round(total_invest, 2)

fund_dw["profit"] = round(fund_dw["asset"] - fund_dw["total_invest"], 2)
fund_dw["Return Rate (%)"] = round(fund_dw["profit"] / fund_dw["total_invest"] * 100, 2)
fund_dw["Fund"] = "华夏中证电网设备"

fund_dw = fund_dw[[ "Fund", "date", "net_value", "growth_rate(%)", "daily_invest", "total_shares", "asset", "total_invest", "profit", "Return Rate (%)"]]


## 5.华夏中证绿色电力ETF联接A（018734）
fund_ld = ak.fund_open_fund_info_em(
    symbol="018734",
    indicator="单位净值走势"
)
fund_ld = fund_ld.rename(
    columns={
        "净值日期": "date", 
        "单位净值": "net_value", 
        "日增长率": "growth_rate(%)"
        }
        )

fund_ld["date"] = pd.to_datetime(fund_ld["date"])
fund_ld = fund_ld[fund_ld["date"] >= "2026-03-10"]
fund_ld.reset_index(drop = True, inplace = True)

fee_rate_ld = 0.0010
plans_ld = [
    {"date": "2026-03-10", "amount": 100.00 * (1 - fee_rate_ld)},
    {"date": "2026-03-31", "amount": 35.00 * (1 - fee_rate_ld)},
    {"date": "2026-04-03", "amount": (150.00 * (1 - fee_rate_ld)) - 88.11},
    {"date": "2026-04-07", "amount": 90.00 * (1 - fee_rate_ld)}
]

plans_ld_df = pd.DataFrame(plans_ld)
plans_ld_df["date"] = pd.to_datetime(plans_ld_df["date"])

fund_ld["daily_invest"] = 0.0

fund_ld = fund_ld.merge(plans_ld_df, on="date", how="left")
fund_ld["amount"] = fund_ld["amount"].fillna(0)

# fund_ld.loc[fund_ld["date"] >= pd.to_datetime("2026-03-24"), "daily_invest"] = 0 * (1 - fee_rate_ld)

fund_ld["daily_invest"] = fund_ld["amount"] + fund_ld["daily_invest"]

total_shares = 0
total_invest = 0

fund_ld["shares"] = 0.0
fund_ld["total_shares"] = 0.0
fund_ld["asset"] = 0.0
fund_ld["total_invest"] = 0.0

for i in range(len(fund_ld)):
    nav = fund_ld.loc[i, "net_value"]
    invest_today = fund_ld.loc[i, "daily_invest"]

    # 买入 / 卖出
    shares = invest_today / nav

    total_shares += shares
    total_invest += invest_today

    fund_ld.loc[i, "shares"] = round(shares, 2)
    fund_ld.loc[i, "total_shares"] = round(total_shares, 2)
    fund_ld.loc[i, "asset"] = round(total_shares * nav, 2)
    fund_ld.loc[i, "total_invest"] = round(total_invest, 2)

fund_ld["profit"] = round(fund_ld["asset"] - fund_ld["total_invest"], 2)
fund_ld["Return Rate (%)"] = round(fund_ld["profit"] / fund_ld["total_invest"] * 100, 2)
fund_ld["Fund"] = "华夏中证绿色电力"

fund_ld = fund_ld[[ "Fund", "date", "net_value", "growth_rate(%)", "daily_invest", "total_shares", "asset", "total_invest", "profit", "Return Rate (%)"]]

## 6.广发远见智选混合C（016874）
fund_yj = ak.fund_open_fund_info_em(
    symbol="016874",
    indicator="单位净值走势"
)
fund_yj = fund_yj.rename(
    columns={
        "净值日期": "date", 
        "单位净值": "net_value", 
        "日增长率": "growth_rate(%)"
        }
        )

fund_yj["date"] = pd.to_datetime(fund_yj["date"])
fund_yj = fund_yj[fund_yj["date"] >= "2026-03-27"]
fund_yj.reset_index(drop = True, inplace = True)

fee_rate_yj = 0.000
plans_yj = [
    {"date": "2026-03-27", "amount": 100.00 * (1 - fee_rate_yj)},
    {"date": "2026-04-10", "amount": 100.00 * (1 - fee_rate_yj)}
]

plans_yj_df = pd.DataFrame(plans_yj)
plans_yj_df["date"] = pd.to_datetime(plans_yj_df["date"])

fund_yj["daily_invest"] = 0.0

fund_yj = fund_yj.merge(plans_yj_df, on="date", how="left")
fund_yj["amount"] = fund_yj["amount"].fillna(0)

# fund_yj.loc[fund_yj["date"] >= pd.to_datetime("2026-03-24"), "daily_invest"] = 0 * (1 - fee_rate_yj)

fund_yj["daily_invest"] = fund_yj["amount"] + fund_yj["daily_invest"]

total_shares = 0
total_invest = 0

fund_yj["shares"] = 0.0
fund_yj["total_shares"] = 0.0
fund_yj["asset"] = 0.0
fund_yj["total_invest"] = 0.0

for i in range(len(fund_yj)):
    nav = fund_yj.loc[i, "net_value"]
    invest_today = fund_yj.loc[i, "daily_invest"]

    # 买入 / 卖出
    shares = invest_today / nav

    total_shares += shares
    total_invest += invest_today

    fund_yj.loc[i, "shares"] = round(shares, 2)
    fund_yj.loc[i, "total_shares"] = round(total_shares, 2)
    fund_yj.loc[i, "asset"] = round(total_shares * nav, 2)
    fund_yj.loc[i, "total_invest"] = round(total_invest, 2)

fund_yj["profit"] = round(fund_yj["asset"] - fund_yj["total_invest"], 2)
fund_yj["Return Rate (%)"] = round(fund_yj["profit"] / fund_yj["total_invest"] * 100, 2)
fund_yj["Fund"] = "广发远见混合"

fund_yj = fund_yj[[ "Fund", "date", "net_value", "growth_rate(%)", "daily_invest", "total_shares", "asset", "total_invest", "profit", "Return Rate (%)"]]


## 7.南方有色金属ETF联接C（004433）
fund_js = ak.fund_open_fund_info_em(
    symbol="004433",
    indicator="单位净值走势"
)
fund_js = fund_js.rename(
    columns={
        "净值日期": "date", 
        "单位净值": "net_value", 
        "日增长率": "growth_rate(%)"
        }
        )

fund_js["date"] = pd.to_datetime(fund_js["date"])
fund_js = fund_js[fund_js["date"] >= "2026-03-27"]
fund_js.reset_index(drop = True, inplace = True)

fee_rate_js = 0.000
plans_js = [
    {"date": "2026-03-27", "amount": 100.00 * (1 - fee_rate_js)}
]

plans_js_df = pd.DataFrame(plans_js)
plans_js_df["date"] = pd.to_datetime(plans_js_df["date"])

fund_js = fund_js.merge(plans_js_df, on="date", how="left")

fund_js["amount"] = fund_js["amount"].fillna(0)
fund_js["daily_invest"] = 0.0
# fund_js.loc[fund_js["date"] >= pd.to_datetime("2026-03-24"), "daily_invest"] = 0 * (1 - fee_rate_js)

fund_js["daily_invest"] = fund_js["amount"] + fund_js["daily_invest"]
total_shares = 0
total_invest = 0

fund_js["shares"] = 0.0
fund_js["total_shares"] = 0.0
fund_js["asset"] = 0.0
fund_js["total_invest"] = 0.0

for i in range(len(fund_js)):
    nav = fund_js.loc[i, "net_value"]
    invest_today = fund_js.loc[i, "daily_invest"]

    # 买入 / 卖出
    shares = invest_today / nav

    total_shares += shares
    total_invest += invest_today

    fund_js.loc[i, "shares"] = round(shares, 2)
    fund_js.loc[i, "total_shares"] = round(total_shares, 2)
    fund_js.loc[i, "asset"] = round(total_shares * nav, 2)
    fund_js.loc[i, "total_invest"] = round(total_invest, 2)

fund_js["profit"] = round(fund_js["asset"] - fund_js["total_invest"], 2)
fund_js["Return Rate (%)"] = round(fund_js["profit"] / fund_js["total_invest"] * 100, 2)
fund_js["Fund"] = "南方有色金属"

fund_js = fund_js[[ "Fund", "date", "net_value", "growth_rate(%)", "daily_invest", "total_shares", "asset", "total_invest", "profit", "Return Rate (%)"]]

## 8.华泰柏瑞质量成长混合C（011452）
fund_cpo = ak.fund_open_fund_info_em(
    symbol="011452",
    indicator="单位净值走势"
)
fund_cpo = fund_cpo.rename(
    columns={
        "净值日期": "date", 
        "单位净值": "net_value", 
        "日增长率": "growth_rate(%)"
        }
        )

fund_cpo["date"] = pd.to_datetime(fund_cpo["date"])
fund_cpo = fund_cpo[fund_cpo["date"] >= "2026-04-02"]
fund_cpo.reset_index(drop = True, inplace = True)

fee_rate_cpo = 0.000
plans_cpo = [
    {"date": "2026-04-02", "amount": 100.00 * (1 - fee_rate_cpo)},
    {"date": "2026-04-10", "amount": 50.00 * (1 - fee_rate_cpo)}
]

plans_cpo_df = pd.DataFrame(plans_cpo)
plans_cpo_df["date"] = pd.to_datetime(plans_cpo_df["date"])

fund_cpo = fund_cpo.merge(plans_cpo_df, on="date", how="left")

fund_cpo["amount"] = fund_cpo["amount"].fillna(0)
fund_cpo["daily_invest"] = 0.0
# fund_cpo.loc[fund_cpo["date"] >= pd.to_datetime("2026-04-02"), "daily_invest"] = 0 * (1 - fee_rate_cpo)

fund_cpo["daily_invest"] = fund_cpo["amount"] + fund_cpo["daily_invest"]
total_shares = 0
total_invest = 0

fund_cpo["shares"] = 0.0
fund_cpo["total_shares"] = 0.0
fund_cpo["asset"] = 0.0
fund_cpo["total_invest"] = 0.0

for i in range(len(fund_cpo)):
    nav = fund_cpo.loc[i, "net_value"]
    invest_today = fund_cpo.loc[i, "daily_invest"]

    # 买入 / 卖出
    shares = invest_today / nav

    total_shares += shares
    total_invest += invest_today

    fund_cpo.loc[i, "shares"] = round(shares, 2)
    fund_cpo.loc[i, "total_shares"] = round(total_shares, 2)
    fund_cpo.loc[i, "asset"] = round(total_shares * nav, 2)
    fund_cpo.loc[i, "total_invest"] = round(total_invest, 2)

fund_cpo["profit"] = round(fund_cpo["asset"] - fund_cpo["total_invest"], 2)
fund_cpo["Return Rate (%)"] = round(fund_cpo["profit"] / fund_cpo["total_invest"] * 100, 2)
fund_cpo["Fund"] = "华泰成长混合"

fund_cpo = fund_cpo[[ "Fund", "date", "net_value", "growth_rate(%)", "daily_invest", "total_shares", "asset", "total_invest", "profit", "Return Rate (%)"]]


funds = pd.concat([fund_kc, fund_dw, fund_ld, fund_yj, fund_js, fund_cpo], ignore_index = True)
funds["daily profit"] = funds.groupby("Fund")["profit"].diff()
funds = funds[funds["total_shares"] > 0]
date = funds["date"].max()
date_only = date.date()

total_funds = funds[funds["date"] <= date].copy()
total_funds = total_funds[total_funds["total_shares"] > 0]
total_funds["weight"] = (
    total_funds["asset"] /
    total_funds.groupby("date")["asset"].transform("sum")
)

# 加权收益率
total_funds["weighted_rate"] = (
    total_funds["Return Rate (%)"] * total_funds["weight"]
)

# 每天组合收益
portfolio_rate = (
    total_funds.groupby("date")["weighted_rate"]
    .sum()
    .reset_index()
)
portfolio_rate["smooth"] = portfolio_rate["weighted_rate"].rolling(5).mean()


fig_rate = px.line(
    funds,
    x="date",
    y="Return Rate (%)",
    color="Fund",
    title=f"Portfolio Total Profit Rate(%) (Updated on {date_only})"
)

fig_rate.add_trace(
    go.Scatter(
        x=portfolio_rate["date"],
        y=round(portfolio_rate["weighted_rate"],2),
        mode="lines",
        name="Portfolio",
        line=dict(color="black", width=2, dash="dash")
    )
)

fig_rate.add_hline(
    y=0,
    line=dict(color="red", width=2, dash="dash")
)
fig_rate.update_layout(legend_title="Fund")

funds_share = (
    funds[funds["date"] == date]
         .groupby("Fund")
         .tail(1)
         .reset_index(drop=True)
)

funds_share["color"] = funds_share["daily profit"].apply(
    lambda x: "Positive" if x >= 0 else "Negative"
)

funds_share = funds_share.sort_values("daily profit")
funds_share.tail(60)

fig_pie = px.pie(
    funds_share,
    names="Fund",
    values="asset",
    title=f"Asset Allocation (Updated on {date_only})"
)

fig_pie.update_traces(
    textinfo="percent"
)

fig_pie.update_traces(hole=0.3)


profit_kc = funds_share["daily profit"][funds_share["Fund"] == "易方达科创50"]
profit_dw = funds_share["daily profit"][funds_share["Fund"] == "华夏中证电网设备"]
profit_ld = funds_share["daily profit"][funds_share["Fund"] == "华夏中证绿色电力"]
profit_yj = funds_share["daily profit"][funds_share["Fund"] == "广发远见混合"]
profit_js = funds_share["daily profit"][funds_share["Fund"] == "南方有色金属"]
profit_cpo = funds_share["daily profit"][funds_share["Fund"] == "华泰成长混合"]

fig_profit = px.bar(
    funds_share,
    x="Fund",
    y="daily profit",
    color="color",
    title=f"Earnings (Updated on {date_only})",
    color_discrete_map={
        "Positive": "#16c784",
        "Negative": "#ea3943"
    }
)

fig_profit.update_traces(
    hovertemplate="Fund: %{x}<br>Profit: %{y:.2f}"
)

fig_profit.update_layout(showlegend=False)

fig_profit.update_layout(xaxis_title=None, yaxis_title=None)

Profit = funds_share["daily profit"].sum()

Invest = funds_share["total_invest"].sum()

Asset = funds_share["asset"].sum()

Return_Rate = round((Asset - Invest)/Invest * 100, 2)

Arrow = "▲" if Asset > Invest else "▼"
arrow = "▲" if Profit > 0 else "▼"

df_time = (
    funds.groupby("date")
    .agg({
        "asset": "sum",
        "total_invest": "sum"
    })
    .reset_index()
)


df_time["Returns"] = df_time["asset"] - df_time["total_invest"]


def make_card(title, value, color="black"):
    return dbc.Card(
        dbc.CardBody([
            html.H6(title, className="text-muted"),
            html.H2(value, style={"color": color,
                                  "fontWeight": "bold"})
        ]),
        style={
            "textAlign": "center",
            "borderRadius": "15px",
            "boxShadow": "0 4px 10px rgba(0,0,0,0.1)"
        }
    )


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])


# ===== layout =====
app.layout = dbc.Container([

    html.H2("📊 Portfolio", className="my-4"),
    html.Br(),
    
    dbc.Row([
        dbc.Col(make_card("Total Asset", f"{Asset:.2f}({Arrow}{Return_Rate:.2f}%)",
                          color = "#16c784" if Asset > Invest else "#ea3943")),
        dbc.Col(make_card("Total Invest", f"{Invest:.2f}")),
        dbc.Col(make_card("Return", f"{arrow}{Profit:.2f}",
                          color = "#16c784" if Profit > 0 else "#ea3943"
                          ))
    ]),
    html.Br(),
    
    html.Div([
    
    dcc.Dropdown(
        id="time-filter",
        options=[
            {"label": "1W", "value": 7},
            {"label": "1M", "value": 30},
            {"label": "3M", "value": 90},
            {"label": "All", "value": "all"},
        ],
        value="all",
        clearable=False,
        style={
            "position": "absolute",
            "top": "10px",
            "right": "20px",
            "width": "120px",
            "zIndex": 1000,
            "backgroundColor": "white"
        }),
    dcc.Graph(id="profit-chart")], 
    style={"position": "relative"}),
    html.Br(),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_profit), xs = 12, md = 6),
        dbc.Col(dcc.Graph(figure=fig_pie), xs = 12, md = 6)])], fluid=True)

@app.callback(
    Output("profit-chart", "figure"),
    Input("time-filter", "value")
)

def update_chart(days):
    
    df_filtered = funds[funds["date"] >= "2026-03-09"].copy()
    if days != "all":
        df_filtered = (
            df_filtered.sort_values("date")
            .groupby("Fund")
            .tail(days)
        )
    fig_rate = px.line(
        df_filtered,
        x="date",
        y="Return Rate (%)",
        color="Fund",
        title=f"Return Rate(%)"
    )
    
    pr_filtered = portfolio_rate[portfolio_rate["date"] >= "2026-03-09"].copy()

    if days != "all":
        pr_filtered = pr_filtered.tail(days)

    fig_rate.add_trace(
        go.Scatter(
            x=pr_filtered["date"],
            y=round(pr_filtered["weighted_rate"], 2),
            mode="lines",
            name="Portfolio",
            line=dict(color="black", width=2.5)
        )
    )
    fig_rate.add_hline(
        y=0,
        line=dict(color="red", width=2, dash="dash")
    )
    fig_rate.update_layout(
    xaxis_title=None,
    yaxis_title=None)
    return fig_rate

app.layout.style = {
    "backgroundColor": "#DAE8FA"
    }


server = app.server
if __name__ == "__main__":
    app.run(debug=True)
