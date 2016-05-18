import sys
import os
from dateutil.relativedelta import relativedelta
from bokeh.models import Button, HBox, VBoxForm
from bokeh.models.widgets import Slider, Select, TextInput, RadioGroup
from bokeh.charts.attributes import cat, color
from bokeh.plotting import Figure, curdoc, vplot
from bokeh.models import ColumnDataSource
from bokeh.io import vform
from fispy.fispy import C1

d = dict(
        pay=[1.5, 1.5],
        cash=19,
        debt=70.,
        repay=0.5,
        expenses=0.7,
        stocks=12,
        max_cash=30,
        stock_growth=0.04,
        property_deposit=100,
        second_flat_cost=200,
        second_flat_monthly_payment=0.8,
        rent_first_flat=0.8,
        max_flats=1,
        pay_debt_faster=True,
        prd=50,
        )

test = C1(d=d)
source = ColumnDataSource(test.gen_quads())
TOOLS = "crosshair, pan, reset, resize, wheel_zoom"

plot = Figure(tools=TOOLS, x_axis_type='datetime', plot_height=600,
              plot_width=600, title="FI calculator")
p = plot.quad(left='left', right='right', bottom='bottom', top='top',
              color='color', source=source)

def update_graphic():
    test = C1(d=d)
    bdf_quad = test.gen_quads()
    source.data['bottom'] = bdf_quad['bottom']
    source.data['top'] = bdf_quad['top']
    source.data['left'] = bdf_quad['left']
    source.data['right'] = bdf_quad['right']
    source.trigger('data', source.data, source.data)


# Set up widgets
debt_input = Slider(title="D start", value=d['debt'], start=0.0, end=200.0,
                    step=1.0)
debt_repay = Slider(title="D repay", value=d['repay'], start=0.0, end=5,
                    step=0.1)
expense_input = Slider(title="Monthly expenses", value=d['expenses'],
                       start=0, end=5, step=0.1)
s1_input = Slider(title="s1", value=1.5, start=0.0, end=10.0)
s2_input = Slider(title="s2", value=1.5, start=0.0, end=10.0)
cash_start = Slider(title="Initial cash", value=d['cash'], start=0.0, end=100)
cash_max = Slider(title="max_cash", value=d['max_cash'], start=0.0, end=200)
# pay_faster = RadioGroup(
#        labels=["PD faster", "Base only"], active=1)
select = Select(title="Repay options:", value="base", options=["base", "ASAP"])


def update_data(attrname, old, new):
    # Get the current slider values
    d['debt'] = debt_input.value
    d['repay'] = debt_repay.value
    d['cash'] = cash_start.value
    d['max_cash'] = cash_max.value
    d['pay'] = [s1_input.value, s2_input.value]
    d['expenses'] = expense_input.value
    if select.value == 'base':
        print("In logic ", select.value)
        d['pay_debt_faster'] = False
    else:
        d['pay_debt_faster'] = True
    update_graphic()


interactive_list = [debt_input, debt_repay, expense_input, cash_start,
                    cash_max, s1_input, s2_input, select]

for w in interactive_list:
    w.on_change('value', update_data)


# Set up layouts and add to document
inputs = VBoxForm(children=interactive_list)
curdoc().add_root(HBox(children=[inputs, plot], width=800))
