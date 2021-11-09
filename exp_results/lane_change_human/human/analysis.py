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
        if s.startswith("AGGRESSIVE"):
            attributes["aggressive"]=number
        if s.startswith("ASSERTIVE"):
            attributes["assertive"]=number
        if s.startswith("MERGE"):
            attributes["merge"]=number
    content = open(f,'r')
    start_reading = False
    for line in content:
        if line.startswith("Round  100 :"):
            start_reading = True
        if start_reading: 
            if line.startswith("Speed"):
                speed = re.findall("\d+\.\d+",line)
                attributes["spd_mean"] = float(speed[0])
                attributes["spd_var"] = float(speed[1])
            if line.startswith("Inflow"):
                inflow = re.findall("\d+\.\d+",line)
                attributes["inflow_mean"] = float(inflow[0])
                attributes["inflow_var"] = float(inflow[1])
            if line.startswith("Outflow"):
                outflow = re.findall("\d+\.\d+",line)
                attributes["outflow_mean"] = float(outflow[0])
                attributes["outflow_var"] = float(outflow[1])

    results.append(attributes)

from matplotlib import pyplot as plt


