from DuplicateRemover import Parser
from PaperCounter import PaperPlotter

path_to_data = "/home/boyan/sandbox/utils/data/Results Data Filtering/Data"
Parser = Parser(path_to_data)
Parser.LoadData()
data = Parser.FilterTitle(save_data=True)

Plotter = PaperPlotter(data)
Plotter.process_data()  # Process the data
Plotter.plot_histogram('papers_per_year_histogram.png')  

