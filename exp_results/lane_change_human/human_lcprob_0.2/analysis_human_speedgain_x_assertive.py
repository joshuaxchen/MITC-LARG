import numpy as np
from glob import glob
import re
results = []
files=glob("*.txt")
for f in files:
    fname = f.split("_")
    attributes = {}
    for s in fname:
        try:
            number = float(re.findall(r"[-+]?\d*\.\d+|\d+",s)[0])
        except: continue
        if s.startswith("LEFT"):
            attributes["left_inflow"]=number
        if s.startswith("RIGHTHUMANLC"):
            attributes["right_human_lc"]=number
        elif s.startswith("RIGHT"):
            attributes["right_inflow"]=number
        if s.startswith("SPEEDGAIN"):
            attributes["speedgain"]=number
        if s.startswith("ASSERTIVE"):
            attributes["assertive"]=number
        if s.startswith("MERGE"):
            attributes["merge"]=number
    content = open(f,'r')
    start_reading = False
    metrics={}
    for line in content:
        if line.startswith("Round  100 :"):
            start_reading = True
        if start_reading: 
            if line.startswith("Speed"):
                speed = re.findall("\d+\.\d+",line)
                metrics["spd_mean"] = float(speed[0])
                metrics["spd_var"] = float(speed[1])
            if line.startswith("Inflow"):
                inflow = re.findall("\d+\.\d+",line)
                metrics["inflow_mean"] = float(inflow[0])
                metrics["inflow_var"] = float(inflow[1])
            if line.startswith("Outflow"):
                outflow = re.findall("\d+\.\d+",line)
                metrics["outflow_mean"] = float(outflow[0])
                metrics["outflow_var"] = float(outflow[1])
    result={}
    result['attr']=attributes
    result['metric']=metrics
    results.append(result)
print("# of results", len(results))
from matplotlib import pyplot as plt

def match(result,fixed_attr):
    result_attr = result['attr']
    for key, value in fixed_attr.items():
        if float(result_attr[key]) != float(value):
            return False
    return True

def collect(results, fixed_attr, metric='outflow'):
    for result in results:
        if match(result, fixed_attr):
            if result['metric']:
                return result['metric'][metric+'_mean'], result['metric'][metric+'_var']
    return np.nan, np.nan


right_inflow=1800
metric='outflow'
#Figure1 Symmetric No Lane change
plt.figure(1)
plt.title("Symmetric Inflow without Lane Change")
plt.xlabel('Symmetric Inflow')
plt.ylabel('{}'.format(metric))
x=[1000, 1200, 1400, 1600, 1800, 2000]
fixed_attr = {'right_human_lc':0.0,
              'assertive':0.0,
              'speedgain':0.0,
              'merge':200.0}
upperbound=[]
output_mean=[]
output_var=[]
for I in x:
    fixed_attr.update({'right_inflow':I})
    fixed_attr.update({'left_inflow':I})
    o_mean, o_var = collect(results,fixed_attr,metric)
    output_mean.append(o_mean)
    output_var.append(o_var)
    upperbound.append(2*I+fixed_attr['merge'])
output_mean, output_var, upperbound = np.array(output_mean), np.array(output_var), np.array(upperbound)
plt.plot(x,upperbound,'--', label='upperbound')
plt.fill_between(x,upperbound, upperbound,alpha=0.3)
plt.plot(x,output_mean, label='Symmetric Inflow, No Lanechange')
plt.fill_between(x,output_mean-output_var, output_mean+output_var,alpha=0.3)
plt.legend()

#Figure2 Asymmetric No Lane change
plt.figure(2)
plt.xlabel('Left Inflow')
plt.ylabel('{}'.format(metric))
plt.title("Asymmetric Inflow without Lane Change, right inflow{}".format(right_inflow))
x=[1000, 1200, 1400, 1600, 1800, 2000]
fixed_attr = {'right_human_lc':0.0,
              'assertive':0.0,
              'speedgain':0.0,
              'merge':200.0,
              'right_inflow':right_inflow}
upperbound=[]
output_mean=[]
output_var=[]
for I in x:
    fixed_attr.update({'left_inflow':I})
    o_mean, o_var = collect(results,fixed_attr,metric)
    output_mean.append(o_mean)
    output_var.append(o_var)
    upperbound.append(I+fixed_attr['right_inflow']+fixed_attr['merge'])
output_mean, output_var, upperbound = np.array(output_mean), np.array(output_var), np.array(upperbound)
plt.plot(x,upperbound,'--', label='upperbound')
plt.fill_between(x,upperbound, upperbound,alpha=0.3)
plt.plot(x,output_mean, label='Aymmetric Inflow, No Lanechange')
plt.fill_between(x,output_mean-output_var, output_mean+output_var,alpha=0.3)
plt.legend()

