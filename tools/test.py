from matplotlib_plot import PlotWriter

a=PlotWriter("time", "outflow") 
a.set_plot_range(0, 5, 0, 10)
a.add_plot("test_100", [(1, 2, 0), (2, 3, 0)])
a.add_plot("test_101", [(1, 3, 0), (2, 4, 0)])
a.add_plot("test_102", [(1, 4, 0), (2, 5, 0)])
a.add_plot("test_200", [(1, 5, 0), (2, 6, 0)])
a.add_plot("test_201", [(1, 6, 0), (2, 7, 0)])
a.add_plot("test_202", [(1, 7, 0), (2, 8, 0)])
a.write_plot("test.tex", 2)

