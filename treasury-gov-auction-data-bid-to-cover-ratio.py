import pandas as pd

from bokeh.plotting import figure, show
from bokeh.models   import NumeralTickFormatter, HoverTool

from bokeh.models import LinearAxis, Range1d

import yfinance as yf

import treasury_gov_pandas
# ---------------------------------------------------------------------
df = treasury_gov_pandas.update_records(
    'auctions_query.pkl',
    'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/auctions_query')

# print(df.iloc[-100].to_string())

# df[['tips']].value_counts()
# ---------------------------------------------------------------------
df['record_date']   = pd.to_datetime(df['record_date'])
df['issue_date']    = pd.to_datetime(df['issue_date']) 
df['maturity_date'] = pd.to_datetime(df['maturity_date'])
df['auction_date']  = pd.to_datetime(df['auction_date'])

df['price_per100'] = pd.to_numeric(df['price_per100'], errors='coerce')
# ----------------------------------------------------------------------
bills = df[df['security_type'] == 'Bill']
notes = df[df['security_type'] == 'Note']
bonds = df[df['security_type'] == 'Bond']

# bills_4_week = df[df['security_term'] == '4-Week']
# bills_8_week = df[df['security_term'] == '8-Week']
# bills_13_week = df[df['security_term'] == '13-Week']
# bills_26_week = df[df['security_term'] == '26-Week']
# bills_52_week = df[df['security_term'] == '52-Week']

# notes_2_year  = df[ df['security_term'] == '2-Year']
# notes_3_year  = df[ df['security_term'] == '3-Year']
# notes_5_year  = df[(df['security_term'] == '5-Year')  | df['security_term'].str.startswith('4-Year')]
# notes_7_year  = df[ df['security_term'] == '7-Year']
# notes_10_year = df[(df['security_term'] == '10-Year') | df['security_term'].str.startswith('9-Year')]

# bonds_20_year = df[df['security_term'].str.contains('20-Year|19-Year')]
# bonds_30_year = df[df['security_term'].str.contains('30-Year|29-Year')]

bills_4_week = df[df['security_term'] == '4-Week']
bills_8_week = df[df['security_term'] == '8-Week']
bills_13_week = df[df['security_term'] == '13-Week']
bills_26_week = df[df['security_term'] == '26-Week']
bills_52_week = df[df['security_term'] == '52-Week']

notes_2_year  = df[ df['security_term'] == '2-Year']
notes_3_year  = df[ df['security_term'] == '3-Year']

notes_5_year      = df[   ((df['security_term'] == '5-Year')  | df['security_term'].str.startswith('4-Year'))   &   (df['tips'] == 'No')]
notes_5_year_tips = df[   ((df['security_term'] == '5-Year')  | df['security_term'].str.startswith('4-Year'))   &   (df['tips'] == 'Yes')]

notes_7_year  = df[ df['security_term'] == '7-Year']

# notes_10_year      = df[   ((df['security_term'] == '10-Year') | df['security_term'].str.startswith('9-Year'))   &   (df['tips'] == 'No')   ]
notes_10_year      = df[   ((df['security_term'] == '10-Year') | df['security_term'].str.startswith('9-Year'))   &   ((df['tips'] == 'No') | (df['tips'] == 'null'))   ]
notes_10_year_tips = df[   ((df['security_term'] == '10-Year') | df['security_term'].str.startswith('9-Year'))   &   (df['tips'] == 'Yes')  ]

bonds_20_year = df[df['security_term'].str.contains('20-Year|19-Year')]

bonds_30_year      = df[   df['security_term'].str.contains('30-Year|29-Year')   &   (df['tips'] == 'No')    ]
bonds_30_year_tips = df[   df['security_term'].str.contains('30-Year|29-Year')   &   (df['tips'] == 'Yes')   ]

# ----------------------------------------------------------------------
y_field = 'bid_to_cover_ratio'