#Figure3 Asymmetric with Lane change
plt.figure(3)
plt.xlabel('Left Inflow')
plt.ylabel('{}'.format(metric))
plt.title("Asymmetric Inflow with Lane Change Prob 0.2(Decisive), right inflow{}".format(right_inflow))
x=[1000, 1200, 1400, 1600, 1800, 2000]
asss = [0, 5.0]
aggs = [0, 1.0]
fixed_attr = {'right_human_lc':1.0,
              'assertive':0.0,
              'speedgain':0.0,
              'merge':200.0,
              'right_inflow':right_inflow}
for ass in asss:
    for agg in aggs:
        upperbound=[]
        output_mean=[]
        output_var=[]

        for I in x:
            fixed_attr.update({'left_inflow':I})
            fixed_attr.update({'assertive':ass})
            fixed_attr.update({'speedgain':agg})
            if agg==0 and ass==0:
                fixed_attr.update({'right_human_lc':0.0})
            else:
                fixed_attr.update({'right_human_lc':1.0})
            o_mean, o_var = collect(results,fixed_attr,metric)
            output_mean.append(o_mean)
            output_var.append(o_var)
            upperbound.append(I+fixed_attr['right_inflow']+fixed_attr['merge'])
        output_mean, output_var, upperbound = np.array(output_mean), np.array(output_var), np.array(upperbound)
        if sum(output_mean>0)>0:
            if agg==0 and ass==0:
                plt.plot(x,output_mean, label='No Lane-change'.format(ass, agg))
            else:
                plt.plot(x,output_mean, label='ass:{}, spd gain:{}'.format(ass, agg))
            
            plt.fill_between(x,output_mean-output_var, output_mean+output_var,alpha=0.3)

plt.plot(x,upperbound,'--', label='upperbound')
plt.fill_between(x,upperbound, upperbound,alpha=0.3)
plt.legend()

#Figure4 Asymmetric with Lane change
speedgain=10000.0
plt.figure(4)
plt.xlabel('Left Inflow')
plt.ylabel('{}'.format(metric))
plt.title("Asymmetric Inflow with Lane Change, right inflow{}, speedgain {}".format(right_inflow, speedgain))
x=[1000, 1200, 1400, 1600, 1800, 2000]
asss = [0, 0.5, 1.0, 5.0, 10.0]
aggs = [0, 0.5, 1.0, 5.0, 10.0, 100.0, 1000.0, 10000.0]
fixed_attr = {'right_human_lc':1.0,
              'assertive':0.0,
              'speedgain':0.0,
              'merge':200.0,
              'right_inflow':right_inflow}
agg=speedgain
for ass in asss:
    upperbound=[]
    output_mean=[]
    output_var=[]

    for I in x:
        fixed_attr.update({'left_inflow':I})
        fixed_attr.update({'assertive':ass})
        fixed_attr.update({'speedgain':agg})
        o_mean, o_var = collect(results,fixed_attr,metric)
        output_mean.append(o_mean)
        output_var.append(o_var)
        upperbound.append(I+fixed_attr['right_inflow']+fixed_attr['merge'])
    output_mean, output_var, upperbound = np.array(output_mean), np.array(output_var), np.array(upperbound)
    plt.plot(x,output_mean, label='ass:{}, spd gain:{}'.format(ass, agg))
    plt.fill_between(x,output_mean-output_var, output_mean+output_var,alpha=0.3)

plt.plot(x,upperbound,'--', label='upperbound')
plt.fill_between(x,upperbound, upperbound,alpha=0.3)
plt.legend()

#Figure5 Asymmetric with Lane change
assertive=5.0
plt.figure(5)
plt.xlabel('Left Inflow')
plt.ylabel('{}'.format(metric))
plt.title("Asymmetric Inflow with Lane Change, right inflow{}, assertive {}".format(right_inflow, assertive))
x=[1000, 1200, 1400, 1600, 1800, 2000]
asss = [0, 5.0]
aggs = [0, 1.0]
fixed_attr = {'right_human_lc':1.0,
              'assertive':0.0,
              'speedgain':0.0,
              'merge':200.0,
              'right_inflow':right_inflow}
ass=assertive
for agg in aggs:
    upperbound=[]
    output_mean=[]
    output_var=[]

    for I in x:
        fixed_attr.update({'left_inflow':I})
        fixed_attr.update({'assertive':ass})
        fixed_attr.update({'speedgain':agg})
        o_mean, o_var = collect(results,fixed_attr,metric)
        output_mean.append(o_mean)
        output_var.append(o_var)
        upperbound.append(I+fixed_attr['right_inflow']+fixed_attr['merge'])
    output_mean, output_var, upperbound = np.array(output_mean), np.array(output_var), np.array(upperbound)
    plt.plot(x,output_mean, label='ass:{}, spd gain:{}'.format(ass, agg))
    plt.fill_between(x,output_mean-output_var, output_mean+output_var,alpha=0.3)

plt.plot(x,upperbound,'--', label='upperbound')
plt.fill_between(x,upperbound, upperbound,alpha=0.3)
plt.legend()





















































plt.show()
