import pandas as pd
import treasury_gov_pandas
from bokeh.plotting import figure, show
from bokeh.models   import NumeralTickFormatter, HoverTool
import bokeh.models

import bokeh.palettes
import bokeh.transform
# ----------------------------------------------------------------------
# df = treasury_gov_pandas.update_records(
#     'auctions_query.pkl',
#     'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/auctions_query')

df = treasury_gov_pandas.update_records('https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/auctions_query', lookback=10)

# df
# ----------------------------------------------------------------------
df['issue_date']    = pd.to_datetime(df['issue_date']) 
df['maturity_date'] = pd.to_datetime(df['maturity_date'])

df['total_accepted'] = pd.to_numeric(df['total_accepted'], errors='coerce')
# ----------------------------------------------------------------------

# show all unique values in 'security_type'

df['security_type'].unique()

# ----------------------------------------------------------------------
# group by 'issue_date' and 'security_type' and sum 'total_accepted'

issued = df.groupby(['issue_date', 'security_type'])['total_accepted'].sum().reset_index()

# group by 'maturity_date' and 'security_type' and sum 'total_accepted'

maturing = df.groupby(['maturity_date', 'security_type'])['total_accepted'].sum().reset_index()

# join issued and maturing on 'issue_date' = 'maturity_date' and 'security_type' = 'security_type'

merged = pd.merge(issued, maturing, how='outer', left_on=['issue_date', 'security_type'], right_on=['maturity_date', 'security_type'])

merged.rename(columns={'total_accepted_x': 'issued', 'total_accepted_y': 'maturing'}, inplace=True)

merged['change'] = merged['issued'].fillna(0) - merged['maturing'].fillna(0)

merged['date'] = merged['issue_date'].combine_first(merged['maturity_date'])
# ----------------------------------------------------------------------
tmp = merged

agg = tmp.groupby(['date', 'security_type'])['change'].sum().reset_index()

# agg['date'] = agg['date'].dt.date

pivot_df = agg.pivot(index='date', columns='security_type', values='change').fillna(0)

# ----------------------------------------------------------------------
custom_colors = [
    bokeh.palettes.Category20c[20][5],
    bokeh.palettes.Category20c[20][6],
    
    bokeh.palettes.Category20c[20][8],
    bokeh.palettes.Category20c[20][9],
    bokeh.palettes.Category20c[20][10],

    bokeh.palettes.Category20c[20][0],
    bokeh.palettes.Category20c[20][1]
]

# stacked_items = ['Bill', 'CMB', 'Note', 'FRN Note', 'TIPS Note', 'Bond']

stacked_items = ['Bill', 'CMB', 'Note', 'FRN Note', 'TIPS Note', 'Bond', 'TIPS Bond']
# ----------------------------------------------------------------------

p = figure(title='Treasury Securities Net Issuance', sizing_mode='stretch_both', x_axis_type='datetime', x_axis_label='date', y_axis_label='change')

width = pd.Timedelta(days=0.9)

# p.vbar_stack(stackers=stacked_items, x='date', width=width, color=custom_colors, source=pivot_df, legend_label=stacked_items)

p.vbar_stack(stackers=stacked_items, x='date', width=width, color=custom_colors, source=pivot_df[pivot_df < 0].fillna(0), legend_label=stacked_items)
p.vbar_stack(stackers=stacked_items, x='date', width=width, color=custom_colors, source=pivot_df[pivot_df > 0].fillna(0), legend_label=stacked_items)

p.yaxis.formatter = NumeralTickFormatter(format='$0a')

p.add_tools(HoverTool(tooltips=[
    ('date', '@date{%F}'),
    ('Date', '@x{%F}'),
    ('Change', '@top{$0.0a}'),
    ], 
    formatters={ '@x': 'datetime', '@date': 'datetime'}
    ))

p.legend.click_policy = 'hide'

# p.xaxis.ticker = bokeh.models.MonthsTicker(months=list(range(1, 13)))

p.xaxis.ticker = bokeh.models.DatetimeTicker(desired_num_ticks=30)

show(p)

# ----------------------------------------------------------------------
# exit()
# ----------------------------------------------------------------------

df[df['issue_date']    == '2024-04-18'][['cusip', 'issue_date', 'maturity_date', 'security_type', 'total_accepted']]
df[df['maturity_date'] == '2024-04-18'][['cusip', 'issue_date', 'maturity_date', 'security_type', 'total_accepted']]



# rows where 'issue_date' is > '2024-03-01' and 'issue_date' is < '2024-03-31'

issued = df[(df['issue_date'] >= '2024-03-01') & (df['issue_date'] <= '2024-03-31')][['cusip', 'issue_date', 'maturity_date', 'security_type', 'total_accepted']]

maturing = df[(df['maturity_date'] >= '2024-03-01') & (df['maturity_date'] <= '2024-03-31')][['cusip', 'issue_date', 'maturity_date', 'security_type', 'total_accepted']]



issued[(issued['issue_date'] >= '2024-03-01') & (issued['issue_date'] <= '2024-03-31')]

maturing[(maturing['maturity_date'] >= '2024-03-01') & (maturing['maturity_date'] <= '2024-03-31')]



merged[(merged['issue_date'] >= '2024-03-01') & (merged['issue_date'] <= '2024-03-31')]

merged[(merged['maturity_date'] >= '2024-03-01') & (merged['maturity_date'] <= '2024-03-31')]

# new column 'issue_or_maturity_date' with values from 'issue_date' or 'maturity_date'

# merged['issue_or_maturity_date'] = merged['issue_date'].combine_first(merged['maturity_date'])

# merged['date'] = merged['issue_date'].combine_first(merged['maturity_date'])

merged[(merged['date'] >= '2024-03-01') & (merged['date'] <= '2024-03-31')][['date', 'security_type', 'issue_date', 'maturity_date', 'total_accepted_x', 'total_accepted_y', 'change']]

# merged['total_accepted_x'] = merged['total_accepted_x'].fillna(0)
# merged['total_accepted_y'] = merged['total_accepted_y'].fillna(0)

# merged['issue_date']

pivot_df['2024-03-01':'2024-03-31']

pivot_df['2024-04-15':'2024-04-15']

df[df['issue_date'] == '2024-04-15'][['security_type', 'issue_date', 'maturity_date', 'total_accepted']]

df[df['maturity_date'] == '2024-04-15'][['security_type', 'issue_date', 'maturity_date', 'total_accepted']]['total_accepted'].sum()

type(pivot_df.index)

pivot_df['Bill']