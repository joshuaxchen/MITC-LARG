import inspect
import os

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
    def set_plot_range(self, xmin, xmax, ymin, ymax):
        self.fname_suffix="_min%d_max%d" % (xmin, xmax)
        self.xmin=xmin
        self.xmax=xmax
        self.ymin=ymin
        self.ymax=ymax
                
    def add_plot(self, label, data):
        label=label.replace("_","-")
        content_str=""
        for value in data:
            content_str+="%s\t%s\t%s\n" % value
        label1=label
        label2=label
        if "*" in label:
            star_text="\\textasteriskcentered{}"
            label2=label.replace("*", star_text)
        self.plot_content+=self.template_plot % (content_str, label1)  
        self.legend+=self.template_legend % (label1, label2)

    def generate_color_lines(self, period, color_same=True):
        j=0
        results=""
        for k in range(len(PlotWriter.colors)):
            color=PlotWriter.colors[k]
            i=0
            for shape in PlotWriter.shapes:
                if j==len(PlotWriter.line_patterns):
                    j=0
                pattern=PlotWriter.line_patterns[j]
                results+=self.template_color % (color, pattern, color, shape)+"\n"
                if not color_same:
                    k=k+1
                    if k==len(PlotWriter.colors):
                        k=0
                    color=PlotWriter.colors[k]
                i+=1
                j+=1
                if i==period:
                    break
        return results
    def set_title(self, title):
        if title and title !="":
            self.title=title
    def write_plot(self, filename, period, color_same=True):
        file1 = open('./template.tex', 'r')
        lines = file1.readlines()
        file1.close()
        header=""
        if self.title:
            #title_statement="\\node[above,font=\\large\\bfseries] at (current bounding box.north) {%s};\n" % self.title
            title_statement="\\node[above,font=\\Large, align=left] at (current bounding box.north) {%s};\n" % self.title
            tail="\\end{axis}\n%s\\end{tikzpicture}\n\\end{document}\n" % title_statement
        else:
            tail="\\end{axis}\n\\end{tikzpicture}\n\\end{document}\n"
        skip=False
        i=0
        while True:
            line=lines[i]
            i+=1
            if "%begin of colors" in line:
                header+=self.generate_color_lines(period, color_same=color_same)
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
                line=line.replace("*range*", ",\n\t xmax={},\n\t xmin={},\n\t ymin={},\n\t ymax={}".format(self.xmax, self.xmin, self.ymin, self.ymax))
                print(filename, "range set")
                #if self.xlabel.endswith("AVP"):
                #    line=line.replace("*range*", ",\n\t xmax=40")
            elif "*range*" in line:
                line=line.replace("*range*", "")
            elif "*xlabel*" in line:
                line=line.replace("*xlabel*",self.xlabel)
            elif "*ylabel*" in line:
                line=line.replace("*ylabel*",self.ylabel)
            axis_setup+=line
            if "%end of axis" in line:
                break

        # add human baseline
        human_template="\\addplot[%s, samples=200] coordinates {(0,%f) (100,%f)};\label{human-%d}"
        content=header+axis_setup+self.plot_content+self.legend+"\n\n"+tail
        file=open(filename, "w")
        file.write(content)
        file.close()

