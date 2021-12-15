import inspect
import os
from matplotlib import pyplot as plt
import matplotlib

matplotlib.use('Agg')

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
        self.title=None
        #plt.figure(0)
        self.data=dict()

    def set_plot_range(self, xmin, xmax, ymin, ymax):
        plt.ylim(ymin, ymax)
        plt.xlim(xmin, xmax)
                
    def add_plot(self, legend, data):
        self.data[legend]=data
                
    def set_title(self, title):
        if title and title !="":
            plt.title(title)
    def write_plot(self, filename, period, color_same=True):
        for key, value in self.data.items():
            x_list=list()
            y_list=list()
            for (x, y, z) in value:
                x_list.append(x)
                y_list.append(y)
            plt.plot(x_list, y_list, label=key)

        plt.legend()
        plt.savefig(filename+".png")
        plt.close()
