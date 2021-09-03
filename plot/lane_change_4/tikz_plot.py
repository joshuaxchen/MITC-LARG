class PlotWriter:
    colors=["blue","red","green", "brown", "cyan", "darkgray", "gray", "lightgray", "lime", "magenta", "olive", "orange", "pink", "purple", "teal", "violet", "yellow", "Bittersweet", "BlueViolet", "BrickRed", "BurntOrange", "CadetBlue", "CarnationPink", "Cerulean", "Dandelion", "DarkOrchid", "Emerald", "Fuchsia", "GreenYellow", "Magenta", "Maroon", "MidnightBlue", "Orange", "OrangeRed", "Orchid", "Periwinkle", "RawSienna"]
    shapes=["star", "triangle*", "diamond*", "otimes*", "square*", "x","+","-","o", "oplus*", "oplus", "triangle", "diamond", "otimes", "square"]
    line_patterns=["", "densely dashed", "dashed", "densely dotted", "loosely dotted", "loosely dashed", "densely dashdotted", "loosely dashdottted"]
    def __init__(self, xlabel, ylabel):
        self.plot_content=""
        self.legend=""
        self.fname_suffix=""
        self.xmin=0
        self.xmax=0
        self.xlabel=xlabel
        self.ylabel=ylabel
        self.add_human=True
        #self.template_plot="\\addplot[thick, mark options={mark size=2 pt}, error bars/.cd, y dir=both, y explicit] table [x=a, y=b, y error=c] {\na\t b\t c\n%s};\n\\label{%s}\n\n" 
        #self.template_plot="\\addplot table [x=a, y=b, y error=c] {\na\t b\t c\n%s};\n\\label{%s}\n\n" 
        self.template_plot="\\addplot table [x=a, y=b] {\na\t b\t c\n%s};\n\\label{%s}\n\n" 
        self.template_legend="\\addlegendimage{/pgfplots/refstyle=%s}\n\\addlegendentry{%s}\n"
        self.template_color="\t %s, %s every mark/.append style={fill=%s!20}, mark=%s, error bars/.cd, y dir=both, y explicit\\\\"
    def set_plot_range(self, xmin, xmax):
        self.fname_suffix="_min%d_max%d" % (xmin, xmax)
        self.xmin=xmin
        self.xmax=xmax
                
    def add_plot(self, label, data):
        label=label.replace("_","-")
        content_str=""
        for value in data:
            content_str+="%s\t%s\t%s\n" % value
        self.plot_content+=self.template_plot % (content_str, label)  
        self.legend+=self.template_legend % (label, label)

    def generate_color_lines(self, period):
        j=0
        results=""
        for color in PlotWriter.colors:
            i=0
            for shape in PlotWriter.shapes:
                if j==len(PlotWriter.line_patterns):
                    j=0
                pattern=PlotWriter.line_patterns[j]
                results+=self.template_color % (color, pattern, color, shape)+"\n"
                i+=1
                j+=1
                if i==period:
                    break
        return results

    def write_plot(self, filename, period):
        file1 = open('./template.tex', 'r')
        lines = file1.readlines()
        file1.close()
        header=""
        tail="\\end{axis}\n\\end{tikzpicture}\n\\end{document}\n"
        skip=False
        i=0
        while True:
            line=lines[i]
            i+=1
            if "%begin of colors" in line:
                header+=self.generate_color_lines(period)
                skip=True
            elif "%end of colors" in line:
                header+=line
                break
            elif not skip:
                header+=line 

        axis_setup=""
        while True:          
            line=lines[i]
            i+=1
            if "*range*" in line:
                if self.xlabel.endswith("AVP"):
                    line=line.replace("*range*", ",\n\t xmax=40")
                else:
                    line=line.replace("*range*", "")
            elif "*xlabel*" in line:
                line=line.replace("*xlabel*",self.xlabel)
            elif "*ylabel*" in line:
                line=line.replace("*ylabel*",self.ylabel)
            axis_setup+=line
            if "%end of axis" in line:
                break

        

