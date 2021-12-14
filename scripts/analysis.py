import re
import glob
import argparse
import numpy as np
from matplotlib import pyplot as plt

filename="human_1600_1200_200_0_10_1_5_ioflow.tex"
filename="human_vehicles_1600_1200_200_0_10_1_5_veh.tex"
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--filename', type=str)
args = parser.parse_args()
filename=args.filename

files = glob.glob("*.tex")
i=0
measure_length=500
for filename in files:
    if "ioflow" in filename or "vehicles" in filename:
        f=open(filename,"r")
        i+=1
    else:
        continue
    
    config = re.findall(r"[-+]?\d*\.\d+|\d+",filename)
    right_inflow = config[0]
    left_inflow = config[1]
    merge_inflow = config[2]
    config = filename.split("_")
    policy_type=config[0]
    if "flow" in filename:
        measure={
            'Inflow':[],
            'Outflow':[]
          }
        start_reading=False
        metric='Inflow'
        for line in f:
        #print(line)
        
            if "addplot" in line:
                start_reading=True
            number = re.findall(r"[-+]?\d*\.\d+|\d+",line)
            if len(number) == 3:
                measure[metric].append(float(number[1]))
            if "label" in line and "Inflow" in line and start_reading:
                start_reading=False
                metric="Outflow"
        plt.figure(i)
        for metric, value in measure.items():
            x = np.arange(len(value)) 
            plt.plot(x, value, label=metric)
        plt.xlabel("timesteps")
        plt.ylabel("Traffic Flow (veh/hr)")
        plt.title("In/Outflow {} Right:{} Left:{} Measure:{} seconds".format(policy_type, right_inflow, left_inflow, measure_length))
        plt.legend()
        plt.ylim(2000, 3500)
        plt.savefig("{}_right{}_left{}_ioflow.png".format(policy_type, right_inflow, left_inflow))
    if "vehicle" in filename:
        measure={
          'Vehicles':[]
          }
        start_reading=False
        metric='Vehicles'
        for line in f:
        #print(line)
        
            if "addplot" in line:
                start_reading=True
            number = re.findall(r"[-+]?\d*\.\d+|\d+",line)
            if len(number) == 3:
                measure[metric].append(float(number[1]))
        plt.figure(i)
        for metric, value in measure.items():
            x = np.arange(len(value)) 
            plt.plot(x, value, label=metric)
        plt.xlabel("timesteps")
        plt.ylabel("# Vehicles")
        plt.title("#Vehicles {} Right:{} Left:{} Measure:{} seconds".format(policy_type, right_inflow, left_inflow, measure_length))
        plt.legend()
        plt.savefig("{}_right{}_left{}_numvehicles.png".format(policy_type, right_inflow, left_inflow))

#plt.show()


