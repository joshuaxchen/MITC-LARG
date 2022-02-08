import os
import matplotlib.pyplot as plt

file_results = {}
speed_results = {}

for fname in os.listdir('./'):
    with open(fname, 'r') as f:
        lines = f.readlines()

    found_outflow = False
    found_speed = False
    for l in reversed(lines):
        s = l.split()
        if len(s) == 0:
            continue
        if s[0] == "Outflow:" and not found_outflow:
            file_results[fname] = float(s[1][:-1])
            found_outflow = True
        if s[0] == "Speed:" and not found_speed:
            speed_results[fname] = float(s[1][:-1])
            found_speed = True

print(file_results)

template = "EVAL_{}_{}_{}_{}_0_1.0_5.0.txt"
template_human = "EVAL_human_{}_{}_{}_{}_0_1.0_5.0.txt"

left_inflow = 1600
plt.rcParams.update({'font.size':20})

line_types = ["-", "--", "-.", ":"]

for i, AVP in enumerate([10, 20, 30, 40]):
    results = []
    for r_inflow in [1600, 1800, 1900, 2000]:
        results.append(file_results[template.format(r_inflow, left_inflow, 200, AVP)])
    plt.plot([1600, 1800, 1900, 2000], results, label=f"AVP={AVP}", color='blue', linestyle=line_types[i])
    results = []
    for r_inflow in [1600, 1800, 1900, 2000]:
        results.append(file_results[template_human.format(r_inflow, left_inflow, 200, AVP)])
    plt.plot([1600, 1800, 1900, 2000], results, label=f"HUMAN Percent Frozen={AVP}", color='red', linestyle=line_types[i])

plt.title("Right RL Vehicles Outflow, Left Inflow=1600")
plt.xlabel("Right Main Inflow")
plt.ylabel("Outflow")
plt.legend()
plt.show()
    
for i, AVP in enumerate([10, 20, 30, 40]):
    results = []
    for r_inflow in [1600, 1800, 1900, 2000]:
        results.append(speed_results[template.format(r_inflow, left_inflow, 200, AVP)])
    plt.plot([1600, 1800, 1900, 2000], results, label=f"AVP={AVP}", color='blue', linestyle=line_types[i])
    results = []
    for r_inflow in [1600, 1800, 1900, 2000]:
        results.append(speed_results[template_human.format(r_inflow, left_inflow, 200, AVP)])
    plt.plot([1600, 1800, 1900, 2000], results, label=f"HUMAN Percent Frozen={AVP}", color='red', linestyle=line_types[i])

plt.title("Right RL Vehicles Speed, Left Inflow=1600")
plt.xlabel("Right Main Inflow")
plt.ylabel("Speed")
plt.legend()
plt.show()

for i, r_inflow in enumerate([1600, 1800, 1900, 2000]):
    results = []
    for AVP in [10, 20, 30, 40]:
        results.append(file_results[template.format(r_inflow, left_inflow, 200, AVP)])
    plt.plot([10, 20, 30, 40], results, label=f"Right Inflow={r_inflow}", color='blue', linestyle=line_types[i])
    results = []
    for AVP in [10, 20, 30, 40]:
        results.append(file_results[template_human.format(r_inflow, left_inflow, 200, AVP)])
    plt.plot([10, 20, 30, 40], results, label=f"HUMAN Right Inflow={r_inflow}", color='red', linestyle=line_types[i])

plt.title("Right RL Vehicles Outflow, Left Inflow=1600")
plt.xlabel("Right AVP")
plt.ylabel("Outflow")
plt.legend()
plt.show()
    
for i, r_inflow in enumerate([1600, 1800, 1900, 2000]):
    results = []
    for AVP in [10, 20, 30, 40]:
        results.append(speed_results[template.format(r_inflow, left_inflow, 200, AVP)])
    plt.plot([10, 20, 30, 40], results, label=f"Right Inflow={r_inflow}", color='blue', linestyle=line_types[i])
    results = []
    for AVP in [10, 20, 30, 40]:
        results.append(speed_results[template_human.format(r_inflow, left_inflow, 200, AVP)])
    plt.plot([10, 20, 30, 40], results, label=f"HUMAN Right Inflow={r_inflow}", color='red', linestyle=line_types[i])

plt.title("Right RL Vehicles Speed, Left Inflow=1600")
plt.xlabel("Right AVP")
plt.ylabel("Speed")
plt.legend()
plt.show()