#        end_line_num_of_color=111
#        end_line_num_of_axis=126
#        for i in range(0, end_line_num_of_color):
#            header+=lines[i]
#        axis_setup=""
#        j=0
#        
#        for i in range(end_line_num_of_color, end_line_num_of_axis):
#            line=lines[i]
#            if "mycolorlist" in lines[i] and self.fname_suffix!="":
#                line=line.strip()+",\n"
#            if "*xlabel*" in line:
#                line=line.replace("*xlabel*",self.xlabel)
#            if "*ylabel*" in line:
#                line=line.replace("*ylabel*",self.ylabel)
#            if "*range*" in line:
#                if self.xlabel.endswith("AVP"):
#                    line=line.replace("*range*", ",\n\t xmax=40")
#                else:
#                    line=line.replace("*range*", "")
#            axis_setup+=line 
        # add human baseline
        human_template="\\addplot[%s, samples=200] coordinates {(0,%f) (100,%f)};\label{human-%d}"
        if self.xlabel.endswith("AVP"):
            mean_1650=1722.20
            mean_1850=1560.38
            mean_2000=1558.12
            mean_2100=1560.31
            mean_2200=1560.38
            mean_2300=1558.66
            mean_2400=1559.52
            mean_2500=1556.64
            mean_2600=1561.28
            self.plot_content+=human_template % (PlotWriter.colors[0], mean_1650, mean_1650, 1650)
            self.legend+=self.template_legend %("human-1650", "human-1650")

            self.plot_content+=human_template % (PlotWriter.colors[1], mean_1850, mean_1850, 1850)
            self.legend+=self.template_legend %("human-1850","human-1850" )

            self.plot_content+=human_template % (PlotWriter.colors[2], mean_2000, mean_2000, 2000)
            self.legend+=self.template_legend %("human-2000","human-2000" )

            self.plot_content+=human_template % (PlotWriter.colors[3], mean_2100, mean_2100, 2100)
            self.legend+=self.template_legend %("human-2100","human-2100" )

            self.plot_content+=human_template % (PlotWriter.colors[4], mean_2200, mean_2200, 2200)
            self.legend+=self.template_legend %("human-2200","human-2200" )
            
            self.plot_content+=human_template % (PlotWriter.colors[5], mean_2300, mean_2300, 2300)
            self.legend+=self.template_legend %("human-2300","human-2300" )

            self.plot_content+=human_template % (PlotWriter.colors[6], mean_2400, mean_2400, 2400)
            self.legend+=self.template_legend %("human-2400","human-2400" )

            self.plot_content+=human_template % (PlotWriter.colors[7], mean_2500, mean_2500, 2500)
            self.legend+=self.template_legend %("human-2500","human-2500" )

            self.plot_content+=human_template % (PlotWriter.colors[8], mean_2600, mean_2600, 2600)
            self.legend+=self.template_legend %("human-2600","human-2600" )

        elif self.add_human:
            human_data=[
                (1600, 1714.93, 78.63),
                (1610, 1740.24, 67.16),
                (1620, 1731.42, 80.21),
                (1630, 1733.36, 86.93),
                (1640, 1731.92, 94.58),
                (1650, 1734.55, 102.65),
                (1660, 1714.68, 109.47),
                (1670, 1709.64, 116.06),
                (1680, 1703.99, 120.06),
                (1690, 1705.57, 118.77),
                (1700, 1694.59, 122.75),
                (1710, 1678.25, 120.81),
                (1720, 1691.06, 130.92),
                (1730, 1670.08, 124.72), 
                (1740, 1644.44, 105.57),
                (1750, 1659.02, 115.09),
                (1760, 1624.90, 92.50),
                (1770, 1615.25, 88.46),
                (1780, 1596.35, 75.51),
                (1790, 1581.01, 47.36),
                (1800, 1572.70, 44.91),
                (1900, 1560.49, 14.78),
                (2000, 1558.12, 15.24),
                (2100,  1560.31, 13.94),
                (2200,  1560.38, 12.38),
                (2250,  1557.14, 12.99),
                (2300,  1558.66, 13.09),
                (2400,  1559.52, 12.93),
                (2500,  1556.64, 13.25),
                (2600,  1561.28, 11.96)
            ]
            self.add_plot("human", human_data)

        content=header+axis_setup+self.plot_content+self.legend+"\n\n"+tail
        file=open(filename, "w")
        file.write(content)
        file.close()


