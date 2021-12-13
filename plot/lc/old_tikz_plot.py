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
        self.xmin=None
        self.xmax=None
        self.ymax=None
        self.ymin=None
        self.xlabel=xlabel
        self.ylabel=ylabel
        self.add_human=True
        self.title=None
        #self.template_plot="\\addplot[thick, mark options={mark size=2 pt}, error bars/.cd, y dir=both, y explicit] table [x=a, y=b, y error=c] {\na\t b\t c\n%s};\n\\label{%s}\n\n" 
        #self.template_plot="\\addplot table [x=a, y=b, y error=c] {\na\t b\t c\n%s};\n\\label{%s}\n\n" 
        self.template_plot="\\addplot table [x=a, y=b] {\na\t b\t c\n%s};\n\\label{%s}\n\n" 
        self.template_legend="\\addlegendimage{/pgfplots/refstyle=%s}\n\\addlegendentry{%s}\n"
        self.template_color="\t %s, %s every mark/.append style={fill=%s}, mark=%s, error bars/.cd, y dir=both, y explicit\\\\"
        self.label_list=list()

        self.human_color_map="Greys"
        self.av_color_map="Set1"

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
<<<<<<< HEAD:plot/lc/tikz_plot1.py
        self.label_list.append(label)
    def get_human_and_av_label_size(self, every_n_per_color):
        total_av_color=0
        total_human_color=0
        for label in self.label_list:
            if "human" in label:
                total_human_color+=1
            else:
                total_av_color+=1
        total_av_color=-1*(-1*total_av_color // every_n_per_color) # compute ceil of division
        total_human_color=-1*(-1*total_human_color // every_n_per_color)
        return total_human_color, total_av_color

    def generate_color_lines(self, every_n_per_color):
        total_human_color, total_av_color=self.get_human_and_av_label_size(every_n_per_color)

        human_color_prefix=self.human_color_map+"-"+str(total_human_color+1)
        human_fill_prefix=self.human_color_map+"-"
        human_color_index=0
        av_color_prefix=self.av_color_map+"-" +str(total_av_color)
        av_fill_prefix=self.av_color_map+"-"

        av_color_index=0
        shape_index=0
        line_pattern_index=0
        line_shape_index=1

        results=""
        start='A'
        for label in self.label_list:
            if "human" in label:
                line_color=str(human_color_index//every_n_per_color+1) +" of "+human_color_prefix
                filled_color=human_fill_prefix+chr(ord('A')+1 + human_color_index//every_n_per_color)
                human_color_index+=1
                if human_color_index>every_n_per_color*9:
                    human_color_index=0
            else:
                line_color=str(av_color_index//every_n_per_color) +" of "+av_color_prefix
                filled_color=av_fill_prefix+chr(ord('A') + av_color_index//every_n_per_color)
                av_color_index+=1
                if av_color_index>every_n_per_color*9:
                    av_color_index=0 
            shape=PlotWriter.shapes[shape_index]
            pattern=PlotWriter.line_patterns[line_pattern_index]
            results+=self.template_color % ("index of colormap="+line_color, pattern, filled_color, shape)+"\n"
            shape_index+=1
            if shape_index>=len(PlotWriter.shapes):
                shape_index=0
            line_pattern_index+=1
            if line_pattern_index>=len(PlotWriter.line_patterns):
                line_pattern_index=0
            line_shape_index+=1
            if line_shape_index>every_n_per_color:
                line_shape_index=1
                shape_index=0
                line_pattern_index=0
=======

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
>>>>>>> more_decisive:plot/lc/old_tikz_plot.py
        return results
    def set_title(self, title):
        if title and title !="":
            self.title=title
<<<<<<< HEAD:plot/lc/tikz_plot1.py
    def write_plot(self, filename, every_n_per_color=4):
        file1 = open('./template1.tex', 'r')
=======
    def write_plot(self, filename, period, color_same=True):
        file1 = open('./template.tex', 'r')
>>>>>>> more_decisive:plot/lc/old_tikz_plot.py
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
            if "%color_map_definition" in line:
                total_human_color, total_av_color=self.get_human_and_av_label_size(every_n_per_color)
                human_color_prefix=self.human_color_map+"-"+str(total_human_color+1)
                av_color_prefix=self.av_color_map+"-" +str(total_av_color)
                header+="\pgfplotsset{cycle list/%s}\n" % human_color_prefix 
                header+="\pgfplotsset{cycle list/%s}\n" % av_color_prefix 

            if "%begin of colors" in line:
<<<<<<< HEAD:plot/lc/tikz_plot1.py
                header+=self.generate_color_lines(every_n_per_color)
=======
                header+=self.generate_color_lines(period, color_same=color_same)
>>>>>>> more_decisive:plot/lc/old_tikz_plot.py
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
                range_to_replace=""
                if self.xmax is not None:
                    range_to_replace+="\n\t xmax={}".format(self.xmax)  
                if self.xmin is not None:
                    range_to_replace+="\n\t xmin={}".format(self.xmin)  
                if self.ymax is not None:
                    range_to_replace+="\n\t ymax={}".format(self.ymax)  
                if self.ymin is not None:
                    range_to_replace+="\n\t ymin={}".format(self.ymin)  
                if range_to_replace !="":
                    range_to_replace+=","
                line=line.replace("*range*", range_to_replace)
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

