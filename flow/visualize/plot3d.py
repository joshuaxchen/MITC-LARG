import json
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.express as px
import numpy as np
from scipy import stats

def compare(outflow, human_outflow):
    print("fixed", sum(outflow<human_outflow))

def paired_T_test(outflow, human_ouflow):
    x=stats.ttest_rel(outflow,human_outflow)
    print(x)

with open('human_baseline_eval-0.7-1.3.json','r') as f:
    data = json.load(f)
    main_inflow = data['main_inflow']
    merge_inflow = data['merge_inflow']
    outflow = data['outflow']
    human_outflow = np.array(outflow)

trace1 = go.Scatter3d(
        x=main_inflow,
        y=merge_inflow,
        z=outflow,
        mode='markers',
        name='human',
)
with open('train-fixed_40_eval-0.7-1.3.json','r') as f:
    data = json.load(f)
    main_inflow = data['main_inflow']
    merge_inflow = data['merge_inflow']
    outflow = data['outflow']
    outflow = np.array(outflow)
    print("fixed", sum(outflow>human_outflow))
    paired_T_test(outflow,human_outflow)
trace3 = go.Scatter3d(
        x=main_inflow,
        y=merge_inflow,
        z=outflow,
        mode='markers',
        name='fixed inflow',
)
with open('train-0.9-1.1_40_eval-0.7-1.3.json','r') as f:
    data = json.load(f)
    main_inflow = data['main_inflow']
    merge_inflow = data['merge_inflow']
    outflow = data['outflow']
    outflow = np.array(outflow)
    print("09-11:", sum(outflow>human_outflow))
    paired_T_test(outflow,human_outflow)

trace2 = go.Scatter3d(
        x=main_inflow,
        y=merge_inflow,
        z=outflow,
        mode='markers',
        name='[0.9,1.1]',
)
with open('train-0.7-1.3_40_eval-0.7-1.3.json','r') as f:
    data = json.load(f)
    main_inflow = data['main_inflow']
    merge_inflow = data['merge_inflow']
    outflow = data['outflow']
    outflow = np.array(outflow)
    print("07-13:", sum(outflow>human_outflow))
    paired_T_test(outflow,human_outflow)

trace4 = go.Scatter3d(
        x=main_inflow,
        y=merge_inflow,
        z=outflow,
        mode='markers',
        name='[0.7,1.3]',
)
with open('train-0.5-1.5_40_eval-0.7-1.3.json','r') as f:
    data = json.load(f)
    main_inflow = data['main_inflow']
    merge_inflow = data['merge_inflow']
    outflow = data['outflow']
    outflow = np.array(outflow)
    print("05-15:", sum(outflow>human_outflow))
    paired_T_test(outflow,human_outflow)

trace5 = go.Scatter3d(
        x=main_inflow,
        y=merge_inflow,
        z=outflow,
        mode='markers',
        name='[0.5,1.5]',
)
with open('train-fixed-linear_40_eval-0.7-1.3.json','r') as f:
    data = json.load(f)
    main_inflow = data['main_inflow']
    merge_inflow = data['merge_inflow']
    outflow = data['outflow']
    outflow = np.array(outflow)
    print("fixed-linear:", sum(outflow>human_outflow))
    paired_T_test(outflow,human_outflow)

trace6 = go.Scatter3d(
        x=main_inflow,
        y=merge_inflow,
        z=outflow,
        mode='markers',
        name='fixed linear',
)

data = [trace1, trace3, trace2, trace4, trace5, trace6]
layout = go.Layout(
      margin=dict(
          l=0,
          r=0,
          b=0,
          t=0
      ),
      scene = dict(
        xaxis = dict( title='main_inflow' ),
        yaxis = dict( title='merge_inflow' ),
        zaxis = dict( title='outflow' ) # not supported here, but appears in example?
      ), 
    )
plot(go.Figure(data=data, layout=layout), filename='eval-0.7-1.3.html')
