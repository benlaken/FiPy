import sys
import os
import datetime as dt
from dateutil.relativedelta import relativedelta
from bokeh.models import Button, HBox, VBoxForm
from bokeh.models.widgets import Slider, Select, TextInput, RadioGroup
from bokeh.models.widgets import PreText, Button
from bokeh.charts.attributes import cat, color
from bokeh.plotting import Figure, curdoc, vplot
from bokeh.layouts import row, column, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.io import vform
from fispy import Asset, Portfolio


# Initilise with list of assets...
d1 = {'kind': 'job',
      'monthly_income': 1.5,
      'monthly_expenses': 0.7,
      'start_date': dt.date(2016, 6, 1)}

d2 = {'kind': 'job',
      'monthly_income': 1.5,
      'start_date': dt.date(2016, 12, 1)}

d3 = {'kind': 'real estate',
      'debt': 70,
      'value': 150,
      'monthly_repayment': 0.5,
      'start_date': dt.date(2016, 6, 1),
      'pay_debt_asap': True}

d4 = {'kind': 'stocks',
      'value': 15,
      'symbol': 'NYSE:BRK.B'}

d5 = {'kind': 'cash',
      'value': 15,
      'max_cash': 30}

projection = Portfolio(Asset(**d1),
                       Asset(**d2),
                       Asset(**d3),
                       Asset(**d4),
                       Asset(**d5), prd=200)
source = ColumnDataSource(projection.gen_quads())

TOOLS = "crosshair, pan, reset, resize, wheel_zoom"
plot = Figure(tools=TOOLS, x_axis_type='datetime', plot_height=600,
              plot_width=600, title="FI calculator")
p = plot.quad(left='left', right='right', bottom='bottom', top='top',
              color='color', source=source)


def update_graphic():
    """Update the data of the Asset dictionaries and recreate the
    projection.
    """
    projection = Portfolio(Asset(**d1),
                           Asset(**d2),
                           Asset(**d3),
                           Asset(**d4),
                           Asset(**d5), prd=200)
    bdf_quad = projection.gen_quads()
    # print(bdf_quad.head())
    source.data['bottom'] = bdf_quad['bottom']
    source.data['top'] = bdf_quad['top']
    source.data['left'] = bdf_quad['left']
    source.data['right'] = bdf_quad['right']
    source.trigger('data', source.data, source.data)


# Set up widgets
debt_input = Slider(title="D start", value=d3['debt'], start=0.0,
                    end=200.0, step=1.0)
debt_repay = Slider(title="D repay", value=d3['monthly_repayment'],
                    start=0.0, end=5, step=0.1)
expense_input = Slider(title="Monthly expenses", value=d1['monthly_expenses'],
                       start=0, end=5, step=0.1)
s1_input = Slider(title="s1", value=d1['monthly_income'], start=0.0, end=10.0)
s2_input = Slider(title="s2", value=d2['monthly_income'], start=0.0, end=10.0)
cash_start = Slider(title="Initial cash", value=d5['value'],
                    start=0.0, end=100)
cash_max = Slider(title="max_cash", value=d5['max_cash'], start=0.0, end=200)
select = RadioGroup(labels=["base repayments only", "repay ASAP"], active=0)
button = Button(label="Calculate", button_type="success")

stats = PreText(text='', width=800)


def update_text(in_text):
    """temp function: status printing will go here"""
    stats.text = in_text


def update():
    """Set the current silder values as dictionary values on button click
    recalculate values, and update the graphic source data.
    """
    d3['debt'] = debt_input.value
    d3['monthly_repayment'] = debt_repay.value
    d5['value'] = cash_start.value
    d5['max_cash'] = cash_max.value
    d1['monthly_income'] = s1_input.value
    d2['monthly_income'] = s2_input.value
    d1['monthly_expenses'] = expense_input.value
    if select.labels[select.active] == "base repayments only":
        d3['pay_debt_asap'] = False
    elif select.labels[select.active] == "repay ASAP":
        d3['pay_debt_asap'] = True
    else:
        raise ValueError("select variable gave unexpected value: {0}".format(
            select.labels[select.active]))
    update_text("Placeholder text...")
    update_graphic()


widget_list = widgetbox(select, debt_input, debt_repay, expense_input,
                        cash_start, cash_max, s1_input, s2_input,
                        button, width=300)

button.on_click(update)

# Set up layouts and add to document
bottomrow = row(stats)
toprow = row(widget_list, plot)
layout = column(toprow, bottomrow)
curdoc().add_root(layout)
