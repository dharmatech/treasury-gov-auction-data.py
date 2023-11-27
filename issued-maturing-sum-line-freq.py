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

df = treasury_gov_pandas.update_records('https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/auctions_query', lookback=5)

# df
# ----------------------------------------------------------------------
df['record_date']   = pd.to_datetime(df['record_date'])
df['issue_date']    = pd.to_datetime(df['issue_date']) 
df['maturity_date'] = pd.to_datetime(df['maturity_date'])
df['auction_date']  = pd.to_datetime(df['auction_date'])

df['total_accepted'] = pd.to_numeric(df['total_accepted'], errors='coerce')
df['total_tendered'] = pd.to_numeric(df['total_tendered'], errors='coerce')

df['total_accepted_neg'] = df['total_accepted'] * -1
# ----------------------------------------------------------------------
bills = df[df['security_type'] == 'Bill']
notes = df[df['security_type'] == 'Note']
bonds = df[df['security_type'] == 'Bond']
# ----------------------------------------------------------------------
# freq='D'
# freq='W'
freq='M'

bills_issued   = bills.groupby(pd.Grouper(key='issue_date',    freq=freq))['total_accepted'].sum()
bills_maturing = bills.groupby(pd.Grouper(key='maturity_date', freq=freq))['total_accepted_neg'].sum()

bills_issued.to_frame().index.name = 'date'
bills_maturing.to_frame().index.name = 'date'

bills_combined = bills_issued.to_frame().join(bills_maturing.to_frame(), how='outer', on='date')

bills_combined = bills_combined.fillna(0)

bills_combined['change'] = bills_combined['total_accepted'] + bills_combined['total_accepted_neg']

bills_change = bills_combined

bills_change_non_zero = bills_change[bills_change['change'] != 0]
# ----------------------------------------------------------------------
notes_issued   = notes.groupby(pd.Grouper(key='issue_date',    freq=freq))['total_accepted'].sum()
notes_maturing = notes.groupby(pd.Grouper(key='maturity_date', freq=freq))['total_accepted_neg'].sum()

notes_issued.to_frame().index.name = 'date'
notes_maturing.to_frame().index.name = 'date'

notes_combined = notes_issued.to_frame().join(notes_maturing.to_frame(), how='outer', on='date')

notes_combined = notes_combined.fillna(0)

notes_combined['change'] = notes_combined['total_accepted'] + notes_combined['total_accepted_neg']

notes_change = notes_combined

notes_change_non_zero = notes_change[notes_change['change'] != 0]
# ----------------------------------------------------------------------
bonds_issued   = bonds.groupby(pd.Grouper(key='issue_date',    freq=freq))['total_accepted'].sum()
bonds_maturing = bonds.groupby(pd.Grouper(key='maturity_date', freq=freq))['total_accepted_neg'].sum()

bonds_issued.to_frame().index.name = 'date'
bonds_maturing.to_frame().index.name = 'date'

bonds_combined = bonds_issued.to_frame().join(bonds_maturing.to_frame(), how='outer', on='date')

bonds_combined = bonds_combined.fillna(0)

bonds_combined['change'] = bonds_combined['total_accepted'] + bonds_combined['total_accepted_neg']

bonds_change = bonds_combined

bonds_change_non_zero = bonds_change[bonds_change['change'] != 0]
# ----------------------------------------------------------------------
p = figure(
    # title='Treasury Securities Auctions Data : Net Issuance',
    title=f'Treasury Securities Auctions Data : Net Issuance : freq={freq}',
    sizing_mode='stretch_both', 
    x_axis_type='datetime',
    x_axis_label='date',
    y_axis_label='total_accepted',
)

p.yaxis.formatter = NumeralTickFormatter(format='$0a')

# p.circle(x=bills_change_non_zero['date'], y=bills_change_non_zero['change'], color='red',   legend_label='Bills')
# p.circle(x=notes_change_non_zero['date'], y=notes_change_non_zero['change'], color='green', legend_label='Notes')
# p.circle(x=bonds_change_non_zero['date'], y=bonds_change_non_zero['change'], color='blue',  legend_label='Bonds')

# p.line(x=bills_change_non_zero['date'], y=bills_change_non_zero['change'], color='red',   legend_label='Bills')
# p.line(x=notes_change_non_zero['date'], y=notes_change_non_zero['change'], color='green', legend_label='Notes')
# p.line(x=bonds_change_non_zero['date'], y=bonds_change_non_zero['change'], color='blue',  legend_label='Bonds')

p.vbar(x=bills_change_non_zero['date'], top=bills_change_non_zero['change'], color='red',   legend_label='Bills')
p.vbar(x=notes_change_non_zero['date'], top=notes_change_non_zero['change'], color='green', legend_label='Notes')
p.vbar(x=bonds_change_non_zero['date'], top=bonds_change_non_zero['change'], color='blue',  legend_label='Bonds')

p.add_tools(HoverTool(tooltips=[
    ('Date', '@x{%F}'),
    ('Change', '@y{$0.0a}'),
    ], 
    formatters={ '@x': 'datetime' }
    ))

p.legend.click_policy = 'hide'

show(p)
# ----------------------------------------------------------------------