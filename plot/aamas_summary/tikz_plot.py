class PlotWriter:
    def __init__(self, xlabel, ylabel):
        self.plot_content=""
        self.legend=""
        self.fname_suffix=""
        self.xmin=0
        self.xmax=0
        self.xlabel=xlabel
        self.ylabel=ylabel
        #self.template_plot="\\addplot[thick, mark options={mark size=2 pt}, error bars/.cd, y dir=both, y explicit] table [x=a, y=b, y error=c] {\na\t b\t c\n%s};\n\\label{%s}\n\n" 
        #self.template_plot="\\addplot table [x=a, y=b, y error=c] {\na\t b\t c\n%s};\n\\label{%s}\n\n" 
        self.template_plot="\\addplot table [x=a, y=b] {\na\t b\t c\n%s};\n\\label{%s}\n\n" 
        self.template_legend="\\addlegendimage{/pgfplots/refstyle=%s}\n\\addlegendentry{%s}\n"
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

    def write_plot(self, filename):
        file1 = open('./template.tex', 'r')
        lines = file1.readlines()
        file1.close()
        header=""
        tail="\\end{axis}\n\\end{tikzpicture}\n\\end{document}\n"
        for i in range(0,40):
            header+=lines[i]
        axis_setup=""
        for i in range(40, 50):
            line=lines[i]
            if "mycolorlist" in lines[i] and self.fname_suffix!="":
                line=line.strip()+",\n"
            if "*xlabel*" in line:
                line=line.replace("*xlabel*",self.xlabel)
            if "*ylabel*" in line:
                line=line.replace("*ylabel*",self.ylabel)
            axis_setup+=line 
        # add human baseline
        human_template="\\addplot[%s, samples=200] coordinates {(0,%f) (100,%f)};\label{human-%d}"
        if self.xlabel.endswith("AVP"):
            mean_1650=1722.20
            mean_1850=1560.38
            mean_2000=1558.12
            self.plot_content+=human_template % ("blue", mean_1650, mean_1650, 1650)
            self.legend+=self.template_legend %("human-1650", "human-1650")

            self.plot_content+=human_template % ("red", mean_1850, mean_1850, 1850)
            self.legend+=self.template_legend %("human-1850","human-1850" )

            self.plot_content+=human_template % ("green", mean_2000, mean_2000, 2000)
            self.legend+=self.template_legend %("human-2000","human-2000" )

        else:
            human_data=[
                (1600, 1714.93, 78.63),
                (1700, 1694.59, 122.75),
                (1800, 1572.70, 44.91),
                (1900, 1560.49, 14.78),
                (2000, 1558.12, 15.24)
            ]
            self.add_plot("human", human_data)

        content=header+axis_setup+self.plot_content+self.legend+"\n\n"+tail
        file=open(filename, "w")
        file.write(content)
        file.close()


