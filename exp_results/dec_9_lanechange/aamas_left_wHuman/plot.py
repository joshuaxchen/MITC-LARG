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

template = "EVAL_{}_{}_{}_0_{}_1.0_5.0.txt"
template_human = "EVAL_human_{}_{}_{}_0_{}_1.0_5.0.txt"

line_types=["-", "--", "-.", ":"]

rl_colors = ["blue", "red", "green"]

human_colors = ["darkorange", "yellow", "purple"]

plt.rcParams.update({"font.size": 20})
for j, r_inflow in enumerate([2000]):
    for i, AVP in enumerate([10, 20, 30, 40]):
        results = []
        for l_inflow in [1600, 1800, 2000]:
            results.append(file_results[template.format(r_inflow, l_inflow, 200, AVP)])
        plt.plot([1800, 1900, 2000], results, label=f"AVP={AVP}, Right Inflow={r_inflow}", linestyle=line_types[i], color=rl_colors[j])
        results = []
        for l_inflow in [1600, 1800, 2000]:
            results.append(file_results[template_human.format(r_inflow, l_inflow, 200, AVP)])
        plt.plot([1800, 1900, 2000], results, label=f"HUMAN Percent Frozen={AVP}, Right Inflow={r_inflow}", linestyle=line_types[i], color=human_colors[j])

plt.title("Left RL Vehicles Outflow")
plt.xlabel("Left Inflow")
plt.ylabel("Outflow")
plt.legend()
plt.show()
    
for j, r_inflow in enumerate([2000]):
    for i, AVP in enumerate([10, 20, 30, 40]):
        results = []
        for l_inflow in [1600, 1800, 2000]:
            results.append(speed_results[template.format(r_inflow, l_inflow, 200, AVP)])
        plt.plot([1800, 1900, 2000], results, label=f"AVP={AVP}, Right Inflow={r_inflow}", linestyle=line_types[i], color=rl_colors[j])
        results = []
        for l_inflow in [1600, 1800, 2000]:
            results.append(speed_results[template_human.format(r_inflow, l_inflow, 200, AVP)])
        plt.plot([1800, 1900, 2000], results, label=f"HUMAN Percent Frozen={AVP}, Right Inflow={r_inflow}", linestyle=line_types[i], color=human_colors[j])

plt.title("Left RL Vehicles Speed")
plt.legend()
plt.xlabel("Left Inflow")
plt.ylabel("Speed")
plt.show()

for j, r_inflow in enumerate([2000]):
   for i, l_inflow in enumerate([1600, 1800, 2000]):
        results = []
        for AVP in [10, 20, 30, 40]:
            results.append(file_results[template.format(r_inflow, l_inflow, 200, AVP)])
        plt.plot([10, 20, 30, 40], results, label=f"Left Inflow={l_inflow}", linestyle=line_types[i], color=rl_colors[j])
        results = []
        for AVP in [10, 20, 30, 40]:
            results.append(file_results[template_human.format(r_inflow, l_inflow, 200, AVP)])
        plt.plot([10, 20, 30, 40], results, label=f"HUMAN Left Inflow={l_inflow}", linestyle=line_types[i], color=human_colors[j])

plt.title("Left RL Vehicles Outflow")
plt.xlabel("Left AVP")
plt.ylabel("Outflow")
plt.legend()
plt.show()
    
for j, r_inflow in enumerate([2000]):
    for i, l_inflow in enumerate([1600, 1800, 2000]):
        results = []
        for _, AVP in enumerate([10, 20, 30, 40]):
            results.append(speed_results[template.format(r_inflow, l_inflow, 200, AVP)])
        plt.plot([10, 20, 30, 40], results, label=f"Left Inflow={l_inflow}", linestyle=line_types[i], color=rl_colors[j])
        results = []
        for _, AVP in enumerate([10, 20, 30, 40]):
            results.append(speed_results[template_human.format(r_inflow, l_inflow, 200, AVP)])
        plt.plot([10, 20, 30, 40], results, label=f"HUMAN Left Inflow={r_inflow}", linestyle=line_types[i], color=human_colors[j])

plt.title("Left RL Vehicles Speed")
plt.legend()
plt.xlabel("Left AVP")
plt.ylabel("Speed")
plt.show()