# p = figure(
#     title=f'Treasury Securities Auctions Data', sizing_mode='stretch_both', 
#     x_axis_type='datetime', x_axis_label='date', y_axis_label=y_field,
#     x_range=(pd.to_datetime('1972-01-01'), pd.to_datetime('2030-01-01')),
#     y_range=(-3, 19))

p = figure(title=f'Treasury Securities Auctions Data', sizing_mode='stretch_both', x_axis_type='datetime', x_axis_label='date', y_axis_label=y_field, y_range=(0, 12))

p.circle(x='auction_date', y=y_field, color='red',   legend_label=f'{y_field} : bills', source=bills)
p.circle(x='auction_date', y=y_field, color='green', legend_label=f'{y_field} : notes', source=notes)
p.circle(x='auction_date', y=y_field, color='blue',  legend_label=f'{y_field} : bonds', source=bonds)

p.line(  x='auction_date', y=y_field, color='red',   legend_label=f'{y_field} : 4-Week', source=bills_4_week)
p.line(  x='auction_date', y=y_field, color='red',   legend_label=f'{y_field} : 8-Week', source=bills_8_week)
p.line(  x='auction_date', y=y_field, color='red',   legend_label=f'{y_field} : 13-Week', source=bills_13_week)
p.line(  x='auction_date', y=y_field, color='red',   legend_label=f'{y_field} : 26-Week', source=bills_26_week)
p.line(  x='auction_date', y=y_field, color='red',   legend_label=f'{y_field} : 52-Week', source=bills_52_week)

p.line(  x='auction_date', y=y_field, color='green', legend_label=f'{y_field} : 2-Year',  source=notes_2_year)
p.line(  x='auction_date', y=y_field, color='green', legend_label=f'{y_field} : 3-Year',  source=notes_3_year)

p.line(  x='auction_date', y=y_field, color='green', legend_label=f'{y_field} : 5-Year',  source=notes_5_year)
p.line(  x='auction_date', y=y_field, color='green', legend_label=f'{y_field} : 5-Year TIPS', source=notes_5_year_tips)

p.line(  x='auction_date', y=y_field, color='green', legend_label=f'{y_field} : 7-Year',  source=notes_7_year)

p.line(  x='auction_date', y=y_field, color='green', legend_label=f'{y_field} : 10-Year', source=notes_10_year)
p.line(  x='auction_date', y=y_field, color='green', legend_label=f'{y_field} : 10-Year TIPS', source=notes_10_year_tips)

p.line(  x='auction_date', y=y_field, color='blue',  legend_label=f'{y_field} : 20-Year', source=bonds_20_year)

p.line(  x='auction_date', y=y_field, color='blue',  legend_label=f'{y_field} : 30-Year', source=bonds_30_year)
p.line(  x='auction_date', y=y_field, color='blue',  legend_label=f'{y_field} : 30-Year TIPS', source=bonds_30_year_tips)

p.legend.click_policy = 'hide'

p.legend.location = 'top_left'

p.add_tools(HoverTool(
    tooltips=[ 
        ('record_date',   '@record_date{%F}'),
        ('auction_date',  '@auction_date{%F}'),
        ('issue_date',    '@issue_date{%F}'),
        ('maturity_date', '@maturity_date{%F}'),
        ('cusip',         '@cusip'),
        ('price_per100',  '@price_per100{0.00}'),
        ('security_type', '@security_type'),
        ('security_term', '@security_term'),
        ('high_discnt_rate', '@high_discnt_rate{0.0000}'),
        ('high_investment_rate', '@high_investment_rate{0.0000}'),
        ('high_yield',       '@high_yield{0.0000}'),
        ('bid_to_cover_ratio', '@bid_to_cover_ratio{0.0000}'),
        ('tips', '@tips'),
    ], 
    formatters={ 
        '@record_date':   'datetime',
        '@auction_date': 'datetime',
        '@issue_date': 'datetime',
        '@maturity_date': 'datetime',
    }))

show(p)

