import os

dict_to_merge={
"vehicle_placement": [
("even_evaluation_placement_inflow_1850_Outflow.tex",
"even_evaluation_placement_inflow_1850_Speed.tex"),
("random_evaluation_placement_inflow_1850_Outflow.tex",
"random_evaluation_placement_inflow_1850_Speed.tex"),
]
,
"best_avp":[
("best_avp_vs_avp_1650_Outflow.tex",
"best_avp_vs_avp_1650_Speed.tex"),
("best_avp_vs_avp_1850_Outflow.tex",
"best_avp_vs_avp_1850_Speed.tex"),
("best_avp_vs_avp_2000_Outflow.tex",
"best_avp_vs_avp_2000_Speed.tex"),
("best_avp_vs_inflow_1650_Outflow.tex",
"best_avp_vs_inflow_1650_Speed.tex"),
("best_avp_vs_inflow_1850_Outflow.tex",
"best_avp_vs_inflow_1850_Speed.tex"),
("best_avp_vs_inflow_2000_Outflow.tex",
"best_avp_vs_inflow_2000_Speed.tex"),
]
,
"best_flow":[
("best_flow_vs_avp_1600_Outflow.tex",
"best_flow_vs_avp_1600_Speed.tex"
),
("best_flow_vs_avp_1800_Outflow.tex",
"best_flow_vs_avp_1800_Speed.tex"
),
("best_flow_vs_avp_2000_Outflow.tex",
"best_flow_vs_avp_2000_Speed.tex"
),
("best_flow_1_Outflow.tex",
"best_flow_1_Speed.tex"
)
,
("best_flow_20_Outflow.tex",
"best_flow_20_Speed.tex"
)
,
("best_flow_40_Outflow.tex",
"best_flow_40_Speed.tex"
)
]
}

def merge_outflow_speed(folder, outflow_filename, speed_filename):
    os_filename="os_"+"_".join(outflow_filename.split("_")[0:-1])+".tex"
    os_file=os.path.join(folder, os_filename)
    outflow_filename=os.path.join(folder, outflow_filename)
    speed_filename=os.path.join(folder, speed_filename)
    with open(os_file, "w") as out_file:
        anchor_node_text=None
        with open(outflow_filename) as flow_file:
            # loop to read iterate
            # last n lines and print it
            lines=flow_file.readlines() 
            for line in lines:
                if line.startswith("\\node["):
                    anchor_node_text=line
                    break
                if "legend style=" in line and "%" not in line:
                    line="legend style={at={(1.1,-0.45)},anchor=south, font=\\large},\n"
                if "cs:0.030" in line:
                    line=line.replace("cs:0.030", "cs:0.0")

                if "transpose legend" in line:
                    continue
                if "legend columns" in line:
                    if 'placement' in outflow_filename:
                        line="\t\t legend columns=4,\n"
                    else:
                        line="\t\t legend columns=3,\n"
                out_file.write(line)
        with open(speed_filename) as speed_file:
            lines=speed_file.readlines()
            begin_to_write=False
            for line in lines:
                if line.startswith("\\begin{axis}"):
                    begin_to_write=True
                if line.startswith("\\node["):
                    continue
                if line.startswith('\\addlegend'):
                    continue
                if "name=ax1" in line:
                    line="at={($(ax1.south east)+(60,0)$)},\n"
                if "\\end{axis}" in line:
                    #anchor_node_text=anchor_node_text.replace("\\\\"," ")
                    line=line+anchor_node_text
                if "cs:0.030" in line:
                    line=line.replace("cs:0.030", "cs:0.050")
                if begin_to_write:
                    out_file.write(line)


for key, tex_list in dict_to_merge.items():
    for outflow_filename, speed_filename in tex_list:
        merge_outflow_speed("./aamas", outflow_filename, speed_filename)

